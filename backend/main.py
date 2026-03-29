import sys
import os
import joblib
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth

# Add current folder to path
sys.path.append(str(Path(__file__).parent.parent))

# Import your custom logic
from backend.logic.calculator import calculate_risk, calculate_bmi, calculate_health_score, simulate_improvement, get_risk_explanations

# 1. LOAD SECRETS
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "a_very_secret_key")

# 2. LOAD THE AI BRAIN
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "diabetes_model.pkl")
model = joblib.load(MODEL_PATH)

# 3. INITIALIZE APP
app = FastAPI()

# 4. MIDDLEWARE
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 5. DATA BLUEPRINT (LifeGuard.AI Specification)
class HealthData(BaseModel):
    Pregnancies: int
    Glucose: float
    BloodPressure: float
    SkinThickness: float
    Insulin: float
    BMI: float
    DiabetesPedigreeFunction: float
    Age: int
    weight_kg: float = 70.0 
    height_m: float = 1.75
    blood_sugar: float = 90.0
    is_diabetic: bool = False
class UserProfile(BaseModel):
    full_name: str
    age: int
    gender: str
    target_weight: float
    daily_calorie_goal: int = 2000
    notification_enabled: bool = True
    profile_picture_url: str = "https://example.com/default-avatar.png"

# 6. ROUTES
@app.get("/")
def home():
    return {"message": "LifeGuard AI is running!"}

@app.post("/predict")
async def predict_health(data: HealthData):
    try:
        # Prepare inputs for AI
        input_vector = [
            float(data.Pregnancies), float(data.Glucose), float(data.BloodPressure),
            float(data.SkinThickness), float(data.Insulin), float(data.BMI),
            float(data.DiabetesPedigreeFunction), float(data.Age)
        ]
        
        # AI Prediction
        risk_percent = model.predict_proba([input_vector])[0][1] * 100
        
        # Manual Score & Explanations (Day 9 Target)
        health_score, manual_reasons = calculate_health_score(data.Age, data.Glucose, data.BMI, data.is_diabetic)
        explanations = get_risk_explanations(data.dict())
        
        return {
            "status": "Success",
            "ai_risk": f"{round(risk_percent, 2)}%",
            "manual_score": health_score,
            "remarks": " | ".join(manual_reasons),
            "explanations": explanations 
        }
    except Exception as e:
        return {"status": "Error", "message": f"Calculation Error: {str(e)}"}

@app.post("/simulate")
async def get_simulation(data: HealthData):
    try:
        current_data_dict = data.dict()
        improved_stats = simulate_improvement(current_data_dict)
        
        input_vector = [
            float(improved_stats["Pregnancies"]), float(improved_stats["Glucose"]),
            float(improved_stats["BloodPressure"]), float(improved_stats["SkinThickness"]),
            float(improved_stats["Insulin"]), float(improved_stats["BMI"]),
            float(improved_stats["DiabetesPedigreeFunction"]), float(improved_stats["Age"])
        ]
        
        new_risk_percent = model.predict_proba([input_vector])[0][1] * 100
        
        return {
            "status": "Success",
            "original_risk": data.Glucose,
            "simulated_risk": f"{round(new_risk_percent, 2)}%",
            "message": "This is your potential risk with improved habits!"
        }
    except Exception as e:
        return {"status": "Error", "message": str(e)}
@app.get("/profile/{user_email}")
async def get_user_profile(user_email: str):
    try:
        # In Day 11, we will pull this from the real Database
        # For Day 10, we are returning a "Mock" profile to test the UI
        return {
            "status": "Success",
            "profile": {
                "full_name": "Manvil",
                "email": user_email,
                "age": 20,
                "gender": "Male",
                "target_weight": 75.0,
                "daily_calorie_goal": 2200,
                "college": "BMSIT",
                "joined_date": "March 2026"
            }
        }
    except Exception as e:
        return {"status": "Error", "message": str(e)}
@app.put("/profile/{user_email}")
async def update_user_profile(user_email: str, updated_data: UserProfile):
    try:
        # This is where we 'Overwrite' the old data with the new 'updated_data'
        return {
            "status": "Success",
            "message": f"Profile for {user_email} has been updated!",
            "new_goals": updated_data
        }
    except Exception as e:
        return {"status": "Error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)