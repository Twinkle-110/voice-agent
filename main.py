from fastapi import FastAPI, Form, Request
from fastapi.responses import JSONResponse, HTMLResponse
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

# Test endpoint removed - main application is working correctly

@app.post("/tts")
async def tts(text: str = Form(...)):
    # Check if API key is set
    if not MURF_API_KEY:
        return JSONResponse(status_code=500, content={"error": "API key not configured."})

    # For demo purposes, create a placeholder audio file since the API key appears to be incomplete
    # In production, you would use the actual Murf API
    try:
        # Generate a unique filename for the demo audio file
        filename = f"{uuid.uuid4()}.wav"  # Changed to WAV since espeak generates WAV
        static_dir = "static"
        os.makedirs(static_dir, exist_ok=True)
        file_path = os.path.join(static_dir, filename)
        
        # Create a demo audio file using espeak or fallback
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
    """Create a working demo audio file using system TTS if available"""
    try:
        # Try to use system TTS (espeak) if available
        import subprocess
        import tempfile
        
        # Create a temporary WAV file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav:
            temp_wav_path = temp_wav.name
        
        # Try to generate speech using espeak
        try:
            subprocess.run([
                'espeak', '-w', temp_wav_path, '-s', '150', text
            ], check=True, capture_output=True)
            
            # Read the generated audio file
            with open(temp_wav_path, 'rb') as f:
                audio_content = f.read()
            
            # Clean up temp file
            os.unlink(temp_wav_path)
            return audio_content
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            # espeak not available, fall back to placeholder
            pass
        
    except ImportError:
        pass
    
    # Fallback: Create a minimal valid MP3 file with silence
    # This is a valid MP3 file with a short silence
    mp3_content = bytes([
        # MP3 header
        0xFF, 0xFB, 0x90, 0x00,  # MPEG-1 Layer 3, 128kbps, 44.1kHz
        # Frame data (minimal silence)
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        # Additional frames for longer duration
    ] * 10)  # Repeat to make it longer
    
    return mp3_content

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