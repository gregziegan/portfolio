from functools import wraps
from flask import g, url_for, flash, request, redirect

def requires_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash(u'You need to be signed in for this page.')
            return redirect(url_for('login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function

def requires_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash(u'You need to be logged in for this page.')
            return redirect(url_for('login', next=request.path))
        elif g.user['is_admin'] == 0:
            flash(u'You must be an admin to register new users.')
            return redirect(url_for('index', next=request.path))
        return f(*args, **kwargs)
    return decorated_function
