from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import re

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    

# Adjust the URI for SQLAlchemy 1.4+ compatibility
    uri = os.getenv('DATABASE_URL', 'postgresql://postgres:Welcome181@localhost/postgres')
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = uri
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SECRET_KEY'] = 'melong'  
    
    db.init_app(app)
    
    migrate = Migrate(app, db)

    from .routes import configure_routes
    configure_routes(app)

    return app