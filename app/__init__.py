from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('postgres://ub66kl0nhdc9hb:p8822129e06a098fc12d0a9f1ed8d3dfedf93928144517a21abd4a3daf98b70ba@cb5ajfjosdpmil.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/dabhal8574i1h0')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'melong'  
    
    
    db.init_app(app)
    
    migrate = Migrate(app, db)

    from .routes import configure_routes
    configure_routes(app)

    return app