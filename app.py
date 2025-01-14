from flask import Flask
from extensions import db, jwt
from routes.auth_routes import auth_bp
from routes.blog_routes import blog_bp
from routes.bookmark_routes import bookmark_bp
from flask_cors import CORS


def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object("config.Config")
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(blog_bp)
    app.register_blueprint(bookmark_bp, url_prefix="/bookmarks")

    # Define home route
    @app.route('/')
    def home():
        return "Greet thee in this realm known as Dream MEmoir!"

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0",port=4000,debug=True)
