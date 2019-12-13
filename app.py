
from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId
import os
from pymongo import MongoClient

host = os.environ.get('MONGODB_URI','mongodb://localhost:27017/finalProj')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
posts = db.posts

app = Flask(__name__)

# posts = [
#     {
#         'author': 'Barack Obama',
#         'title': 'Blog Post 1',
#         'content': 'First post content',
#         'date_posted': 'April 20, 2018'
#     },
#     {
#         'author': 'Jane Doe',
#         'title': 'Blog Post 2',
#         'content': 'Second post content'
#         'date_posted': 'April 21, 2018'
#     }
# ]


# @app.route("/")
# @app.route("/home")
# def home():
#     return render_template('home.html', post=post)


@app.route("/about", methods=['GET','POST'])
def about():
    return render_template('about.html', title="New Post" )

@app.route('/')
def index():
    """Show all appointments."""
    return render_template('home.html', posts=posts.find())

@app.route('/book_post')
def show_book_post_form():
    """Show Book Appointment Form"""
    return render_template('book_post.html')

@app.route('/book_post', methods=['Post'])
def submit_post():
    """Submit new post."""
    print(request.form)
    post = {
       'firstname':request.form.get('firstname'),
       'lastname':request.form.get('lastname'),

   }
    post_id = posts.insert_one(post).inserted_id
    return redirect(url_for('post_show', post_id=post_id))

@app.route('/posts/<post_id>', methods=['GET'])
def post_show(post_id):
    """Show a single post."""
    post = posts.find_one({'_id': ObjectId(post_id)})
    return render_template('post_show.html', post=post)

@app.route('/post/<post_id>/edit')
def post_edit(post_id):
    """Show the edit form for an post."""
    post = posts.find_one({'_id': ObjectId(post_id)})
    return render_template('post_edit.html', post=post, title='Edit Appointment')

@app.route('/post/<post_id>', methods=['POST'])
def post_update(post_id):
    """Submit an edited post."""
    updated_post = {
        'firstname':request.form.get('firstname'),
        'lastname':request.form.get('lastname'),
        'address':request.form.get('address'),
       }

    posts.update_one({'_id': ObjectId(post_id)}, {'$set': updated_post})
    return redirect(url_for('post_show', post_id=post_id))


@app.route('/post/<post_id>/delete', methods=['POST'])
def post_delete(post_id):
    """Delete one post."""
    posts.delete_one({'_id': ObjectId(post_id)})
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
