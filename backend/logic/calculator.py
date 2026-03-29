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

# ... your existing functions are up here ...

def simulate_improvement(current_data):
    # This creates a "Best-Case" version of the user's data
    improved_data = current_data.copy()
    
    # Improved Diet: Reduce Glucose by 20%
    improved_data["Glucose"] = current_data["Glucose"] * 0.8
    
    # Exercise: Reduce BMI by 5%
    improved_data["BMI"] = current_data["BMI"] * 0.95
    
    # Healthier sleep/habits often stabilize insulin
    if improved_data.get("Insulin") == 0:
        improved_data["Insulin"] = 30 
        
    return improved_data
def get_risk_explanations(data_dict):
    # This identifies the "Why" behind the risk
    reasons = []
    
    if float(data_dict.get("Glucose", 0)) > 140:
        reasons.append("High Glucose level is the primary risk driver.")
        
    if float(data_dict.get("BMI", 0)) > 30:
        reasons.append("BMI is in the obese range, significantly increasing risk.")
        
    if float(data_dict.get("Age", 0)) > 45:
        reasons.append("Age-related factors contribute to higher vulnerability.")
        
    if float(data_dict.get("BloodPressure", 0)) > 90:
        reasons.append("Elevated Blood Pressure adds strain to the system.")

    # Return top 3 reasons or a 'Healthy' message
    return reasons[:3] if reasons else ["Lifestyle factors are currently in a healthy range."]