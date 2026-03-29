import sys
from pathlib import Path

# Add the current folder to the Python path
sys.path.append(str(Path(__file__).parent.parent))
import os
import joblib
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
# Use the full path from the project root
from backend.logic.calculator import calculate_risk, calculate_bmi, calculate_health_score, simulate_improvement
from backend.database.db import save_health_result

# 1. LOAD SECRETS FIRST (The Master Key)
load_dotenv()
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
SECRET_KEY = os.getenv("SECRET_KEY")

# 2. LOAD THE AI BRAIN (The Knowledge)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "diabetes_model.pkl")
model = joblib.load(MODEL_PATH)

# 3. INITIALIZE THE APP (The Building)
app = FastAPI()

# 4. ATTACH SECURITY (The Guards)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 5. DATA BLUEPRINT
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

# 6. AUTH SETUP
oauth = OAuth()
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

# 7. ROUTES
@app.get("/")
def home():
    return {"message": "LifeGuard AI is running!"}

@app.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for('auth_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth/callback")
async def auth_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get('userinfo')
    if user_info:
        request.session['user'] = user_info['email']
        request.session['user_name'] = user_info['name']
    return {"message": f"Welcome {user_info['name']}! Logged in."}

@app.post("/predict")
async def predict_health(data: HealthData, request: Request):
    user_email = request.session.get('user', 'Guest')
    
    try:
        # 1. AI Calculation - Force the data into a "Numpy-like" list
        input_data = [
            float(data.Pregnancies), 
            float(data.Glucose), 
            float(data.BloodPressure), 
            float(data.SkinThickness), 
            float(data.Insulin), 
            float(data.BMI), 
            float(data.DiabetesPedigreeFunction), 
            float(data.Age)
        ]
        
        # The AI expects a "List of Lists" -> [[...]]
        ai_risk_percent = model.predict_proba([input_data])[0][1] * 100
        
        # 2. Manual Logic
        from logic.calculator import calculate_risk, calculate_bmi, calculate_health_score
        from database.db import save_health_result
        bmi_val = calculate_bmi(data.weight_kg, data.height_m)
        h_score, reasons = calculate_health_score(data.Age, data.blood_sugar, bmi_val, data.is_diabetic)
        
        return {
            "status": "Success",
            "ai_risk": f"{round(ai_risk_percent, 2)}%",
            "manual_score": h_score,
            "remarks": " | ".join(reasons) if reasons else "Healthy"
        }

    except Exception as e:
        # This will tell us EXACTLY what went wrong in the response!
        return {"status": "Error", "message": str(e)}
    



@app.post("/simulate")
async def get_simulation(data: HealthData):
    try:
        # 1. Convert Pydantic data to a Dictionary
        current_data_dict = data.dict()
        
        # 2. Run the "Improved Habits" logic
        improved_stats = simulate_improvement(current_data_dict)
        
        # 3. Predict the NEW risk using the AI Brain
        input_vector = [
            float(improved_stats["Pregnancies"]),
            float(improved_stats["Glucose"]),
            float(improved_stats["BloodPressure"]),
            float(improved_stats["SkinThickness"]),
            float(improved_stats["Insulin"]),
            float(improved_stats["BMI"]),
            float(improved_stats["DiabetesPedigreeFunction"]),
            float(improved_stats["Age"])
        ]
        
        new_risk_percent = model.predict_proba([input_vector])[0][1] * 100
        
        return {
            "status": "Success",
            "original_risk": data.Glucose, # Just for comparison
            "simulated_risk": f"{round(new_risk_percent, 2)}%",
            "message": "This is your risk if you improve your diet and activity!"
        }
    except Exception as e:
        return {"status": "Error", "message": str(e)}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)   
