from flask import request, jsonify
import requests

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
    scan_id = response.json().get('scan') if response.status_code == 200 else None
    return jsonify({"message": f"{scan_type.capitalize()} scan started", "scan_id": scan_id})

def get_scans_status():
    zap_endpoint = f"{ZAP_API_URL}/JSON/ascan/view/scans/?apikey={ZAP_API_KEY}"
    response = requests.get(zap_endpoint)
    scans = response.json() if response.status_code == 200 else {}
    return scans
