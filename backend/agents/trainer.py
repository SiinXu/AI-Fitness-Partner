from typing import Dict, List
import openai
from datetime import datetime, timedelta

class Trainer:
    def __init__(self, model_config: Dict):
        self.model_config = model_config
        
    async def create_training_session(self, user_profile: Dict, fitness_goals: List[str]) -> Dict:
        """
        Creates a personalized training session
        
        Args:
            user_profile: Dict containing user information
            fitness_goals: List of fitness goals
        """
        prompt = self._create_training_prompt(user_profile, fitness_goals)
        
        try:
            response = await openai.ChatCompletion.create(
                messages=[
                    {"role": "system", "content": "You are an expert personal trainer creating customized workout sessions."},
                    {"role": "user", "content": prompt}
                ],
                **self.model_config
            )
            return self._parse_training_session(response.choices[0].message.content)
        except Exception as e:
            print(f"Error creating training session: {str(e)}")
            return None

    async def provide_real_time_feedback(self, exercise_data: Dict) -> Dict:
        """
        Provides real-time feedback during exercises
        
        Args:
            exercise_data: Dict containing exercise metrics and form data
        """
        prompt = self._create_feedback_prompt(exercise_data)
        
        try:
            response = await openai.ChatCompletion.create(
                messages=[
                    {"role": "system", "content": "You are a real-time exercise form coach providing immediate feedback."},
                    {"role": "user", "content": prompt}
                ],
                **self.model_config
            )
            return {
                "feedback": response.choices[0].message.content,
                "exercise": exercise_data.get("name"),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error providing feedback: {str(e)}")
            return None

    def track_exercise_progress(self, exercise_history: List[Dict]) -> Dict:
        """
        Tracks progress for specific exercises
        
        Args:
            exercise_history: List of exercise records
        """
        progress = {}
        for exercise in exercise_history:
            name = exercise.get("name")
            if name not in progress:
                progress[name] = {
                    "max_weight": 0,
                    "max_reps": 0,
                    "total_volume": 0,
                    "progression": []
                }
            
            # Update exercise stats
            weight = exercise.get("weight", 0)
            reps = exercise.get("reps", 0)
            volume = weight * reps
            
            progress[name]["max_weight"] = max(progress[name]["max_weight"], weight)
            progress[name]["max_reps"] = max(progress[name]["max_reps"], reps)
            progress[name]["total_volume"] += volume
            progress[name]["progression"].append({
                "date": exercise.get("date"),
                "weight": weight,
                "reps": reps,
                "volume": volume
            })
        
        return {
            "exercise_progress": progress,
            "recommendations": self._generate_progression_recommendations(progress),
            "timestamp": datetime.now().isoformat()
        }

    def calculate_training_load(self, recent_workouts: List[Dict]) -> Dict:
        """
        Calculates training load and suggests recovery needs
        
        Args:
            recent_workouts: List of recent workout sessions
        """
        acute_load = self._calculate_acute_load(recent_workouts)
        chronic_load = self._calculate_chronic_load(recent_workouts)
        
        if chronic_load > 0:
            acwr = acute_load / chronic_load  # Acute:Chronic Workload Ratio
        else:
            acwr = 1.0
        
        return {
            "acute_load": acute_load,
            "chronic_load": chronic_load,
            "acwr": round(acwr, 2),
            "status": self._determine_training_status(acwr),
            "recommendations": self._generate_load_recommendations(acwr),
            "timestamp": datetime.now().isoformat()
        }

    def _create_training_prompt(self, user_profile: Dict, fitness_goals: List[str]) -> str:
        """Creates prompt for training session generation"""
        return f"""
        Create a training session for someone who:
        - Fitness level: {user_profile.get('fitness_level', 'beginner')}
        - Goals: {', '.join(fitness_goals)}
        - Available equipment: {user_profile.get('equipment', [])}
        - Time available: {user_profile.get('session_duration', 60)} minutes
        - Injuries/limitations: {user_profile.get('limitations', [])}
        - Preferred training style: {user_profile.get('training_style', 'balanced')}
        """

    def _create_feedback_prompt(self, exercise_data: Dict) -> str:
        """Creates prompt for real-time exercise feedback"""
        return f"""
        Provide form feedback for {exercise_data.get('name')} exercise:
        - Current form metrics: {exercise_data.get('form_metrics', {})}
        - Movement pattern: {exercise_data.get('movement_pattern')}
        - Weight used: {exercise_data.get('weight')} kg
        - Rep speed: {exercise_data.get('rep_speed')}
        """

    def _parse_training_session(self, response: str) -> Dict:
        """Parses AI response into structured training session"""
        return {
            "workout": response,
            "created_at": datetime.now().isoformat(),
            "estimated_duration": "60 minutes",  # Default duration
            "difficulty": "intermediate"  # Default difficulty
        }

    def _generate_progression_recommendations(self, progress: Dict) -> List[str]:
        """Generates exercise progression recommendations"""
        recommendations = []
        
        for exercise, data in progress.items():
            if len(data["progression"]) >= 2:
                # Compare last two sessions
                last = data["progression"][-1]
                previous = data["progression"][-2]
                
                if last["volume"] <= previous["volume"]:
                    recommendations.append(f"Consider increasing volume for {exercise}")
                if len(data["progression"]) >= 4:
                    recommendations.append(f"Time to reassess {exercise} max weight")
                    
        return recommendations

    def _calculate_acute_load(self, workouts: List[Dict], days: int = 7) -> float:
        """Calculates acute training load (last 7 days)"""
        recent_workouts = [
            w for w in workouts 
            if datetime.fromisoformat(w['date']) > datetime.now() - timedelta(days=days)
        ]
        
        return sum(w.get('load', 0) for w in recent_workouts)

    def _calculate_chronic_load(self, workouts: List[Dict], weeks: int = 4) -> float:
        """Calculates chronic training load (last 4 weeks)"""
        recent_workouts = [
            w for w in workouts 
            if datetime.fromisoformat(w['date']) > datetime.now() - timedelta(weeks=weeks)
        ]
        
        if not recent_workouts:
            return 0
            
        return sum(w.get('load', 0) for w in recent_workouts) / weeks

    def _determine_training_status(self, acwr: float) -> str:
        """Determines training status based on Acute:Chronic Workload Ratio"""
        if acwr < 0.8:
            return "undertraining"
        elif 0.8 <= acwr <= 1.3:
            return "optimal"
        elif 1.3 < acwr <= 1.5:
            return "high_risk"
        else:
            return "very_high_risk"

    def _generate_load_recommendations(self, acwr: float) -> List[str]:
        """Generates recommendations based on training load"""
        if acwr < 0.8:
            return [
                "Gradually increase training volume",
                "Add one extra session this week",
                "Increase intensity in current sessions"
            ]
        elif 0.8 <= acwr <= 1.3:
            return [
                "Maintain current training load",
                "Focus on quality of sessions",
                "Monitor recovery markers"
            ]
        else:
            return [
                "Reduce training volume",
                "Include extra recovery sessions",
                "Focus on technique and form",
                "Consider a deload week"
            ]
