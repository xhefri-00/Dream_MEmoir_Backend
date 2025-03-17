from flask import Flask, request
from extensions import db, jwt
from routes.auth_routes import auth_bp
from routes.blog_routes import blog_bp
from routes.bookmark_routes import bookmark_bp
from flask_cors import CORS
from flask_talisman import Talisman


def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask application instance.
    """
    app = Flask(__name__)
    Talisman(app, content_security_policy=None)
    CORS(app, resources={r"/*": {"origins": "https://dream-me-moir.vercel.app"}}, 
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], 
     allow_headers=["Content-Type", "Authorization"], 
     supports_credentials=True)
    app.config.from_object("config.Config")

    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "https://dream-me-moir.vercel.app"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        print("CORS Headers Added") 
        return response

    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            response = Flask.response_class()
            response.headers["Access-Control-Allow-Origin"] = "https://dream-me-moir.vercel.app"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.status_code = 200
            return response

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(blog_bp, url_prefix="/blogs")
    app.register_blueprint(bookmark_bp, url_prefix="/bookmarks")

    # Define home route
    @app.route('/')
    def home():
        return "Greet thee in this realm known as Dream MEmoir!"

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0",port=4000,debug=True)