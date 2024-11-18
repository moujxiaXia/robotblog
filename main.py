from flask import Flask, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_all_posts():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute('SELECT * FROM posts ORDER BY created_date DESC')
    posts = c.fetchall()
    conn.close()
    return posts

@app.route('/')
def home():
    posts = get_all_posts()
    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/post/<int:post_id>')
def post(post_id):
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    post = c.execute(
        'SELECT id, title, content, created_date'
        ' FROM posts '
        ' WHERE id = ?',
        (post_id,)
    ).fetchone()
    conn.close()

    if post is None:
        abort(404, f"Post id {post_id} doesn't exist.")

    return render_template('post.html', post=post)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)


