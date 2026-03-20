from fastapi import FastAPI
from pydantic import BaseModel
class HealthData(BaseModel):
    age: int
    blood_sugar: float
    is_diabetic: bool
app = FastAPI()
@app.get("/")
def home():
    return {"message": "LifeGuard AI is running!"}
@app.post("/predict")
def predict_health(data: HealthData):
    return {"status": "Received", "age_provided": data.age}