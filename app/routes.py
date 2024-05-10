from flask import render_template, redirect, url_for, session,request,abort,jsonify
from .auth import login, logout,register
from .network import run_nmap
from .web import start_spider, start_active_scan
from .models import db, NetworkScan, ScanResult

def configure_routes(app):
    @app.route('/')
    def home():
        if 'user_id' in session:
            unique_ips = NetworkScan.query.filter_by(user_id=session['user_id']).with_entities(NetworkScan.ip_address).distinct()
            return render_template('index.html', unique_ips=unique_ips)
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
        if 'user_id' not in session:
            return redirect(url_for('login_route'))
        return run_nmap()
    
    @app.route('/scans/<ip_address>')
    def show_scans(ip_address):
        if 'user_id' not in session:
            return redirect(url_for('login_route'))
    
        scans = NetworkScan.query.filter_by(ip_address=ip_address, user_id=session['user_id']).all()
        if not scans:
            abort(404)  # Or handle the case where no scans are found differently
        return render_template('scans.html', scans=scans, ip_address=ip_address)

    @app.route('/spider')
    def spider_route():
        if 'user_id' in session:
            return render_template('spider.html')
        return redirect(url_for('login_route'))

    @app.route('/start_spider', methods=['POST'])
    def start_spider_route():
        return start_spider()

    @app.route('/start_active_scan', methods=['POST'])
    def start_active_scan_route():
        return start_active_scan()
    
    @app.route('/download_results/<scan_type>/<scan_id>')
    def download_results(scan_type, scan_id):
        if 'user_id' not in session:
            return jsonify({"error": "User not logged in"}), 401

        user_id = session['user_id']
        scan = ScanResult.query.filter_by(scan_id=scan_id, scan_type=scan_type, user_id=user_id).first()
        if scan and scan.results:
            return jsonify({scan.results})
        return jsonify({"error": "Results not found or scan not completed"}), 404
    

