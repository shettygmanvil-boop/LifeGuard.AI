import sys
import os
from typing import Optional
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel, validator
import joblib
from dotenv import load_dotenv

from services.ai_services import get_health_advice, get_health_roadmap, get_stress_score
from services.map_services import get_nearby_hospitals
from services.voice_services import process_voice_command
from services.dashboard_service import get_user_health_history

from database.db import (
    get_user_profile_by_google_id,
    sync_google_user,
    save_user_profile,
    save_health_result,
)

from logic.calculator import (
    calculate_bmi,
    calculate_health_score,
    calculate_disease_risks,
    simulate_improvement,
    get_risk_explanations,
)

# ── CONFIG ────────────────────────────────────────────────────────────────────
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "lifeguard_secret_2026")

# ── MODEL ─────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "diabetes_model.pkl")
model = joblib.load(MODEL_PATH)

# ── APP ───────────────────────────────────────────────────────────────────────
app = FastAPI(title="LifeGuard.AI")

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── PYDANTIC MODELS ───────────────────────────────────────────────────────────
class HealthData(BaseModel):
    # Required lifestyle fields
    age: int
    Gender: str
    Height: float
    Weight: float
    sleep_duration: float
    physical_activity: str
    stress_level: int
    Diet_quality: str = "Average"
    sugar_intake: str
    salt_intake: str
    Smoking_habit: str
    Alcohol_consumption: str
    is_diabetic: bool = False

    # Optional medical fields — BMI auto-computed from Height/Weight
    Pregnancies: Optional[int] = 0
    Glucose: Optional[float] = None
    BloodPressure: Optional[float] = None
    SkinThickness: Optional[float] = None
    Insulin: Optional[float] = None
    BMI: Optional[float] = None
    DiabetesPedigreeFunction: Optional[float] = None
    steps_per_day: Optional[int] = None
    heart_rate: Optional[int] = None

    @validator("Glucose", "BloodPressure", "SkinThickness", "Insulin",
               "DiabetesPedigreeFunction", "BMI", pre=True)
    def blank_to_none(cls, v):
        if v == "" or v == 0:
            return None
        return v


class UserProfile(BaseModel):
    full_name: str
    email: str
    phone_number: str = ""
    age: int = 20
    gender: str = "Not Specified"
    target_weight: float = 70.0
    daily_calorie_goal: int = 2000


# ── HELPERS ───────────────────────────────────────────────────────────────────
DEFAULTS = {
    "Glucose": 100.0,
    "BloodPressure": 72.0,
    "SkinThickness": 20.0,
    "Insulin": 79.0,
    "DiabetesPedigreeFunction": 0.47,
    "Pregnancies": 0,
}


def prepare_dict(data: HealthData) -> dict:
    """Convert HealthData to dict, auto-compute BMI, fill medical defaults."""
    d = data.dict()
    # Auto-compute BMI from Height and Weight
    d["BMI"] = calculate_bmi(data.Weight, data.Height)
    # Fill missing optional medical fields with population averages
    for key, val in DEFAULTS.items():
        if d.get(key) is None:
            d[key] = val
    return d


# ── ROUTES ────────────────────────────────────────────────────────────────────
@app.get("/")
def home():
    return {"message": "LifeGuard AI is running!"}


@app.post("/predict")
async def predict_health(data: HealthData):
    try:
        d = prepare_dict(data)

        # ML model prediction (diabetes risk)
        input_vector = [
            float(d["Pregnancies"]), float(d["Glucose"]),
            float(d["BloodPressure"]), float(d["SkinThickness"]),
            float(d["Insulin"]), float(d["BMI"]),
            float(d["DiabetesPedigreeFunction"]), float(d["age"]),
        ]
        risk_percent = model.predict_proba([input_vector])[0][1] * 100

        # Health score
        health_score, reasons = calculate_health_score(d)

        # Multi-disease risks
        disease_risks = calculate_disease_risks(d)

        # Explanations
        explanations = get_risk_explanations(d)

        return {
            "status": "Success",
            "ai_risk": f"{round(risk_percent, 2)}%",
            "health_score": round(health_score),
            "bmi": d["BMI"],
            "remarks": " | ".join(reasons) if reasons else "All metrics look healthy.",
            "explanations": explanations,
            "disease_risks": disease_risks,
        }
    except Exception as e:
        return {"status": "Error", "message": f"Prediction Error: {str(e)}"}


@app.post("/simulate")
async def get_simulation(data: HealthData):
    try:
        d = prepare_dict(data)
        improved = simulate_improvement(d)

        # Original disease risks
        original_risks = calculate_disease_risks(d)
        original_score, _ = calculate_health_score(d)

        # Simulated ML risk
        input_vector = [
            float(improved["Pregnancies"]), float(improved["Glucose"]),
            float(improved["BloodPressure"]), float(improved["SkinThickness"]),
            float(improved["Insulin"]), float(improved["BMI"]),
            float(improved["DiabetesPedigreeFunction"]), float(improved["age"]),
        ]
        sim_risk_percent = model.predict_proba([input_vector])[0][1] * 100

        # Simulated disease risks
        sim_disease_risks = calculate_disease_risks(improved)
        sim_score, _ = calculate_health_score(improved)

        return {
            "status": "Success",
            "original": {
                "ai_risk": f"{round(model.predict_proba([input_vector])[0][1] * 100, 2)}%",
                "health_score": round(original_score),
                "disease_risks": original_risks,
            },
            "simulated": {
                "ai_risk": f"{round(sim_risk_percent, 2)}%",
                "health_score": round(sim_score),
                "disease_risks": sim_disease_risks,
            },
            "improvements": {
                k: round(original_risks[k] - sim_disease_risks[k], 1)
                for k in original_risks
            },
            "message": "Simulated with improved diet, exercise, sleep and stress management.",
        }
    except Exception as e:
        return {"status": "Error", "message": str(e)}


@app.post("/roadmap")
async def get_roadmap(data: HealthData):
    try:
        d = prepare_dict(data)
        health_score, _ = calculate_health_score(d)
        disease_risks = calculate_disease_risks(d)
        roadmap = await get_health_roadmap(d, health_score, disease_risks)
        return {"status": "Success", "roadmap": roadmap}
    except Exception as e:
        return {"status": "Error", "message": str(e)}


@app.post("/login/google")
async def login_with_google(google_data: dict):
    try:
        sync_google_user(google_data)
        user_profile = get_user_profile_by_google_id(google_data["sub"])
        return {
            "status": "Success",
            "user": dict(user_profile),
        }
    except Exception as e:
        return {"status": "Error", "message": str(e)}


@app.post("/calculate-stress")
async def calculate_stress(data: dict):
    try:
        text = data.get("text", "")
        if not text:
            return {"status": "Error", "message": "No text provided."}
        score = await get_stress_score(text)
        return {"status": "Success", "stress_level": score}
    except Exception as e:
        return {"status": "Error", "message": str(e)}


@app.get("/profile/google/{google_id}")
async def fetch_profile(google_id: str):
    try:
        db_data = get_user_profile_by_google_id(google_id)
        if db_data:
            return {"status": "Success", "profile": dict(db_data)}
        return {"status": "Error", "message": "User not found."}
    except Exception as e:
        return {"status": "Error", "message": str(e)}


@app.put("/profile/{user_email}")
async def update_profile(user_email: str, profile: UserProfile):
    try:
        d = profile.dict()
        d["email"] = user_email
        save_user_profile(d)
        return {"status": "Success", "message": "Profile updated."}
    except Exception as e:
        return {"status": "Error", "message": str(e)}


@app.get("/ai-tip/{google_id}")
async def get_ai_tip(google_id: str):
    try:
        db_data = get_user_profile_by_google_id(google_id)
        if not db_data:
            return {"status": "Error", "message": "User not found."}
        user_dict = dict(db_data)
        tip = await get_health_advice(user_dict)
        return {"status": "Success", "ai_tip": tip}
    except Exception as e:
        return {"status": "Error", "message": str(e)}


@app.post("/voice-command")
async def handle_voice(data: dict):
    try:
        text = data.get("text", "")
        if not text:
            return {"status": "Error", "message": "No text received"}
        intent = process_voice_command(text)
        return {"status": "Success", "intent": intent}
    except Exception as e:
        return {"status": "Error", "message": str(e)}


@app.get("/nearby-hospitals")
async def find_hospitals(lat: float, lng: float):
    try:
        hospitals = get_nearby_hospitals(lat, lng)
        return {"status": "Success", "count": len(hospitals), "data": hospitals}
    except Exception as e:
        return {"status": "Error", "message": str(e)}


@app.get("/dashboard/{google_id}")
async def fetch_dashboard(google_id: str):
    try:
        history = await get_user_health_history(google_id)
        return {"status": "Success", "count": len(history), "history": history}
    except Exception as e:
        return {"status": "Error", "message": f"Cloud error: {str(e)}"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
