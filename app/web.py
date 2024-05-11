from flask import request, jsonify,render_template,session
import requests
import json
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
    scan_id = response.json().get('scan') if response.status_code == 200 else None
    return jsonify({"message": f"{scan_type.capitalize()} scan started", "scan_id": scan_id})

def get_scan_status():
    data = request.get_json()
    scan_id = data.get('scanId')
    if not scan_id:
        return jsonify({"error": "Scan ID is required"}), 400
    
    zap_endpoint = f"{ZAP_API_URL}/JSON/ascan/view/status/?apikey={ZAP_API_KEY}&scanId={scan_id}"
    response = requests.get(zap_endpoint)
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to fetch scan status"}), response.status_code
    

def fetch_scan_results(scan_id, scan_type):
    results_endpoint = f"{ZAP_API_URL}/JSON/{scan_type}/view/results?apikey={ZAP_API_KEY}&scanId={scan_id}"
    response = requests.get(results_endpoint)
    if response.status_code == 200:
        results_data = response.json()
        return results_data
    else:
        return jsonify({"error": "Failed to fetch scan results", "status_code": response.status_code})
    

def fetch_and_save_results():
    data = request.get_json()
    scan_id = data.get('scanId')
    scan_type = 'ascan'  # or 'spider', depending on your setup

    results = fetch_scan_results(scan_id, scan_type)
    if 'error' in results:
        return jsonify(results), 400

    # Check if a record already exists for this scan
    scan_result = ScanResult.query.filter_by(scan_id=scan_id).first()
    if scan_result:
        # Update existing record
        scan_result.results = results
        scan_result.status = 'completed'
    else:
        # Create a new record
        scan_result = ScanResult(scan_id=scan_id, scan_type=scan_type, results=results, status='completed')
        db.session.add(scan_result)

    # Commit changes to the database
    db.session.commit()
    
    return jsonify({"message": "Results fetched successfully", "results": results})