from fastapi import FastAPI
from pydantic import BaseModel, Field
from backend.logic.calculator import calculate_risk
class HealthData(BaseModel):
    age: int = Field(gt=0, lt=120)
    blood_sugar: float = Field(gt=0)
    is_diabetic: bool
app = FastAPI()
@app.get("/")
def home():
    return {"message": "LifeGuard AI is running!"}
@app.post("/predict")
@app.post("/predict")
def predict_health(data: HealthData):
    # Now passing all 3 pieces of data to the Brain
    risk_result = calculate_risk(data.age, data.blood_sugar, data.is_diabetic)
    
    return {
        "status": "Success",
        "risk_level": risk_result
    }