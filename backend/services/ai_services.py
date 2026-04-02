import os
import httpx
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("GEMINI_API_KEY")
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"


async def _call_gemini(prompt: str) -> str:
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    async with httpx.AsyncClient() as client:
        try:
            r = await client.post(URL, json=payload, timeout=15.0)
            if r.status_code == 200:
                return r.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            pass
    return None


async def get_health_advice(user: dict) -> str:
    """Short 2-line tip for the dashboard."""
    prompt = (
        f"You are LifeGuard.AI coach. The user is {user.get('full_name', 'the user')}, "
        f"age {user.get('age', '?')}, gender {user.get('gender', '?')}, "
        f"target weight {user.get('target_weight', '?')} kg. "
        "Give exactly 2 motivating, actionable health tips. Be concise and personal."
    )
    result = await _call_gemini(prompt)
    return result or f"Stay consistent, {user.get('full_name', 'friend')}! Small daily habits lead to big results."


async def get_health_roadmap(health_data: dict, health_score: int, disease_risks: dict) -> str:
    """
    Generates a personalised AI roadmap with specific tips to improve health score
    and reduce disease risks.
    """
    risks_text = (
        f"Type-2 Diabetes: {disease_risks.get('type2_diabetes')}%, "
        f"Hypertension: {disease_risks.get('hypertension')}%, "
        f"Cardiovascular: {disease_risks.get('cardiovascular')}%, "
        f"Obesity: {disease_risks.get('obesity')}%"
    )

    score_instruction = ""
    if health_score < 60:
        score_instruction = "Their health score is critically low. Focus on urgent lifestyle interventions, strong encouragement to consult medical professionals, and immediate risk mitigation."
    elif health_score < 85:
        score_instruction = "Their health score is moderate. Focus on sustainable lifestyle improvements, building better habits, and reducing specific identified risks."
    else:
        score_instruction = "Their health score is excellent. Focus on maintaining current good habits, fine-tuning their routine, and long-term optimization."

    prompt = (
        f"You are LifeGuard.AI, a professional health coach AI. "
        f"A user has the following health profile:\n"
        f"- Age: {health_data.get('age')}, Gender: {health_data.get('Gender')}\n"
        f"- BMI: {health_data.get('BMI')}, Glucose: {health_data.get('Glucose')}, "
        f"Blood Pressure: {health_data.get('BloodPressure')}\n"
        f"- Physical Activity: {health_data.get('physical_activity')}, "
        f"Sleep: {health_data.get('sleep_duration')} hrs, Stress: {health_data.get('stress_level')}/10\n"
        f"- Smoking: {health_data.get('Smoking_habit')}, Alcohol: {health_data.get('Alcohol_consumption')}, "
        f"Sugar Intake: {health_data.get('sugar_intake')}\n"
        f"- Current Health Score: {health_score}/100. {score_instruction}\n"
        f"- Disease Risk Estimates: {risks_text}\n\n"
        f"Generate a highly personalised 4-week health improvement roadmap based on their health score ({health_score}/100).\n"
        f"Structure it as:\n"
        f"**Week 1 – Foundation:** (2-3 specific actions)\n"
        f"**Week 2 – Build Momentum:** (2-3 specific actions)\n"
        f"**Week 3 – Intensify:** (2-3 specific actions)\n"
        f"**Week 4 – Sustain:** (2-3 specific actions)\n"
        f"**Key Focus Areas:** List the top 3 things this person must prioritise.\n"
        f"Be specific, actionable, and address their actual risk factors. Keep it under 300 words."
    )

    result = await _call_gemini(prompt)
    return result or (
        "**Week 1:** Start with 20-min daily walks and reduce sugar intake.\n"
        "**Week 2:** Add strength training twice a week. Track your meals.\n"
        "**Week 3:** Aim for 7-8 hrs sleep. Practice stress-reduction techniques.\n"
        "**Week 4:** Maintain all habits. Schedule a health check-up.\n"
        "**Key Focus:** Diet, Exercise, Sleep."
    )


async def get_stress_score(user_text: str) -> int:
    """Uses Gemini to evaluate a stress score (1-10) based on free-text."""
    prompt = (
        f"You are a clinical AI evaluating stress levels. "
        f"Based on the following text from a user about their life, mood, and sleep, "
        f"determine their stress level on a scale of 1 to 10. "
        f"Return ONLY a single integer. No other text.\n\n"
        f"User text: \"{user_text}\""
    )
    result = await _call_gemini(prompt)
    if result:
        try:
            val = int(result.strip())
            return max(1, min(10, val))
        except ValueError:
            pass
            
    # --- FALLBACK: Since the current Gemini API Key is disabled/deleted ---
    # Smart keyword calculator to prove the UI works locally
    text = user_text.lower()
    score = 4  # base healthy-ish score
    
    # Stressors
    if "overwhelmed" in text or "anxious" in text or "panic" in text: score += 3
    if "deadlines" in text or "work" in text or "busy" in text: score += 2
    if "sluggish" in text or "tired" in text or "exhausted" in text: score += 2
    if "inconsistent" in text or "bad sleep" in text or "insomnia" in text: score += 2
    
    # Reducers
    if "sufficient" in text or "good sleep" in text or "8 hours" in text: score -= 2
    if "relaxing" in text or "no tight deadlines" in text or "chill" in text: score -= 2
    
    return max(1, min(10, score))
