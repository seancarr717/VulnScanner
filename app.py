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



#runs the app when flask app is ran with debug on
if __name__ == '__main__':
    app.run(debug=True)