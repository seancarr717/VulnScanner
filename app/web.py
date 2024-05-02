from flask import request, jsonify

ZAP_API_URL = "http://localhost:9090"
ZAP_API_KEY = "1mag%GjdDmjj3or!jt24gp1zk"

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
    response = request.get(zap_endpoint)
    scan_id = response.json().get('scan') if response.status_code == 200 else None
    return jsonify({"message": f"{scan_type.capitalize()} scan started", "scan_id": scan_id})