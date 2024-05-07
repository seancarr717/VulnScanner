from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Welcome181@database-2.cdco2ayo4wwh.eu-north-1.rds.amazonaws.com:5432'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
    
    
    db.init_app(app)
    
    migrate = Migrate(app, db)

    from .routes import configure_routes
    configure_routes(app)

    return app
