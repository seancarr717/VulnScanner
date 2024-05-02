from flask import render_template, redirect, url_for, session
from .auth import login, logout
from .network import run_nmap
from .web import start_spider, start_active_scan

def configure_routes(app):
    @app.route('/')
    def home():
        if 'username' in session:
            return render_template('index.html', username=session['username'])
        return redirect(url_for('login_route'))

    @app.route('/login', methods=['GET', 'POST'])
    def login_route():
        return login()

    @app.route('/logout')
    def logout_route():
        return logout()

    @app.route('/network', methods=['GET', 'POST'])
    def network_route():
        if 'username' not in session:
            return redirect(url_for('login_route'))
        return run_nmap()

    @app.route('/spider')
    def spider_route():
        if 'username' in session:
            return render_template('spider.html')
        return redirect(url_for('login_route'))

    @app.route('/start_spider', methods=['POST'])
    def start_spider_route():
        return start_spider()

    @app.route('/start_active_scan', methods=['POST'])
    def start_active_scan_route():
        return start_active_scan()