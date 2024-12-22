from typing import Dict, List
import openai
from datetime import datetime, timedelta
import random

class Motivator:
    def __init__(self, model_config: Dict):
        self.model_config = model_config
        
    async def generate_motivation(self, user_profile: Dict, progress_data: Dict) -> Dict:
        """
        Generates personalized motivational messages based on user's progress
        
        Args:
            user_profile: Dict containing user information
            progress_data: Dict containing progress metrics
        """
        prompt = self._create_motivation_prompt(user_profile, progress_data)
        
        try:
            response = await openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an inspiring fitness motivator who provides personalized encouragement."},
                    {"role": "user", "content": prompt}
                ],
                **self.model_config
            )
            return {
                "message": response.choices[0].message.content,
                "type": "progress_based",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error generating motivation: {str(e)}")
            return None

    async def create_challenge(self, user_level: str, preferences: List[str]) -> Dict:
        """
        Creates a personalized fitness challenge
        
        Args:
            user_level: Fitness level of the user
            preferences: List of preferred activities
        """
        prompt = self._create_challenge_prompt(user_level, preferences)
        
        try:
            response = await openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a fitness challenge creator specializing in engaging and achievable goals."},
                    {"role": "user", "content": prompt}
                ],
                **self.model_config
            )
            return self._parse_challenge(response.choices[0].message.content)
        except Exception as e:
            print(f"Error creating challenge: {str(e)}")
            return None

    def track_consistency(self, workout_history: List[Dict]) -> Dict:
        """
        Tracks workout consistency and provides encouragement
        
        Args:
            workout_history: List of past workouts
        """
        streak = self._calculate_streak(workout_history)
        consistency_score = self._calculate_consistency_score(workout_history)
        
        return {
            "current_streak": streak,
            "consistency_score": consistency_score,
            "encouragement": self._generate_streak_message(streak),
            "timestamp": datetime.now().isoformat()
        }

    def get_daily_quote(self) -> Dict:
        """Returns an inspiring fitness quote"""
        quotes = [
            "The only bad workout is the one that didn't happen.",
            "Your body can stand almost anything. It's your mind you have to convince.",
            "The hard days are what make you stronger.",
            "Fitness is not about being better than someone else. It's about being better than you used to be.",
            "The only person you are destined to become is the person you decide to be.",
            "Success is usually the culmination of controlling failure.",
            "The difference between try and triumph is just a little umph!",
            "The only way to define your limits is by going beyond them.",
            "Don't wish for it, work for it.",
            "Your health is an investment, not an expense."
        ]
        
        return {
            "quote": random.choice(quotes),
            "timestamp": datetime.now().isoformat()
        }

    def _create_motivation_prompt(self, user_profile: Dict, progress_data: Dict) -> str:
        """Creates a personalized motivation prompt"""
        return f"""
        Generate a motivational message for someone who:
        - Has been working out for {progress_data.get('weeks_active', 0)} weeks
        - Has achieved {progress_data.get('goals_achieved', 0)} goals
        - Current goal: {user_profile.get('current_goal')}
        - Recent milestone: {progress_data.get('recent_milestone')}
        - Preferred motivation style: {user_profile.get('motivation_style', 'encouraging')}
        """

    def _create_challenge_prompt(self, user_level: str, preferences: List[str]) -> str:
        """Creates a prompt for challenge generation"""
        return f"""
        Create a 7-day fitness challenge for a {user_level} level user who enjoys:
        {', '.join(preferences)}
        
        The challenge should be:
        1. Progressive in difficulty
        2. Achievable yet challenging
        3. Include rest days
        4. Incorporate preferred activities
        """

    def _parse_challenge(self, response: str) -> Dict:
        """Parses AI response into structured challenge"""
        return {
            "challenge": response,
            "duration": "7 days",
            "start_date": datetime.now().isoformat(),
            "end_date": (datetime.now() + timedelta(days=7)).isoformat()
        }

    def _calculate_streak(self, workout_history: List[Dict]) -> int:
        """Calculates current workout streak"""
        if not workout_history:
            return 0
            
        streak = 0
        today = datetime.now().date()
        
        for workout in reversed(workout_history):
            workout_date = datetime.fromisoformat(workout['date']).date()
            days_diff = (today - workout_date).days
            
            if days_diff == streak:
                streak += 1
            else:
                break
                
        return streak

    def _calculate_consistency_score(self, workout_history: List[Dict]) -> float:
        """Calculates consistency score (0-100)"""
        if not workout_history:
            return 0
            
        # Look at last 30 days
        today = datetime.now().date()
        thirty_days_ago = today - timedelta(days=30)
        
        # Count workouts in last 30 days
        recent_workouts = [
            w for w in workout_history 
            if datetime.fromisoformat(w['date']).date() >= thirty_days_ago
        ]
        
        # Calculate score (assuming 4 workouts per week is ideal)
        ideal_workouts = 17  # ~4 workouts/week for 30 days
        actual_workouts = len(recent_workouts)
        
        score = (actual_workouts / ideal_workouts) * 100
        return min(100, round(score, 1))

    def _generate_streak_message(self, streak: int) -> str:
        """Generates encouraging message based on streak"""
        if streak == 0:
            return "Ready to start your fitness journey? Let's build that streak!"
        elif streak < 3:
            return f"Great start! You're on a {streak}-day streak. Keep it going!"
        elif streak < 7:
            return f"Amazing! {streak} days in a row. You're building strong habits!"
        elif streak < 14:
            return f"Incredible discipline! {streak}-day streak. You're unstoppable!"
        else:
            return f"You're a machine! {streak}-day streak. This is legendary!"
