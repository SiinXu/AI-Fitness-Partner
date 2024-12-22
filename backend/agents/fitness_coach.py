from typing import Dict, List
import os
import requests
import json

class FitnessCoach:
    def __init__(self, model_config: Dict = None, api_key: str = None):
        self.model_config = model_config or {
            'temperature': 0.7,
            'max_tokens': 1000
        }
        self.api_key = api_key or os.getenv('MODELSCOPE_API_KEY')
        
    def create_workout_plan(self, user_data: Dict) -> Dict:
        """
        Creates a personalized workout plan
        
        Args:
            user_data: Dict containing user information and preferences
        """
        prompt = self._create_workout_prompt(user_data)
        
        try:
            if not self.api_key:
                return {
                    "workouts": [],
                    "recommendations": [],
                    "error": "Please configure your ModelScope API key."
                }
                
            # Get AI workout plan using ModelScope API
            url = "https://api-inference.modelscope.cn/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "Qwen/Qwen2.5-32B-Instruct",
                "messages": [
                    {"role": "system", "content": "You are an expert fitness coach creating personalized workout plans."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": self.model_config.get('temperature', 0.7),
                "max_tokens": self.model_config.get('max_tokens', 1000)
            }
            
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            if 'choices' in result and len(result['choices']) > 0:
                return self._parse_workout_plan(result['choices'][0]['message']['content'])
            else:
                return {
                    "workouts": [],
                    "recommendations": [],
                    "error": "Unable to generate workout plan at this time."
                }
                
        except Exception as e:
            print(f"Error creating workout plan: {str(e)}")
            return {
                "workouts": [],
                "recommendations": [],
                "error": "Unable to create workout plan at this time."
            }
            
    def analyze_workout_progress(self, workout_data: Dict) -> Dict:
        """
        Analyzes workout progress and provides feedback
        
        Args:
            workout_data: Dict containing workout tracking data
        """
        prompt = self._create_analysis_prompt(workout_data)
        
        try:
            if not self.api_key:
                return {
                    "analysis": "Please configure your ModelScope API key.",
                    "confidence": False
                }
                
            # Get AI analysis using ModelScope API
            url = "https://api-inference.modelscope.cn/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "Qwen/Qwen2.5-32B-Instruct",
                "messages": [
                    {"role": "system", "content": "You are a fitness analyst providing insights on workout performance."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": self.model_config.get('temperature', 0.7),
                "max_tokens": self.model_config.get('max_tokens', 1000)
            }
            
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            if 'choices' in result and len(result['choices']) > 0:
                return {
                    "analysis": result['choices'][0]['message']['content'],
                    "confidence": True
                }
            else:
                return {
                    "analysis": "Unable to analyze workout at this time.",
                    "confidence": False
                }
                
        except Exception as e:
            print(f"Error analyzing workout: {str(e)}")
            return {
                "analysis": "Unable to analyze workout at this time.",
                "confidence": False
            }
            
    def analyze_performance(self, workout_data: Dict) -> Dict:
        """
        Analyzes workout performance and provides feedback
        
        Args:
            workout_data: Dict containing workout metrics
        """
        prompt = self._create_performance_prompt(workout_data)
        
        try:
            if not self.api_key:
                return {
                    "feedback": "Please configure your ModelScope API key.",
                    "confidence": False
                }
                
            # Get AI feedback using ModelScope API
            url = "https://api-inference.modelscope.cn/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "Qwen/Qwen2.5-32B-Instruct",
                "messages": [
                    {"role": "system", "content": "You are a performance analyst providing real-time workout feedback."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": self.model_config.get('temperature', 0.7),
                "max_tokens": self.model_config.get('max_tokens', 1000)
            }
            
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            if 'choices' in result and len(result['choices']) > 0:
                return {
                    "feedback": result['choices'][0]['message']['content'],
                    "confidence": True
                }
            else:
                return {
                    "feedback": "Unable to analyze performance at this time.",
                    "confidence": False
                }
                
        except Exception as e:
            print(f"Error analyzing performance: {str(e)}")
            return {
                "feedback": "Unable to analyze performance at this time.",
                "confidence": False
            }
    
    def _create_workout_prompt(self, user_data: Dict) -> str:
        """Creates prompt for workout plan generation"""
        return f"""
        Please create a personalized workout plan based on:
        Goals: {user_data.get('goals', [])}
        Fitness Level: {user_data.get('fitness_level', 'beginner')}
        Available Equipment: {user_data.get('equipment', [])}
        Time Available: {user_data.get('time_available', '30')} minutes
        
        Please include:
        1. Warm-up routine
        2. Main exercises with sets and reps
        3. Cool-down routine
        4. Safety tips and form cues
        5. Progress tracking metrics
        """
        
    def _create_analysis_prompt(self, workout_data: Dict) -> str:
        """Creates prompt for workout analysis"""
        return f"""
        Please analyze the following workout data:
        Exercises: {workout_data.get('exercises', [])}
        Duration: {workout_data.get('duration', 0)} minutes
        Intensity: {workout_data.get('intensity', 'moderate')}
        Heart Rate: {workout_data.get('heart_rate', [])}
        
        Please provide:
        1. Overall performance assessment
        2. Areas of improvement
        3. Recovery recommendations
        4. Progress indicators
        """
        
    def _create_performance_prompt(self, workout_data: Dict) -> str:
        """Creates prompt for performance analysis"""
        return f"""
        Please analyze the current workout performance:
        Exercise: {workout_data.get('current_exercise', '')}
        Set: {workout_data.get('current_set', 1)}
        Reps: {workout_data.get('reps', 0)}
        Form Score: {workout_data.get('form_score', 0)}
        Heart Rate: {workout_data.get('heart_rate', 0)}
        
        Please provide:
        1. Real-time form feedback
        2. Intensity adjustment recommendations
        3. Safety alerts if necessary
        4. Encouragement and motivation
        """
        
    def _parse_workout_plan(self, response_text: str) -> Dict:
        """Parses the workout plan response into structured data"""
        try:
            # Split response into sections
            sections = response_text.split('\n\n')
            
            workouts = []
            recommendations = []
            
            current_section = None
            for section in sections:
                if section.lower().startswith('warm-up'):
                    current_section = 'warm_up'
                    workouts.append({
                        'type': 'warm_up',
                        'exercises': []
                    })
                elif section.lower().startswith('main'):
                    current_section = 'main'
                    workouts.append({
                        'type': 'main',
                        'exercises': []
                    })
                elif section.lower().startswith('cool-down'):
                    current_section = 'cool_down'
                    workouts.append({
                        'type': 'cool_down',
                        'exercises': []
                    })
                elif section.lower().startswith(('tip', 'recommend', 'note')):
                    recommendations.append(section.strip())
                elif current_section and section.strip():
                    # Add exercises to current section
                    for line in section.split('\n'):
                        if line.strip():
                            workouts[-1]['exercises'].append(line.strip())
            
            return {
                'workouts': workouts,
                'recommendations': recommendations,
                'error': None
            }
            
        except Exception as e:
            print(f"Error parsing workout plan: {str(e)}")
            return {
                'workouts': [],
                'recommendations': [],
                'error': 'Unable to parse workout plan'
            }

def main():
    """Test the FitnessCoach class"""
    print("Testing FitnessCoach...")
    
    # Create an instance with default config
    coach = FitnessCoach()
    
    # Test workout plan creation
    user_data = {
        'goals': ['weight loss', 'muscle tone'],
        'fitness_level': 'intermediate',
        'equipment': ['dumbbells', 'resistance bands'],
        'time_available': 45
    }
    
    plan = coach.create_workout_plan(user_data)
    print("\nWorkout Plan:")
    print(json.dumps(plan, indent=2))
    
    # Test workout analysis
    workout_data = {
        'exercises': ['squats', 'pushups', 'planks'],
        'duration': 40,
        'intensity': 'high',
        'heart_rate': [120, 140, 160, 150, 130]
    }
    
    analysis = coach.analyze_workout_progress(workout_data)
    print("\nWorkout Analysis:")
    print(json.dumps(analysis, indent=2))
    
    # Test performance analysis
    performance_data = {
        'current_exercise': 'squats',
        'current_set': 2,
        'reps': 12,
        'form_score': 85,
        'heart_rate': 145
    }
    
    feedback = coach.analyze_performance(performance_data)
    print("\nPerformance Feedback:")
    print(json.dumps(feedback, indent=2))

if __name__ == '__main__':
    main()
