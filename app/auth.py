from flask import session, redirect, url_for, request, render_template,flash
from .models import User
from . import db


def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')

def register(username, password):
    # Check if user already exists
    if User.query.filter_by(username=username).first():
        flash('Username already exists.')
        return redirect(url_for('register_route'))

    # Create new user with hashed password
    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    flash('User successfully registered!')
    return redirect(url_for('login_route'))

def logout():
    session.pop('username', None)
    return redirect(url_for('login_route'))