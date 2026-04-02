import asyncio
import sys
import os
sys.path.append(r'c:\LifeGuard.AI (2)\LifeGuard.AI\backend')
from services.ai_services import get_stress_score, _call_gemini

async def test():
    prompt = 'You are a clinical AI evaluating stress levels. Based on the following text from a user about their life, mood, and sleep, determine their stress level on a scale of 1 to 10. Return ONLY a single integer. No other text.\n\nUser text: \"I am slightly sluggish\"'
    res = await _call_gemini(prompt)
    print('Raw Gemini Output:', repr(res))
    val = await get_stress_score('I am slightly sluggish')
    print('Final Output:', val)

asyncio.run(test())
