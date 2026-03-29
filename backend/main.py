from services.ai_service import get_health_advice
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
app = FastAPI(title="LifeGuard.AI - Smart Health Assistant")

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
# Import the new database function at the top of main.py
from backend.database.db import get_user_profile_by_google_id

@app.get("/profile/google/{google_id}")
async def fetch_profile_by_id(google_id: str):
    try:
        # Search the 'Locker' using the unique Fingerprint
        db_data = get_user_profile_by_google_id(google_id)
        
        if db_data:
            return {
                "status": "Success",
                "profile": dict(db_data) # Converts the SQL row to a clean Dictionary
            }
        else:
            return {"status": "Error", "message": "User not registered in LifeGuard.AI"}
            
    except Exception as e:
        return {"status": "Error", "message": str(e)}
    # 1. Add 'sync_google_user' to your imports at the top
from backend.database.db import sync_google_user

# 2. Add the Login Route
@app.post("/login/google")
async def login_with_google(google_data: dict):
    try:
        # The 'google_data' comes from Nipun's frontend
        # It contains 'sub', 'name', 'email', and 'picture'
        
        # Sync the user into our SQLite Locker
        sync_google_user(google_data)
        
        # Fetch the updated profile to send back to the frontend
        user_profile = get_user_profile_by_google_id(google_data['sub'])
        
        return {
            "status": "Success",
            "message": "User authenticated and synced.",
            "user": dict(user_profile)
        }
    except Exception as e:
        return {"status": "Error", "message": str(e)}
# Import the save function at the top of main.py
from backend.database.db import save_user_profile

@app.put("/profile/{user_email}")
async def update_profile_permanently(user_email: str, profile: UserProfile):
    try:
        # Convert the Pydantic model to a dictionary
        data_to_save = profile.dict()
        data_to_save['email'] = user_email
        
        # Save it to the SQLite Locker
        save_user_profile(data_to_save)
        
        return {"status": "Success", "message": f"Profile for {user_email} updated in SQL!"}
    except Exception as e:
        return {"status": "Error", "message": str(e)}

# 2. Add the AI Tip Route
@app.get("/ai-tip/{google_id}")
async def get_user_ai_tip(google_id: str):
    try:
        # First, find the user in our SQL locker
        user_profile = get_user_profile_by_google_id(google_id)
        
        if not user_profile:
            return {"status": "Error", "message": "User not found"}
        
        # Convert SQL row to dictionary and ask Gemini for advice
        tip = await get_health_advice(dict(user_profile))
        
        return {
            "status": "Success",
            "ai_tip": tip
        }
    except Exception as e:
        return {"status": "Error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
