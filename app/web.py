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
    

def generate_xml_report(scan_id):
    report_endpoint = f"{ZAP_API_URL}/OTHER/core/other/xmlreport/?apikey={ZAP_API_KEY}&formMethod=GET"
    response = requests.get(report_endpoint)
    if response.status_code == 200:
        return response.content  # This should be the XML content
    else:
        return {"error": "Failed to generate XML report", "status_code": response.status_code}
    
def api_generate_xml_report():
    data = request.get_json()
    scan_id = data.get('scanId')
    if not scan_id:
        return jsonify({"error": "Scan ID is required"}), 400

    xml_report = generate_xml_report(scan_id)
    if isinstance(xml_report, dict) and 'error' in xml_report:
        return jsonify(xml_report), 400

    
    scan_result = ScanResult.query.filter_by(scan_id=scan_id).first()
    if scan_result:
        scan_result.xml_report = xml_report.decode('utf-8')  
    else:
        scan_result = ScanResult(scan_id=scan_id, xml_report=xml_report.decode('utf-8'))
        db.session.add(scan_result)
        
        db.session.commit()

    return jsonify({"message": "XML report generated successfully"})

def view_scan_result():
    scan_id = request.args.get('scanId')
    if not scan_id:
        return jsonify({"error": "Scan ID is required"}), 400

    scan_result = ScanResult.query.filter_by(scan_id=scan_id).first()
    if scan_result and scan_result.xml_report:
        return jsonify({"scan_id": scan_id, "xml_report": scan_result.xml_report})
    else:
        return jsonify({"error": "No results found for the provided scan ID"}), 404