from flask import session, redirect, url_for, request, render_template

def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['username'] = username
        return redirect(url_for('home'))
    return render_template('login.html')

def logout():
    session.pop('username', None)
    return redirect(url_for('login_route'))