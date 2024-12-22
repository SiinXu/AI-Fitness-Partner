import os
import requests
from flask import current_app
import base64
import json

class VoiceService:
    def __init__(self, api_key: str = None):
        self.fish_audio_endpoint = os.getenv('FISH_AUDIO_ENDPOINT', 'https://api.fish-audio.com/v1')
        self.api_key = api_key or os.getenv('FISH_AUDIO_API_KEY')

    def speech_to_text(self, audio_file) -> dict:
        """Convert speech to text using Fish Audio API."""
        try:
            if not self.api_key:
                return {
                    'success': False,
                    'error': 'Please configure your Fish Audio API key.',
                    'text': None
                }
                
            # Read audio file
            audio_content = audio_file.read()
            audio_base64 = base64.b64encode(audio_content).decode('utf-8')

            # Prepare request
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'audio': audio_base64,
                'model': 'general',  # or other model as needed
                'language': 'en'     # or other language as needed
            }

            # Make API request
            response = requests.post(
                f'{self.fish_audio_endpoint}/speech-to-text',
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()

            return {
                'success': True,
                'error': None,
                'text': result.get('text')
            }
            
        except Exception as e:
            error_msg = f'Speech to text error: {str(e)}'
            print(error_msg)  # For testing
            if current_app:
                current_app.logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg,
                'text': None
            }

    def text_to_speech(self, text: str) -> dict:
        """Convert text to speech using Fish Audio API."""
        try:
            if not self.api_key:
                return {
                    'success': False,
                    'error': 'Please configure your Fish Audio API key.',
                    'audio': None
                }
                
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'text': text,
                'voice': 'en-US-1',  # or other voice as needed
                'speed': 1.0,
                'pitch': 1.0
            }

            # Make API request
            response = requests.post(
                f'{self.fish_audio_endpoint}/text-to-speech',
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()

            return {
                'success': True,
                'error': None,
                'audio': result.get('audio')  # Base64 encoded audio
            }
            
        except Exception as e:
            error_msg = f'Text to speech error: {str(e)}'
            print(error_msg)  # For testing
            if current_app:
                current_app.logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg,
                'audio': None
            }

def main():
    """Test the VoiceService class"""
    print("Testing VoiceService...")
    
    # Create an instance
    service = VoiceService()
    
    # Test text to speech
    text = "Welcome to your AI Fitness Partner! Let's start your workout."
    result = service.text_to_speech(text)
    print("\nText to Speech Result:")
    print(json.dumps(result, indent=2))
    
    # Note: We can't test speech to text here without an actual audio file
    print("\nNote: Speech to text test requires an audio file.")

if __name__ == '__main__':
    main()
