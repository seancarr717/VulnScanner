from flask import request, render_template, redirect, url_for
import subprocess
import xml.etree.ElementTree as ET

def parse_nmap_xml(xml_output):
    root = ET.fromstring(xml_output)
    scan_data = []
    for host in root.findall('host'):
        for address in host.findall('address'):
            ip = address.get('addr')
            scan_data.append({'IP': ip, 'Ports': []})
        for port in host.find('ports').findall('port'):
            portid = port.get('portid')
            state = port.find('state').get('state')
            scan_data[-1]['Ports'].append((portid, state))
    return scan_data

def run_nmap():
    if request.method == 'POST':
        ip_address = request.form['ip']
        ports = request.form['ports']
        flags = request.form['flags']
        command = f"nmap {flags} -p {ports} {ip_address} -oX -"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True)
        scan_results = parse_nmap_xml(result.stdout)
        return render_template('network.html', scan_results=scan_results)
    return render_template('network.html')