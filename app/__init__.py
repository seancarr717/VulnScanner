from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os
db = SQLAlchemy()
#import db and create app then configure routes and serve app to wsgi
def create_app(): 
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Welcome181@database-2.cdco2ayo4wwh.eu-north-1.rds.amazonaws.com:5432'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    
    db.init_app(app)
    

    from .routes import configure_routes
    configure_routes(app)

    return app
