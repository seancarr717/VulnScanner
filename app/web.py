from flask import request, jsonify,render_template,session
import requests
from .models import db, ScanResult

ZAP_API_URL = "http://ec2-51-20-35-101.eu-north-1.compute.amazonaws.com:9090"
ZAP_API_KEY = "AMWFOWAIOFNA"

def start_spider():
    return start_zap_scan(request, 'spider')

def start_active_scan():
    return start_zap_scan(request, 'ascan')

def start_zap_scan(request, scan_type):
    data = request.get_json()
    target_url = data.get('url')
    if not target_url:
        return jsonify({"error": "URL is required"}), 400
    zap_endpoint = f"{ZAP_API_URL}/JSON/{scan_type}/action/scan?apikey={ZAP_API_KEY}&url={target_url}"
    response = requests.get(zap_endpoint)
    if response.status_code == 200:
        scan_data = response.json()
        scan_id = scan_data.get('scan')
        if scan_id:
            new_scan = ScanResult(
                scan_id=scan_id,
                scan_type=scan_type,
                status='started',
                user_id=session.get('user_id'),
                results=''
            )
            db.session.add(new_scan)
            db.session.commit()
            return jsonify({"message": "Scan started", "scan_id": scan_id}), 200
        else:
            return jsonify({"error": "Failed to retrieve scan ID"}), 500
    else:
        return jsonify({"error": "Failed to start scan"}), response.status_code