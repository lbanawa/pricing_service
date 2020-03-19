from flask import Blueprint, request, session, url_for, render_template, redirect
from models.user import User, UserErrors


user_blueprint = Blueprint('users', __name__)


# register a new user
@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            User.register_user(email, password)
            # keep track of when a user is logged in or not
            session['email'] = email
            return email
        except UserErrors.UserError as e:
            return e.message

    return render_template('users/register.html')

# log in an existing user
@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                return email
        except UserErrors.UserError as e:
            return e.message

    return render_template('users/login.html')