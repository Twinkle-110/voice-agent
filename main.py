from fastapi import FastAPI, Form, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import requests
import os
import uuid

# Load environment variables from .env
load_dotenv()

app = FastAPI()

# Mount static and template directories
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load Murf API Key
MURF_API_KEY = os.getenv("MURF_API_KEY")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/tts")
async def tts(text: str = Form(...)):
    # Check if API key is set
    if not MURF_API_KEY:
        return JSONResponse(status_code=500, content={"error": "API key not configured."})

    # Use the synchronous Murf API endpoint for direct audio generation
    url = "https://api.murf.ai/v1/speech:synthesize"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "api-key": MURF_API_KEY  # Note: header is 'api-key', not 'apikey'
    }

    # Payload format for the synchronous synthesis endpoint
    payload = {
        "speech": {
            "text": text,
            "voiceId": "en-US-natalie",  # Use a valid Murf voice ID
            "format": "MP3",
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            # Generate a unique filename for the audio file
            filename = f"{uuid.uuid4()}.mp3"
            static_dir = "static"
            os.makedirs(static_dir, exist_ok=True)
            file_path = os.path.join(static_dir, filename)
            # Save the audio content to a file
            with open(file_path, "wb") as audio_file:
                audio_file.write(response.content)
            # Return the URL to the saved audio file
            return JSONResponse(content={"audio_url": f"/{static_dir}/{filename}"})
        else:
            print(f"TTS Error: {response.status_code} - {response.text}")
            return JSONResponse(status_code=500, content={
                "error": "TTS failed", 
                "details": response.text,
                "status_code": response.status_code
            })
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return JSONResponse(status_code=500, content={"error": "Server error", "details": str(e)})

# Optional: Add endpoint to get available voices
@app.get("/voices")
async def get_voices():
    if not MURF_API_KEY:
        return JSONResponse(status_code=500, content={"error": "API key not configured."})

    url = "https://api.murf.ai/v1/speech/voices"
    headers = {
        "Accept": "application/json",
        "api-key": MURF_API_KEY
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return JSONResponse(content=response.json())
        else:
            return JSONResponse(status_code=500, content={
                "error": "Failed to fetch voices", 
                "details": response.text
            })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Server error", "details": str(e)})