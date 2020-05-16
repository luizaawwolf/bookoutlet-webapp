from flask import Flask, redirect, render_template, request, url_for
from app import app
import requests
import urllib.request
from bs4 import BeautifulSoup
from betterreads import client
import urllib.parse

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/main', methods=["GET","POST"])
def main():
	if request.method == 'GET':
		return render_template("main_page.html")
	if request.method == 'POST':
		api_key = "Eny1ro9b7mxhs8CuFj2o6w"
		api_secret = "bQKcvwYsv0ceEBjk95guDtguTXRUSgBxGPBT0YtxD6U"
		gc = client.GoodreadsClient(api_key, api_secret)
		if request.method == 'POST':
			user_id = int( request.form['user_id'] )
			user = gc.user(user_id)
			books = user.per_shelf_reviews(shelf_name = "currently-reading")
			valid_books = []
			for review in books:
				temp_book = review.book
				title = temp_book["title"]
				author = temp_book["authors"]["author"]["name"]
				arr = bookOutletHas(title=title, author=author)
				if arr[0]:
					valid_books += [ arr[1] ]
		return render_template("main_page.html", sum=valid_books)

def bookOutletHas(title, author):
	title = title.split(" (")[0]
	title_url = urllib.parse.quote_plus(title)
	url = 'https://bookoutlet.com/Store/Search?qf=All&q=' + title_url
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'html.parser')
	script = soup.findAll('script')
	book_json = script[8].string
	book_json = book_json.split("products = ")[1]
	book_json = book_json.split(";")[0]
	correct_title = False;
	correct_author = True;
	book_json = book_json.lower()
	title = title.lower()

	if( title in book_json ):
		correct_title = True
	title_ind = book_json.find(title)

	if title_ind == -1:
		return [False,"not found"]

	auth_begin = book_json.lower().find("name", title_ind)
	auth_end = book_json.lower().find("id", title_ind)
	author_bo = book_json[auth_begin : auth_end ]

	if( author in author_bo ):
		correct_author = True
	author = author.lower().split()

	for a in author:
		if a not in author_bo:
		    correct_author = False
		    break
	    
	if( correct_title & correct_author):
		print(url)
		return [True, url]
	return [False,"not found"]