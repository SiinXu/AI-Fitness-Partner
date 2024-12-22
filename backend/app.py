from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

from backend.models import db, migrate
from backend.api.auth import auth_bp
from backend.api.fitness import init_fitness_bp

def create_app():
    # Load environment variables
    load_dotenv()
    
    # Initialize Flask app
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:5002"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "Accept", "Origin", "X-Requested-With"],
            "expose_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True,
            "max_age": 3600,
            "send_wildcard": False,
            "vary_header": True
        }
    })
    
    # Configure database
    db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fitness.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    
    # Initialize database and migrations
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    # Initialize and register fitness blueprint
    fitness_bp = init_fitness_bp()
    app.register_blueprint(fitness_bp, url_prefix='/api/fitness')
    
    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}, 200
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
