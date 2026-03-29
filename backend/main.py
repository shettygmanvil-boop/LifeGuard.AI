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
# Import the new database function at the top of main.py
from backend.database.db import get_user_profile

@app.get("/profile/{user_email}")
async def fetch_real_profile(user_email: str):
    try:
        # 1. Ask the 'Messenger' to find the data in SQL
        db_data = get_user_profile(user_email)
        
        # 2. Check if the user actually exists in the 'Cabinet'
        if db_data:
            return {
                "status": "Success",
                "profile": {
                    "email": db_data[0],
                    "full_name": db_data[1],
                    "age": db_data[2],
                    "gender": db_data[3],
                    "target_weight": db_data[4],
                    "daily_calorie_goal": db_data[5]
                }
            }
        else:
            return {"status": "Error", "message": "User not found in LifeGuard database."}
            
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)