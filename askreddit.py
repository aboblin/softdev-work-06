'''
dataset: AskReddit
description: A list of posts on the subreddit /r/AskReddit. It includes information of each post such as its author, its url, its upvotes/downvotes, and much much more.
download: https://www.reddit.com/r/AskReddit.json
summary of import: We first read the .json file using open() and .read(). Then we turn the contents into a python dictionary using json.loads(). After this, we used created a list of the posts using jsoncont["data"]["children"] (there was additional information about the subreddit). The we used insert_many() to import it into the database.
'''
from flask import Flask, render_template, request
import pymongo
import json
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route('/')
def root():
	return render_template('askReddit.html')

@app.route('/authors', methods=['POST', 'GET'])
def authors():
	author = request.form['authorbox']

	connection = pymongo.MongoClient("homer.stuy.edu")
	db = connection.askreddit
	ar = db.posts

	stuffers = ar.find({"data.author": author})

	return render_template('response.html', posts = stuffers)

@app.route('/scores', methods=['POST', 'GET'])
def scores():

	score = int(request.form['scorebox'])

	connection = pymongo.MongoClient("homer.stuy.edu")
	db = connection.askreddit
	ar = db.posts

	stuffers = ar.find({"data.score": { "$gt": score } })

	return render_template('response.html', posts = stuffers)

@app.route('/tags', methods=['POST', 'GET'])
def tags():
	tag = request.form['tagbox']

	connection = pymongo.MongoClient("homer.stuy.edu")
	db = connection.askreddit
	ar = db.posts

	stuffers = ar.find({"data.link_flair_css_class": tag})

	return render_template('response.html', posts = stuffers)


if __name__ == '__main__':
	
	connection = pymongo.MongoClient("homer.stuy.edu")
	db = connection.askreddit
	db.posts.drop()
	db = connection.askreddit
	ar = db.posts
	filename = "AskReddit.json"
	file = open(filename, "r")
	contents = file.read()
	jsoncont = json.loads(contents)
	posts2 = jsoncont["data"]["children"]
	ar.insert_many(posts2)
	file.close()
	app.debug = True
	app.run()

'''
#print posts that fall under the serious tag
x = ar.find({"data.link_flair_css_class": "serious"})
for post in x:
    print post

#print posts that are made by the author J-Bradley1
y = ar.find({"data.author": "J-Bradley1"})
for post in y:
    print post

#print posts with a score greater than 50 
c = ar.find( { "data.score": { "$gt": 50 } } )
for post in c:
    print post
'''
