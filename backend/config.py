import os

# Flask configuration
os.environ['FLASK_APP'] = 'backend/app.py'
os.environ['FLASK_ENV'] = 'development'

# Database configuration
os.environ['DATABASE_URL'] = 'postgresql://localhost/fitness_partner'

# JWT configuration
os.environ['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this in production

# API Keys (these should be set by the user)
os.environ['MODELSCOPE_API_KEY'] = ''
os.environ['FISH_AUDIO_API_KEY'] = ''
