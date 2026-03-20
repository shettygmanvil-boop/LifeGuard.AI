def calculate_risk(age: int, sugar: float, is_diabetic: bool):
    if is_diabetic or (sugar > 120 and age > 40):
        return "High Risk"
    return "Low Risk"