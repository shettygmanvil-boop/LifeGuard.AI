import os
import httpx
from dotenv import load_dotenv
from pathlib import Path

# Load secrets
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("GEMINI_API_KEY")
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

async def get_health_advice(db_row: dict):
    """Uses the data fetched from SQL (google_id) to give advice."""
    
    # We pull directly from the dictionary keys that match your SQL columns
    payload = {
        "contents": [{
            "parts": [{
                "text": (
                    f"You are the LifeGuard.AI coach for {db_row.get('full_name')}. "
                    f"His strict target is to reach {db_row.get('target_weight')}kg. "
                    "Provide a 2-line health tip. Address him by name."
                )
            }]
        }]
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(URL, json=payload, timeout=10.0)
            if response.status_code == 200:
                return response.json()['candidates'][0]['content']['parts'][0]['text']
            return f"Keep going, {db_row.get('full_name')}! You're close to {db_row.get('target_weight')}kg!"
        except Exception:
            return f"Stay active today, {db_row.get('full_name')}!"