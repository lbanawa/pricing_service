import functools
from typing import Callable
from flask import session, flash, redirect, url_for

#  python decorator that takes in a callable and returns a callable
# decorated functions extend other functions within our application
def requires_login(f: Callable) -> Callable:
    # args = arguments, kwargs = keyword arguments
    # this function can have any number of arguments, and any number of keyword arguments
    @functools.wraps(f) # you need a decorator in order to define one
    def decorated_fuction(*args, **kwargs):
        if not session.get('email'):
            # place this message into a queue of messages, and from your template you can get all messages from that queue and display to user
            flash('You need to be signed in for this page.', 'danger')
            # if user is not logged in, redirect them to log in page, message stored in queue will show here
            return redirect(url_for('users.login_user'))
        # if user is logged in, take all arguments put into this function and call the original function with those
        return f(*args, **kwargs)
    # return the function itself, not the decorated function execution
    return decorated_fuction