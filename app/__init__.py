from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key_here'

    # Import routes configuration
    from .routes import configure_routes
    configure_routes(app)

    return app

app = create_app()