def calculate_risk(score: int):
    if score < 70:
        return "High Risk"
    elif score < 90:
        return "Moderate Risk"
    else:
        return "Low Risk"
def calculate_bmi(weight_kg: float, height_m: float):
    # Formula: weight / (height * height)
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)
def calculate_health_score(age: int, sugar: float, bmi: float, is_diabetic: bool):
    score = 100
    reasons = [] # New: A list to hold our explanations
    
    if is_diabetic:
        score -= 30
        reasons.append("Known diabetic status")
        
    if sugar > 100:
        score -= 20
        reasons.append("High blood sugar levels detected")
        
    if bmi > 25:
        score -= 15
        reasons.append("BMI is in the overweight range")
        
    if age > 45:
        score -= 10
        reasons.append("Age-related health risk factor")
        
    # We return both the score and the list of reasons
    return max(0, score), reasons