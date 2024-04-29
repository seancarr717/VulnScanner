#imports for requests and flask api stuff
from flask import Flask, request, jsonify, render_template,redirect,url_for
import requests

app = Flask(__name__)
#set where zap is hosted and your api key ,accessible at tools>options api
ZAP_API_URL = "http://localhost:9090"
ZAP_API_KEY = "im496jdnidj3mor1jt24kpgi2k"




#route for rendering the index.html file as the default page
@app.route('/')
def home():
    return render_template('index.html')

#route for  login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    return render_template('login.html')

@app.route('/network')
def network():
    return render_template('network.html')

#route for starting spider  scan in zap api
@app.route('/start_spider', methods=['POST'])
def start_spider():
    return start_zap_scan(request, 'spider')
#route for starting active scan in zap api
@app.route('/start_active_scan', methods=['POST'])
def start_active_scan():
    return start_zap_scan(request, 'ascan')



#start zap spider scan which gets all the info from the html whihc is sent over 
def start_zap_scan(request, scan_type):
    data = request.get_json()
    target_url = data.get('url')
    #gives 400 response if no url given
    if not target_url:
        return jsonify({"error": "URL is required"}), 400
    
    #specifies zap endpoint to send to with supplied api key and url
    if scan_type == 'spider':
        zap_endpoint = f"{ZAP_API_URL}/JSON/spider/action/scan/?apikey={ZAP_API_KEY}&url={target_url}"
    else:
        zap_endpoint= f"{ZAP_API_URL}/JSON/ascan/action/scan/?apikey={ZAP_API_KEY}&url={target_url}"
    
    #gets response from zap 
    response = requests.get(zap_endpoint)
    #sets scan id as the response from zap if we get a 200 http request otherwise nothing else 
    scan_id = response.json().get('scan') if response.status_code == 200 else None
    #returns message to frontend through jsonify with scan id and the type
    return jsonify({"message": f"{scan_type.capitalize()} scan started", "scan_id": scan_id})


#runs the app when flask app is ran with debug on
if __name__ == '__main__':
    app.run(debug=True)