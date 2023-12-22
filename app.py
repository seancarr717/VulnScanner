#imports for requests and flask api stuff
from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)
#set where zap is hosted and your api key ,accessible at tools>options api
ZAP_API_URL = "http://localhost:9090"
ZAP_API_KEY = "hmfds6d8j8mqqlc61tqjgvfaqq"

#route for rendering the index.html file as the default page
@app.route('/')
def home():
    return render_template('index.html')

#route for starting scan in zap api
@app.route('/start_spider', methods=['POST'])
def start_spider():
    return start_zap_scan(request, 'spider')


#start zap spider scan which gets all the info from the html whihc is sent over 
def start_zap_scan(request, scan_type):
    data = request.get_json()
    target_url = data.get('url')
    
    #specifies zap endpoint to send to with supplied api key and url
    if scan_type == 'spider':
        zap_endpoint = f"{ZAP_API_URL}/JSON/spider/action/scan/?apikey={ZAP_API_KEY}&url={target_url}"



#runs the app when flask app is ran with debug on
if __name__ == '__main__':
    app.run(debug=True)