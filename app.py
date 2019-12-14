
from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId
import os
from pymongo import MongoClient

host = os.environ.get('MONGODB_URI','mongodb://localhost:27017/posts')
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
@app.route('/')
def index():
    """Show posts."""
    return render_template('home.html', posts=posts.find())

@app.route("/about", methods=['GET','POST'])
def about():
    return render_template('about.html', title="New Post" )



@app.route('/create_post')
def show_post():
    """Show Posts"""
    return render_template('about.html')

@app.route('/create_post', methods=['Post'])
def submit_post():
    """Submit new post."""
    print(request.form)
    post = {
       'name':request.form.get('name'),
       'date':request.form.get('date'),
       'body':request.form.get('body')

   }
    post_id = posts.insert_one(post).inserted_id
    return redirect(url_for('post_show', post_id=post_id))

@app.route('/posts/<post_id>', methods=['GET'])
def post_show(post_id):
    """Show a post."""
    post = posts.find_one({'_id': ObjectId(post_id)})
    return render_template('post_show.html', post=post)

@app.route('/post/<post_id>/edit')
def post_edit(post_id):
    """Edit a post."""
    post = posts.find_one({'_id': ObjectId(post_id)})
    return render_template('post_edit.html', post=post, title='Edit Post')

@app.route('/post/<post_id>', methods=['POST'])
def post_update(post_id):
    """Add edit to post."""
    updated_post = {
        'name':request.form.get('name'),
        'date':request.form.get('date'),
        'body':request.form.get('body'),
       }

    posts.update_one({'_id': ObjectId(post_id)}, {'$set': updated_post})
    return redirect(url_for('post_show', post_id=post_id))

@app.route('/post/<post_id>/delete', methods=['POST'])
def post_delete(post_id):
    """Delete post."""
    posts.delete_one({'_id': ObjectId(post_id)})
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
