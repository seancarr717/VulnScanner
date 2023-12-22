from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

ZAP_API_URL = "http://localhost:8080"  # Change this if your ZAP instance is hosted elsewhere
ZAP_API_KEY = "hmfds6d8j8mqqlc61tqjgvfaqq"       # Replace with your actual ZAP API key

