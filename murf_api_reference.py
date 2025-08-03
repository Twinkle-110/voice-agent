"""
Reference implementation for Murf API integration
Use this when you have a valid Murf API key

Replace the demo implementation in main.py with this code:
"""

import requests
import uuid
import os

async def tts_with_murf_api(text: str, murf_api_key: str):
    """
    Correct implementation for Murf API TTS
    This is the production-ready version to use with a valid API key
    """
    # Use the correct Murf API endpoint for text-to-speech generation
    url = "https://api.murf.ai/v1/speech/generate"
    
    headers = {
        "Content-Type": "application/json",
        "api-key": murf_api_key
    }

    # Payload format for the speech generation endpoint
    payload = {
        "text": text,
        "voiceId": "en-US-natalie",
        "format": "MP3",
        "sampleRate": 22050,
        "modelVersion": "GEN2"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            audio_data = response.json()
            
            if 'audioFile' in audio_data:
                # Download the audio file from the provided URL
                audio_response = requests.get(audio_data['audioFile'])
                if audio_response.status_code == 200:
                    # Generate a unique filename for the audio file
                    filename = f"{uuid.uuid4()}.mp3"
                    static_dir = "static"
                    os.makedirs(static_dir, exist_ok=True)
                    file_path = os.path.join(static_dir, filename)
                    # Save the audio content to a file
                    with open(file_path, "wb") as audio_file:
                        audio_file.write(audio_response.content)
                    # Return the URL to the saved audio file
                    return {"audio_url": f"/static/{filename}"}
                else:
                    return {"error": "Failed to download audio file"}
            else:
                return {"error": "No audio file in response"}
        else:
            return {"error": "TTS failed", "details": response.text}
    except Exception as e:
        return {"error": "Server error", "details": str(e)}

"""
Alternative using Murf Python SDK:

from murf import Murf

def tts_with_murf_sdk(text: str, murf_api_key: str):
    client = Murf(api_key=murf_api_key)
    
    res = client.text_to_speech.generate(
        text=text,
        voice_id="en-US-natalie",
        format="MP3",
        sample_rate=22050
    )
    
    # Download and save the audio file
    audio_response = requests.get(res.audio_file)
    if audio_response.status_code == 200:
        filename = f"{uuid.uuid4()}.mp3"
        with open(f"static/{filename}", "wb") as f:
            f.write(audio_response.content)
        return {"audio_url": f"/static/{filename}"}
    
    return {"error": "Failed to generate audio"}
"""