from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import bcrypt

db = SQLAlchemy()
migrate = Migrate()

# Import models here to ensure they are registered with SQLAlchemy
from .user import User
from .workout import Workout

def init_db(app):
    """Initialize the database with the app context."""
    db.init_app(app)
    migrate.init_app(app, db)
    
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Create a test user if it doesn't exist
        try:
            test_user = User.query.filter_by(username='test@example.com').first()
            if not test_user:
                # Create password hash
                password = 'test123'
                salt = bcrypt.gensalt()
                password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
                
                test_user = User(
                    username='test@example.com',
                    email='test@example.com',
                    password=password_hash,
                    fitness_level='intermediate'
                )
                db.session.add(test_user)
                db.session.commit()  # 确保更改被提交
        except Exception as e:
            print(f"Error creating test user: {str(e)}")
            # Continue even if there's an error, as tables might not exist yet
