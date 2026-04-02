import asyncio
import sys
sys.path.append(r'c:\LifeGuard.AI (2)\LifeGuard.AI\backend')
from services.ai_services import _call_gemini
import httpx
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=r'c:\LifeGuard.AI (2)\LifeGuard.AI\.env')

async def test():
    API_KEY = os.getenv('GEMINI_API_KEY')
    URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}'
    prompt = 'Hello'
    payload = {'contents': [{'parts': [{'text': prompt}]}]}
    print('URL valid:', bool(API_KEY))
    try:
        async with httpx.AsyncClient() as client:
            r = await client.post(URL, json=payload, timeout=15.0)
            print('Status:', r.status_code)
            print('Body:', r.text)
    except Exception as e:
        print('Exception:', e)

asyncio.run(test())
