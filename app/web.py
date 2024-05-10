from flask import request, jsonify,session
import requests
import requests
import time
from .models import db, ScanResult

ZAP_API_URL = "http://ec2-51-20-35-101.eu-north-1.compute.amazonaws.com:9090"
ZAP_API_KEY = "AMWFOWAIOFNA"

def start_spider():
    return start_zap_scan(request, 'spider')

def start_active_scan():
    return start_zap_scan(request, 'ascan')

def start_zap_scan(request, scan_type):
    if 'user_id' not in session:
        return jsonify({"error": "User not logged in"}), 401

    user_id = session['user_id']
    data = request.get_json()
    target_url = data.get('url')
    if not target_url:
        return jsonify({"error": "URL is required"}), 400

    zap_endpoint = f"{ZAP_API_URL}/JSON/{scan_type}/action/scan?apikey={ZAP_API_KEY}&url={target_url}"
    response = requests.get(zap_endpoint)
    scan_id = response.json().get('scan') if response.status_code == 200 else None

    if scan_id:
        new_scan = ScanResult(scan_id=scan_id, scan_type=scan_type, status='started', results=None, user_id=user_id)
        db.session.add(new_scan)
        db.session.commit()
        track_scan_progress(scan_type, scan_id, user_id)

    return jsonify({"message": f"{scan_type.capitalize()} scan started", "scan_id": scan_id})

def track_scan_progress(scan_type, scan_id, user_id):
    while True:
        status_response = requests.get(f"{ZAP_API_URL}/JSON/{scan_type}/view/status?apikey={ZAP_API_KEY}&scanId={scan_id}")
        status = status_response.json().get('status')
        if status == '100':  # Assuming 100 means completed
            results_response = requests.get(f"{ZAP_API_URL}/JSON/{scan_type}/view/results?apikey={ZAP_API_KEY}&scanId={scan_id}")
            results = results_response.json()
            scan = ScanResult.query.filter_by(scan_id=scan_id, user_id=user_id).first()
            if scan:
                scan.results = results
                scan.status = 'completed'
                db.session.commit()
            break
        time.sleep(10)  # Wait for 10 seconds before polling again