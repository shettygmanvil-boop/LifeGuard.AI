'''import os
from dotenv import load_dotenv

# This line finds the .env file and loads the variables into your system
load_dotenv()

# Now we 'Fetch' the specific secrets we saved earlier
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
SECRET_KEY = os.getenv("SECRET_KEY")
from fastapi import FastAPI
from pydantic import BaseModel, Field
from backend.logic.calculator import calculate_risk, calculate_bmi,calculate_health_score
from backend.database.db import save_health_result
from fastapi import Request
app = FastAPI()

@app.get("/login")
async def login(request: Request):
    # This creates the URL for your 'Callback' (where the user returns)
    redirect_uri = request.url_for('auth_callback')
    # This sends the user to Google's login page
    return await oauth.google.authorize_redirect(request, redirect_uri)
@app.get("/auth/callback")
async def auth_callback(request: Request):
    # 1. The 'Handshake': Trade the code for the user's Google Info
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get('userinfo')
    
    # 2. The 'Memory': Save the user's email in the Session
    if user_info:
        request.session['user'] = user_info['email']
        request.session['user_name'] = user_info['name']
        
    # 3. The 'Welcome': Send them back to the main page
    return {"message": f"Welcome {user_info['name']}! You are now logged in."}
@app.get("/logout")
async def logout(request: Request):
    # This clears the 'Memory' (the sticky note)
    request.session.pop('user', None)
    return {"message": "You have been logged out safely."}
class HealthData(BaseModel):
    age: int = Field(gt=0, lt=120)
    blood_sugar: float = Field(gt=0)
    is_diabetic: bool
    weight_kg: float = Field(gt=10, lt=300) # Added Weight
    height_m: float = Field(gt=0.5, lt=2.5) # Added Height (in meters)

app = FastAPI()
from starlette.middleware.sessions import SessionMiddleware

# This tells the 'Guard' to remember users using your Secret Key
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)    
from authlib.integrations.starlette_client import OAuth

# This creates the 'Manager' for all our login types
oauth = OAuth()

# This tells the manager specifically how to talk to Google
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)
@app.get("/")
def home():
    return {"message": "LifeGuard AI is running!"}
@app.post("/predict")
async def predict_health(data: HealthData): # Added 'async' here!
    # 1. Logic Calculations
    bmi_value = calculate_bmi(data.weight_kg, data.height_m)
    health_score, feedback = calculate_health_score(data.age, data.blood_sugar, bmi_value, data.is_diabetic)
    risk_result = calculate_risk(health_score)
    
    # 2. Prepare the "Folder" to be saved
    result_to_save = {
        "user_age": data.age,
        "score": health_score,
        "risk": risk_result,
        "remarks": feedback
    }
    
    # 3. Save to Cloud (The new line!)
    await save_health_result(result_to_save)
    
    return {
        "status": "Success",
        "risk_level": risk_result,
        "bmi": bmi_value,
        "overall_health_score": health_score,
        "remarks": feedback
    }
    The Overwrite: You defined app = FastAPI() once at the top and again in the middle. The second one wiped out the /login and /callback routes you had already defined.

The Ghost 'oauth': You were using the oauth variable in your login function before you actually created it (defined it) later in the file.

Missing Imports: Some required tools (like OAuth) were being used before their import lines.'''


import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Depends
from pydantic import BaseModel, Field
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth

# 1. Load Secrets
load_dotenv()
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
SECRET_KEY = os.getenv("SECRET_KEY")

# 2. Initialize App (ONLY ONCE)
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# 3. Import Logic & Database
from backend.logic.calculator import calculate_risk, calculate_bmi, calculate_health_score
from backend.database.db import save_health_result

# 4. Setup Google OAuth
oauth = OAuth()
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

# 5. Data Models
class HealthData(BaseModel):
    age: int = Field(gt=0, lt=120)
    blood_sugar: float = Field(gt=0)
    is_diabetic: bool
    weight_kg: float = Field(gt=10, lt=300)
    height_m: float = Field(gt=0.5, lt=2.5)

# 6. Routes (The 'Doors')
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
    return {"message": f"Welcome {user_info['name']}! You are now logged in."}

@app.get("/logout")
async def logout(request: Request):
    request.session.pop('user', None)
    return {"message": "You have been logged out safely."}
@app.get("/me")
async def get_my_profile(request: Request):
    # This pulls the 'sticky note' out of your session pocket
    user = request.session.get('user')
    user_name = request.session.get('user_name')
    
    if not user:
        return {"error": "You are not logged in!"}
        
    return {
        "email": user,
        "name": user_name,
        "message": "This data is coming straight from your Google Profile!"
    }

    
@app.post("/predict")
async def predict_health(data: HealthData, request: Request):
    user_email = request.session.get('user', 'Guest')
    user_name = request.session.get('user_name', 'Visitor')

    # ADD YOUR LOGIC HERE (This is the rough work):
    health_score = 100 - (data.age * 0.2) # Example: Replace with your real math
    risk_result = "Low Risk"             # Example: Replace with your real logic
    feedback = "Keep exercising!"       # Example: Replace with your real logic

    # NOW these variables exist and the yellow lines will disappear:
    result_to_save = {
        "user_email": user_email,
        "user_name": user_name,
        "user_age": data.age,
        "score": health_score,
        "risk": risk_result,
        "remarks": feedback
    }
    # ...
    
    # 3. Save to MongoDB
    await save_health_result(result_to_save)
    
    return {
        "status": "Success",
        "risk_level": risk_result,
        "bmi": bmi_value,
        "overall_health_score": health_score,
        "remarks": feedback
    }
