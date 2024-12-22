from typing import Dict, List
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import requests
import json

class DataAnalyst:
    def __init__(self, model_config: Dict = None, user_id: int = None, api_key: str = None):
        self.model_config = model_config or {
            'temperature': 0.2,
            'max_tokens': 1000
        }
        self.user_id = user_id
        self.api_key = api_key or os.getenv('MODELSCOPE_API_KEY')
        
    def analyze_trends(self, data: Dict) -> Dict:
        """
        Analyzes fitness and health trends
        
        Args:
            data: Dict containing historical fitness and health data
        """
        try:
            # Convert data to pandas DataFrame for analysis
            df = pd.DataFrame(data.get('history', []))
            if df.empty:
                return {
                    "trends": [],
                    "insights": "Not enough data for trend analysis.",
                    "recommendations": []
                }
            
            # Calculate basic statistics
            stats = self._calculate_statistics(df)
            
            # Check if we have API key
            if not self.api_key:
                return {
                    "trends": stats,
                    "insights": "Please configure your ModelScope API key to get AI-powered insights.",
                    "recommendations": []
                }
            
            # Generate trend analysis prompt
            prompt = self._create_trend_prompt(stats)
            
            # Get AI insights using ModelScope API (OpenAI compatible endpoint)
            url = "https://api-inference.modelscope.cn/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "Qwen/Qwen2.5-32B-Instruct",
                "messages": [
                    {"role": "system", "content": "You are a fitness data analyst providing insights on health and workout trends."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": self.model_config.get('temperature', 0.2),
                "max_tokens": self.model_config.get('max_tokens', 1000)
            }
            
            # Use simple request configuration
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            if 'choices' in result and len(result['choices']) > 0:
                insights = result['choices'][0]['message']['content']
            else:
                insights = "Unable to generate insights at this time."
            
            return {
                "trends": stats,
                "insights": insights,
                "recommendations": self._extract_recommendations(insights)
            }
            
        except Exception as e:
            print(f"Error analyzing trends: {str(e)}")
            return {
                "trends": [],
                "insights": "Unable to analyze trends at this time.",
                "recommendations": []
            }
            
    def _calculate_statistics(self, df: pd.DataFrame) -> List[Dict]:
        """Calculate basic statistics from fitness data"""
        stats = []
        
        if 'calories_burned' in df.columns:
            avg_calories = df['calories_burned'].mean()
            stats.append({
                'metric': 'Average Calories Burned',
                'value': f"{avg_calories:.1f} kcal"
            })
            
        if 'duration' in df.columns:
            avg_duration = df['duration'].mean()
            stats.append({
                'metric': 'Average Workout Duration',
                'value': f"{avg_duration:.1f} minutes"
            })
            
        if 'heart_rate' in df.columns:
            avg_hr = df['heart_rate'].mean()
            stats.append({
                'metric': 'Average Heart Rate',
                'value': f"{avg_hr:.0f} bpm"
            })
            
        return stats
        
    def _create_trend_prompt(self, stats: List[Dict]) -> str:
        """Create a prompt for trend analysis"""
        prompt = "Based on the following fitness data, provide insights and recommendations:\n\n"
        for stat in stats:
            prompt += f"- {stat['metric']}: {stat['value']}\n"
        prompt += "\nPlease analyze these trends and provide:\n"
        prompt += "1. Key observations about the user's fitness patterns\n"
        prompt += "2. Specific recommendations for improvement\n"
        prompt += "3. Any potential health concerns or areas that need attention\n"
        return prompt
        
    def _extract_recommendations(self, insights: str) -> List[str]:
        """Extract recommendations from insights text"""
        recommendations = []
        lines = insights.split('\n')
        for line in lines:
            if line.strip().startswith('•') or line.strip().startswith('-'):
                recommendations.append(line.strip()[1:].strip())
        return recommendations

def main():
    """Test the analyze_trends method"""
    print("Testing analyze_trends method...")
    
    # Create an instance with default config
    analyst = DataAnalyst()
    
    # Sample fitness data for testing
    sample_data = {
        'history': [
            {
                'date': '2023-12-01',
                'exercises': ['running', 'pushups'],
                'duration': 30,
                'calories_burned': 250,
                'heart_rate': 150,
                'distance': 5,
                'pace': '6:00'
            }
        ]
    }
    
    # Test the analyze_trends method
    results = analyst.analyze_trends(sample_data)
    
    # Print results
    print("\nResults:")
    print(f"Trends: {results['trends']}")
    print(f"\nInsights: {results['insights']}")
    print(f"\nRecommendations: {results['recommendations']}")

if __name__ == '__main__':
    main()
