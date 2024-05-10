#import db and hashing
from . import db  
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    #sets and rreturns hash of password in db
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class NetworkScan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Reference to the User model
    ip_address = db.Column(db.String(15), nullable=False)
    xml_data = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<NetworkScan {self.ip_address}>'
    
class ScanResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scan_id = db.Column(db.String(128), nullable=False)  # Unique identifier for the scan
    scan_type = db.Column(db.String(50), nullable=False)  # Type of scan ('spider', 'ascan', etc.)
    status = db.Column(db.String(50), nullable=False, default='started')  # Status of the scan
    results = db.Column(db.Text, nullable=True)  # JSON string of results
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('scan_results', lazy=True))

    def __repr__(self):
        return f'<ScanResult {self.scan_type} {self.scan_id} by User {self.user_id}>'