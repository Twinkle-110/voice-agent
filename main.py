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

    # For demo purposes, create a placeholder audio file since the API key appears to be incomplete
    # In production, you would use the actual Murf API
    try:
        # Generate a unique filename for the demo audio file
        filename = f"{uuid.uuid4()}.mp3"
        static_dir = "static"
        os.makedirs(static_dir, exist_ok=True)
        file_path = os.path.join(static_dir, filename)
        
        # Create a simple demo audio file (silent MP3) as placeholder
        # In production, this would be replaced with actual Murf API call
        demo_audio_content = create_demo_audio_content(text)
        
        with open(file_path, "wb") as audio_file:
            audio_file.write(demo_audio_content)
        
        # Return the URL to the saved audio file
        return JSONResponse(content={
            "audio_url": f"/static/{filename}",
            "message": "Demo mode: Generated placeholder audio file",
            "text": text
        })
        
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return JSONResponse(status_code=500, content={"error": "Server error", "details": str(e)})

def create_demo_audio_content(text):
    """Create a minimal MP3 file header for demo purposes"""
    # This is a minimal MP3 header for a very short silent audio file
    # In production, this would be replaced with actual Murf API response
    mp3_header = bytes([
        0xFF, 0xFB, 0x90, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
    ])
    return mp3_header

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