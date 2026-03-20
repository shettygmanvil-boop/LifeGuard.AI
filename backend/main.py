from fastapi import FastAPI
from pydantic import BaseModel, Field
from backend.logic.calculator import calculate_risk, calculate_bmi
class HealthData(BaseModel):
    age: int = Field(gt=0, lt=120)
    blood_sugar: float = Field(gt=0)
    is_diabetic: bool
    weight_kg: float = Field(gt=10, lt=300) # Added Weight
    height_m: float = Field(gt=0.5, lt=2.5) # Added Height (in meters)

app = FastAPI()
@app.get("/")
def home():
    return {"message": "LifeGuard AI is running!"}
@app.post("/predict")
@app.post("/predict")
@app.post("/predict")
def predict_health(data: HealthData):
    # 1. Calculate Risk
    risk_result = calculate_risk(data.age, data.blood_sugar, data.is_diabetic)
    
    # 2. Calculate BMI
    bmi_value = calculate_bmi(data.weight_kg, data.height_m)
    
    return {
        "status": "Success",
        "risk_level": risk_result,
        "bmi": bmi_value
    }
