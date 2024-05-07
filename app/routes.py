from flask import render_template, redirect, url_for, session,request
from .auth import login, logout,register
from .network import run_nmap
from .web import start_spider, start_active_scan
from .models import db, NetworkScan

def configure_routes(app):
    @app.route('/')
    def home():
        if 'username' in session:
            unique_ips = NetworkScan.query.with_entities(NetworkScan.ip_address).distinct()
            return render_template('index.html', username=session['username'], unique_ips=unique_ips)
        return redirect(url_for('login_route'))

    @app.route('/login', methods=['GET', 'POST'])
    def login_route():
        return login()

    @app.route('/logout')
    def logout_route():
        return logout()
    
    @app.route('/register', methods=['GET', 'POST'])
    def register_route():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            return register(username, password)
        else:
            return render_template('register.html')

    @app.route('/network', methods=['GET', 'POST'])
    def network_route():
        if 'username' not in session:
            return redirect(url_for('login_route'))
        return run_nmap()
    
    @app.route('/scans/<ip_address>')
    def show_scans(ip_address):
        scans = NetworkScan.query.filter_by(ip_address=ip_address).all()
        return render_template('scans.html', scans=scans, ip_address=ip_address)

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