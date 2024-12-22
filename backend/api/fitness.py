from flask import Blueprint, request, jsonify, current_app
from functools import wraps
import jwt
from backend.models.user import User
from backend.services.fitness_plan import FitnessPlanService
from backend.services.agent_manager import AgentManager
import os
from werkzeug.utils import secure_filename

def init_fitness_bp():
    fitness_bp = Blueprint('fitness', __name__, url_prefix='/api/fitness')
    fitness_service = None
    agent_manager = None

    def get_fitness_service():
        nonlocal fitness_service
        if fitness_service is None:
            fitness_service = FitnessPlanService()
        return fitness_service

    def get_agent_manager():
        nonlocal agent_manager
        if agent_manager is None:
            agent_manager = AgentManager()
        return agent_manager

    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split(' ')[1]
            
            if not token:
                return jsonify({'message': 'Token is missing'}), 401
            
            try:
                data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
                current_user = User.query.filter_by(id=data['user_id']).first()
            except:
                return jsonify({'message': 'Token is invalid'}), 401
            
            return f(current_user, *args, **kwargs)
        return decorated

    @fitness_bp.route('/plan', methods=['POST'])
    @token_required
    def create_fitness_plan(current_user):
        """Create a personalized fitness plan."""
        try:
            data = request.get_json()
            service = get_fitness_service()
            plan = service.create_fitness_plan(current_user.id, data)
            return jsonify(plan), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @fitness_bp.route('/workout', methods=['POST'])
    @token_required
    def log_workout(current_user):
        data = request.get_json()
        
        workout = Workout(
            user_id=current_user.id,
            type=data['type'],
            duration=data['duration'],
            exercises=data['exercises'],
            notes=data.get('notes', '')
        )
        
        workout.save()
        
        # Get AI feedback
        feedback = get_agent_manager().get_workout_feedback(workout)
        
        return jsonify({
            'workout': workout.to_dict(),
            'feedback': feedback
        })

    @fitness_bp.route('/workouts', methods=['GET'])
    @token_required
    def get_workouts(current_user):
        user_id = current_user.id
        
        workouts = Workout.query.filter_by(user_id=user_id).all()
        return jsonify([w.to_dict() for w in workouts])

    @fitness_bp.route('/progress', methods=['GET'])
    @token_required
    def get_progress(current_user):
        """Get user's fitness progress."""
        try:
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')
            
            if not start_date or not end_date:
                return jsonify({'error': 'Start date and end date are required'}), 400
                
            progress = get_fitness_service().calculate_progress(
                current_user.id,
                start_date,
                end_date
            )
            return jsonify(progress), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @fitness_bp.route('/recommendations', methods=['GET'])
    @token_required
    def get_recommendations(current_user):
        user = current_user
        
        recommendations = get_agent_manager().get_recommendations(user)
        return jsonify(recommendations)

    @fitness_bp.route('/stats', methods=['GET'])
    @token_required
    def get_stats(current_user):
        """Get user's fitness statistics."""
        try:
            # Get basic stats
            stats = {
                'totalWorkouts': 0,  # Implement actual stats
                'activeMinutes': 0,
                'currentStreak': 0
            }
            return jsonify(stats), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @fitness_bp.route('/goals', methods=['GET', 'POST'])
    @token_required
    def handle_fitness_goals(current_user):
        """Handle fitness goals endpoints."""
        try:
            if request.method == 'GET':
                # Get user's fitness goals
                user = current_user
                if not user:
                    return jsonify({'error': 'User not found'}), 404
                
                return jsonify(user.fitness_goals or {}), 200
                
            elif request.method == 'POST':
                # Update user's fitness goals
                data = request.get_json()
                if not data:
                    return jsonify({'error': 'No data provided'}), 400
                    
                user = current_user
                if not user:
                    return jsonify({'error': 'User not found'}), 404
                    
                # Update user's fitness goals
                user.fitness_goals = data
                user.save()
                
                # Generate personalized plan based on new goals
                plan = get_fitness_service().create_fitness_plan(user.id, data)
                
                return jsonify({
                    'message': 'Fitness goals updated successfully',
                    'goals': data,
                    'plan': plan
                }), 200
                
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @fitness_bp.route('/knowledge', methods=['POST'])
    @token_required
    def upload_knowledge(current_user):
        """Upload files to knowledge base."""
        try:
            if 'files' not in request.files:
                return jsonify({'error': 'No files provided'}), 400
                
            files = request.files.getlist('files')
            category = request.form.get('category')
            
            if not category:
                return jsonify({'error': 'Category is required'}), 400
                
            # Process and store files
            stored_files = []
            for file in files:
                if file.filename:
                    # Save file and process for RAG
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], category, filename)
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                    file.save(filepath)
                    
                    # Process file for RAG (implement this in a service)
                    get_agent_manager().process_knowledge_file(filepath, category)
                    
                    stored_files.append(filename)
            
            return jsonify({
                'message': 'Files uploaded successfully',
                'files': stored_files
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @fitness_bp.route('/voice', methods=['POST'])
    @token_required
    def handle_voice_command(current_user):
        """Handle voice commands using Fish Audio."""
        try:
            if 'audio' not in request.files:
                return jsonify({'error': 'No audio file provided'}), 400
                
            audio_file = request.files['audio']
            
            # Process audio using Fish Audio service
            text = get_agent_manager().process_audio(audio_file)
            
            # Process the command
            response = get_agent_manager().process_voice_command(text, current_user.id)
            
            # Generate audio response
            audio_response = get_agent_manager().generate_voice_response(response)
            
            return jsonify({
                'text': response,
                'audio': audio_response
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return fitness_bp
