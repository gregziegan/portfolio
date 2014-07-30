# -*- coding: utf-8 -*-
from time import strftime
import time
from flask import Flask, request, session, url_for, redirect, \
        render_template, g, flash
from jinja2 import evalcontextfilter, Markup, escape
from werkzeug import check_password_hash, generate_password_hash
from werkzeug.routing import BaseConverter
from werkzeug.utils import secure_filename
from hashlib import md5
from utils import requires_login, requires_admin
import datetime
import json
import re
import sqlite3

app = Flask(__name__)
app.config.from_object('config')

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n')
                          for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def connect_db():
    con = sqlite3.connect(app.config['DATABASE'])
    con.row_factory = dict_factory
    return con

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


def init_db():
    """Creates the database tables."""
    with app.app_context():
        g.db = connect_db()
        with app.open_resource('schema.sql', mode='r') as f:
            g.db.cursor().executescript(f.read())
        g.db.commit()


def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    cur = g.db.execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv


def get_user_id(username):
    """Convenience method to look up the id for a username."""
    rv = query_db('select user_id from user where username = ?',
                  [username], one=True)
    return rv[0] if rv else None


@app.before_request
def before_request():
    g.db = connect_db()
    g.user = None
    if 'user_id' in session:
        g.user = query_db('select * from user where user_id = ?',
                          [session['user_id']], one=True)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Logs the user in."""
    if g.user:
        return redirect(url_for('index'))
    error = None
    if request.method == 'POST':
        user = query_db('''select * from user where
            username = ?''', [request.form['username']], one=True)
        if user is None:
            error = 'Invalid username'
        elif not check_password_hash(user['pw_hash'],
                                     request.form['password']):
            error = 'Invalid password'
        else:
            session['user_id'] = user['user_id']
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    """Logs the user out."""
    flash('You were logged out')
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registers a new user."""
    error = None
    if request.method == 'POST':
        if not request.form['username']:
            error = 'You have to enter a username'
        elif not request.form['email'] or \
                 '@' not in request.form['email']:
            error = 'You have to enter a valid email address'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'The two passwords do not match'
        elif get_user_id(request.form['username']) is not None:
            error = 'The username is already taken'
        else:
            is_admin = 1 if request.form.get('is_admin') else 0
            g.db.execute('''insert into user (
              username, email, pw_hash, is_admin) values (?, ?, ?, ?)''',
              [request.form['username'], request.form['email'],
               generate_password_hash(request.form['password']), is_admin])
            g.db.commit()
            return redirect(url_for('login'))
    return render_template('register.html', error=error)

@app.route('/')
def index():
    most_recent_post = query_db('select * from blog_post order by post_id desc limit 1', one=True)
    return render_template('index.html', most_recent_post=most_recent_post)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/pyohio14-presentation')
def pyohio_presentation():
    return render_template('pyohio14_presentation.html')

@app.route('/blog')
def blog():
    blog_posts = query_db('select * from blog_post limit 5')
    return render_template('blog.html', blog_posts=blog_posts)

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        print "in post"
        email = request.form['email']
        message = request.form['message']
        if g.user:
            g.db.execute('insert into private_message (email, message, user_id) values (?, ?, ?)',
                          [email, message, g.user['user_id']])
            g.db.commit()
        else:
            name = request.form['contact_name']
            g.db.execute('insert into private_message (name, email, message) values (?, ?, ?)',
                          [name, email, message])
            g.db.commit()
        return redirect(url_for('index'))

    return render_template('contact.html')

@requires_admin
@app.route('/new_blog_post', methods=['GET', 'POST'])
def new_blog_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        poster_id = g.user['user_id']
        g.db.execute('insert into blog_post (title, content, poster_id) values (?, ?, ?)', [title, content, poster_id])
        g.db.commit()
        return redirect(url_for('blog'))
    return render_template('blog_post.html', post=None)

@requires_admin
@app.route('/edit_blog_post/<regex("\d+"):post_id>', methods=['GET', 'POST'])
def edit_blog_post(post_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        g.db.execute('update blog_post set title = ?, content = ? where post_id = ?', [title, content, post_id])
        g.db.commit()
        return redirect(url_for('blog'))
    post = query_db('select * from blog_post where post_id = ?', [post_id], one=True)
    return render_template('blog_post.html', post=post)


if __name__ == '__main__':
    app.run()
