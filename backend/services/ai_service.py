import os
import httpx
from dotenv import load_dotenv
from pathlib import Path

# Load secret key
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("GEMINI_API_KEY")
# This is the "Universal" Google URL that never changes
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

async def get_health_advice(user_profile: dict):
    """The Direct Brain: Talks to Google via a simple web call."""
    
    payload = {
        "contents": [{
            "parts": [{
                "text": f"You are LifeGuard.AI. User: {user_profile['full_name']}, Goal: {user_profile['target_weight']}kg. Give a 2-line health tip."
            }]
        }]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(URL, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            # Extracting the text from the JSON structure
            return data['candidates'][0]['content']['parts'][0]['text']
        else:
            return "Keep pushing toward your 68kg goal, Manvil! You've got this."