def calculate_risk(age: int, sugar: float, is_diabetic: bool):
    if is_diabetic or (sugar > 120 and age > 40):
        return "High Risk"
    return "Low Risk"
def calculate_bmi(weight_kg: float, height_m: float):
    # Formula: weight / (height * height)
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)
