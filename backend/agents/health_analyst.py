from typing import Dict, List
from datetime import datetime, timedelta

class HealthAnalyst:
    def __init__(self, model_config: Dict):
        self.model_config = model_config
        
    def analyze_health_metrics(self, metrics: Dict) -> Dict:
        """
        Analyzes health metrics and provides insights
        
        Args:
            metrics: Dict containing health metrics
        """
        prompt = self._create_analysis_prompt(metrics)
        
        try:
            response = openai.ChatCompletion.create(
                messages=[
                    {"role": "system", "content": "You are a health analyst providing insights on fitness and wellness metrics."},
                    {"role": "user", "content": prompt}
                ],
                **self.model_config
            )
            return {
                "analysis": response.choices[0].message.content,
                "confidence": response.choices[0].finish_reason == "stop"
            }
        except Exception as e:
            print(f"Error analyzing health metrics: {str(e)}")
            return {
                "analysis": "Unable to analyze health metrics at this time.",
                "confidence": False
            }
            
    def analyze_health_progress(self, progress_data: Dict) -> Dict:
        """
        Analyzes health progress over time
        
        Args:
            progress_data: Dict containing historical health data
        """
        prompt = self._create_progress_prompt(progress_data)
        
        try:
            response = openai.ChatCompletion.create(
                messages=[
                    {"role": "system", "content": "You are a health progress analyst providing insights on fitness improvements."},
                    {"role": "user", "content": prompt}
                ],
                **self.model_config
            )
            return {
                "analysis": response.choices[0].message.content,
                "confidence": response.choices[0].finish_reason == "stop"
            }
        except Exception as e:
            print(f"Error analyzing health progress: {str(e)}")
            return {
                "analysis": "Unable to analyze health progress at this time.",
                "confidence": False
            }
    
    def _create_analysis_prompt(self, metrics: Dict) -> str:
        """Creates prompt for health metrics analysis"""
        return f"""
        Please analyze the following health metrics:
        Heart Rate: {metrics.get('heart_rate', {})}
        Blood Pressure: {metrics.get('blood_pressure', {})}
        Sleep Quality: {metrics.get('sleep', {})}
        Activity Level: {metrics.get('activity', {})}
        
        Please provide:
        1. Overall health assessment
        2. Areas of concern
        3. Improvement recommendations
        4. Risk factors (if any)
        """
        
    def _create_progress_prompt(self, progress_data: Dict) -> str:
        """Creates prompt for progress analysis"""
        return f"""
        Please analyze the following progress data:
        Weight Changes: {progress_data.get('weight', [])}
        Body Composition: {progress_data.get('body_composition', {})}
        Fitness Metrics: {progress_data.get('fitness', {})}
        Health Markers: {progress_data.get('markers', {})}
        
        Please provide:
        1. Progress assessment
        2. Notable improvements
        3. Areas needing attention
        4. Recommendations for continued progress
        """
