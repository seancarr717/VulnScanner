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
    data = request.get_json()
    scan_id = data.get('scanId')
    # Define API details
    
    report_endpoint = f"{ZAP_API_URL}/OTHER/core/other/xmlreport/?apikey={ZAP_API_KEY}&scanId={scan_id}&formMethod=GET"
    
    # Attempt to fetch the XML report from the ZAP API
    try:
        response = requests.get(report_endpoint)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        xml_report = response.content
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 400

    # Decode XML report, assuming xml_report is in bytes
    decoded_xml_report = xml_report.decode('utf-8')

    # Query the database for an existing scan result
    scan_result = ScanResult.query.filter_by(scan_id=scan_id).first()

    if scan_result:
        # If a scan result exists, update the xml_report
        scan_result.xml_report = decoded_xml_report
    else:
        # If no scan result exists, create a new one
        scan_result = ScanResult(scan_id=scan_id, xml_report=decoded_xml_report)
        db.session.add(scan_result)

    # Attempt to commit changes to the database
    try:
        db.session.commit()
        return jsonify({"message": "XML report fetched and saved successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

def view_scan_result():
    scan_id = request.args.get('scanId')
    if not scan_id:
        return jsonify({"error": "Scan ID is required"}), 400

    scan_result = ScanResult.query.filter_by(scan_id=scan_id).first()
    if scan_result and scan_result.xml_report:
        return jsonify({"scan_id": scan_id, "xml_report": scan_result.xml_report})
    else:
        return jsonify({"error": "No results found for the provided scan ID"}), 404