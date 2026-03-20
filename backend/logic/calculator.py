def calculate_risk(age: int, sugar: float):
    if sugar > 120 and age > 40:
        return "High Risk"
    return "Low Risk"