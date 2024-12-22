from typing import Dict, List
import openai
from datetime import datetime

class Nutritionist:
    def __init__(self, model_config: Dict):
        self.model_config = model_config
        
    async def create_meal_plan(self, user_profile: Dict, fitness_goals: List[str]) -> Dict:
        """
        Creates a personalized meal plan based on user profile and fitness goals
        
        Args:
            user_profile: Dict containing user information
            fitness_goals: List of fitness goals
        """
        prompt = self._create_meal_plan_prompt(user_profile, fitness_goals)
        
        try:
            response = await openai.ChatCompletion.create(
                messages=[
                    {"role": "system", "content": "You are an expert nutritionist specializing in sports nutrition and meal planning."},
                    {"role": "user", "content": prompt}
                ],
                **self.model_config
            )
            return self._parse_meal_plan(response.choices[0].message.content)
        except Exception as e:
            print(f"Error creating meal plan: {str(e)}")
            return None

    async def analyze_diet(self, food_log: List[Dict]) -> Dict:
        """
        Analyzes food intake and provides nutritional insights
        
        Args:
            food_log: List of food items consumed
        """
        total_nutrients = self._calculate_total_nutrients(food_log)
        prompt = self._create_diet_analysis_prompt(food_log, total_nutrients)
        
        try:
            response = await openai.ChatCompletion.create(
                messages=[
                    {"role": "system", "content": "You are a nutrition analyst specializing in dietary assessment."},
                    {"role": "user", "content": prompt}
                ],
                **self.model_config
            )
            return {
                "analysis": response.choices[0].message.content,
                "total_nutrients": total_nutrients,
                "recommendations": self._generate_diet_recommendations(total_nutrients),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error analyzing diet: {str(e)}")
            return None

    def calculate_macros(self, user_profile: Dict, activity_level: str) -> Dict:
        """
        Calculates recommended macronutrient ratios
        
        Args:
            user_profile: Dict containing user information
            activity_level: String indicating activity level
        """
        # Calculate BMR using Harris-Benedict equation
        bmr = self._calculate_bmr(user_profile)
        
        # Calculate TDEE (Total Daily Energy Expenditure)
        tdee = self._calculate_tdee(bmr, activity_level)
        
        # Calculate macros based on goals
        macros = self._calculate_macro_split(tdee, user_profile.get('goal', 'maintenance'))
        
        return {
            "daily_calories": tdee,
            "macros": macros,
            "timestamp": datetime.now().isoformat()
        }

    def _create_meal_plan_prompt(self, user_profile: Dict, fitness_goals: List[str]) -> str:
        """Creates a detailed prompt for meal planning"""
        return f"""
        Create a personalized meal plan considering:
        - Age: {user_profile.get('age')}
        - Weight: {user_profile.get('weight')} kg
        - Height: {user_profile.get('height')} cm
        - Dietary restrictions: {user_profile.get('dietary_restrictions', [])}
        - Fitness goals: {fitness_goals}
        - Allergies: {user_profile.get('allergies', [])}
        - Preferred cuisines: {user_profile.get('preferred_cuisines', [])}
        """

    def _parse_meal_plan(self, response: str) -> Dict:
        """Parses AI response into structured meal plan"""
        return {
            "meal_plan": response,
            "created_at": datetime.now().isoformat(),
            "duration": "7 days"  # Default duration
        }

    def _calculate_total_nutrients(self, food_log: List[Dict]) -> Dict:
        """Calculates total nutrients from food log"""
        totals = {
            "calories": 0,
            "protein": 0,
            "carbs": 0,
            "fat": 0,
            "fiber": 0
        }
        
        for food in food_log:
            totals["calories"] += food.get("calories", 0)
            totals["protein"] += food.get("protein", 0)
            totals["carbs"] += food.get("carbs", 0)
            totals["fat"] += food.get("fat", 0)
            totals["fiber"] += food.get("fiber", 0)
            
        return totals

    def _create_diet_analysis_prompt(self, food_log: List[Dict], total_nutrients: Dict) -> str:
        """Creates prompt for diet analysis"""
        return f"""
        Analyze the following daily food intake:
        - Total Calories: {total_nutrients['calories']}
        - Protein: {total_nutrients['protein']}g
        - Carbohydrates: {total_nutrients['carbs']}g
        - Fat: {total_nutrients['fat']}g
        - Fiber: {total_nutrients['fiber']}g

        Food items consumed:
        {', '.join(food['name'] for food in food_log)}
        """

    def _generate_diet_recommendations(self, nutrients: Dict) -> List[str]:
        """Generates dietary recommendations based on nutrient intake"""
        recommendations = []
        
        if nutrients["protein"] < 50:
            recommendations.append("Increase protein intake")
        if nutrients["fiber"] < 25:
            recommendations.append("Add more fiber-rich foods")
        if nutrients["fat"] > 70:
            recommendations.append("Reduce fat intake")
            
        return recommendations

    def _calculate_bmr(self, user_profile: Dict) -> float:
        """Calculates Basal Metabolic Rate using Harris-Benedict equation"""
        weight = user_profile.get('weight', 0)  # in kg
        height = user_profile.get('height', 0)  # in cm
        age = user_profile.get('age', 0)
        gender = user_profile.get('gender', 'male')
        
        if gender.lower() == 'male':
            return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else:
            return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

    def _calculate_tdee(self, bmr: float, activity_level: str) -> int:
        """Calculates Total Daily Energy Expenditure"""
        activity_multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'very_active': 1.725,
            'extra_active': 1.9
        }
        
        multiplier = activity_multipliers.get(activity_level.lower(), 1.2)
        return int(bmr * multiplier)

    def _calculate_macro_split(self, tdee: int, goal: str) -> Dict:
        """Calculates macronutrient split based on goals"""
        if goal == 'muscle_gain':
            protein_ratio = 0.3
            fat_ratio = 0.25
            carb_ratio = 0.45
        elif goal == 'fat_loss':
            protein_ratio = 0.4
            fat_ratio = 0.3
            carb_ratio = 0.3
        else:  # maintenance
            protein_ratio = 0.3
            fat_ratio = 0.3
            carb_ratio = 0.4
            
        return {
            "protein": int((tdee * protein_ratio) / 4),  # 4 calories per gram
            "fat": int((tdee * fat_ratio) / 9),  # 9 calories per gram
            "carbs": int((tdee * carb_ratio) / 4)  # 4 calories per gram
        }
