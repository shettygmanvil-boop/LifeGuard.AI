def calculate_bmi(weight_kg: float, height_m: float) -> float:
    if not height_m or height_m <= 0:
        return 0.0
    return round(float(weight_kg) / (float(height_m) ** 2), 2)


def _safe(data: dict, key: str):
    val = data.get(key)
    if val is None or val == "":
        return None
    try:
        return float(val)
    except (ValueError, TypeError):
        return None


def calculate_health_score(data: dict):
    score = 100
    reasons = []

    age = int(data.get("age") or 25)
    if age > 50:
        score -= 10
        reasons.append("Age-related risk factor")

    bmi = _safe(data, "BMI")
    if bmi:
        if bmi > 30:
            score -= 15; reasons.append("BMI in Obese range")
        elif bmi > 25:
            score -= 8;  reasons.append("BMI in Overweight range")

    glucose = _safe(data, "Glucose")
    if glucose is not None:
        if glucose > 125:
            score -= 20; reasons.append("Elevated Blood Sugar")
        elif glucose > 100:
            score -= 10; reasons.append("Borderline Blood Sugar")

    bp = _safe(data, "BloodPressure")
    if bp is not None and bp > 90:
        score -= 15; reasons.append("High Blood Pressure")

    insulin = _safe(data, "Insulin")
    if insulin is not None and insulin > 150:
        score -= 10; reasons.append("High Insulin Levels")

    pedigree = _safe(data, "DiabetesPedigreeFunction")
    if pedigree is not None and pedigree > 0.5:
        score -= 10; reasons.append("Genetic Risk Factor (Pedigree)")

    if data.get("is_diabetic") is True:
        score -= 15; reasons.append("Existing Diabetic Condition")

    if data.get("physical_activity") == "Sedentary":
        score -= 10; reasons.append("Low Physical Activity")

    stress = _safe(data, "stress_level")
    if stress and stress > 7:
        score -= 8; reasons.append("High Stress Levels")

    sleep = _safe(data, "sleep_duration")
    if sleep and sleep < 6:
        score -= 7; reasons.append("Poor Sleep Duration")

    if data.get("sugar_intake") == "High":
        score -= 10; reasons.append("High Dietary Sugar")

    if data.get("Smoking_habit") == "Regular":
        score -= 12; reasons.append("Regular Smoking")

    if data.get("Alcohol_consumption") == "Regular":
        score -= 8; reasons.append("Regular Alcohol Intake")

    steps_day = _safe(data, "steps_per_day")
    if steps_day is not None:
        if steps_day < 4000:
            score -= 5; reasons.append("Low daily step count")
        elif steps_day > 8000:
            score += 5

    hr = _safe(data, "heart_rate")
    if hr is not None:
        if hr > 100:
            score -= 5; reasons.append("Elevated resting heart rate")

    return max(0, min(100, score)), reasons if reasons else ["Excellent health markers!"]


def calculate_disease_risks(data: dict) -> dict:
    """
    Returns estimated risk % for 4 diseases based on user data.
    Uses evidence-based heuristic scoring (not ML).
    """
    age    = int(data.get("age") or 25)
    bmi    = _safe(data, "BMI") or 22.0
    glucose = _safe(data, "Glucose") or 90.0
    bp     = _safe(data, "BloodPressure") or 70.0
    pedigree = _safe(data, "DiabetesPedigreeFunction") or 0.3
    smoking = data.get("Smoking_habit", "Non-smoker")
    alcohol = data.get("Alcohol_consumption", "None")
    activity = data.get("physical_activity", "Moderate")
    stress  = _safe(data, "stress_level") or 5
    sugar   = data.get("sugar_intake", "Low")
    salt    = data.get("salt_intake", "Low")
    is_diabetic = data.get("is_diabetic", False)
    steps   = _safe(data, "steps_per_day")
    hr      = _safe(data, "heart_rate")

    # ── TYPE-2 DIABETES ──────────────────────────────────────────────────────
    d2 = 5.0
    if glucose > 125: d2 += 35
    elif glucose > 100: d2 += 18
    if bmi > 30: d2 += 20
    elif bmi > 25: d2 += 10
    if pedigree > 0.5: d2 += 15
    if age > 45: d2 += 10
    if sugar == "High": d2 += 8
    if activity == "Sedentary": d2 += 7
    if is_diabetic: d2 = max(d2, 80)

    # ── HYPERTENSION ─────────────────────────────────────────────────────────
    ht = 5.0
    if bp > 130: ht += 40
    elif bp > 110: ht += 20
    if bmi > 30: ht += 15
    if salt == "High": ht += 12
    if stress > 7: ht += 10
    if smoking == "Regular": ht += 10
    if alcohol == "Regular": ht += 8
    if age > 50: ht += 10

    # ── CARDIOVASCULAR DISEASE ───────────────────────────────────────────────
    cv = 5.0
    if smoking == "Regular": cv += 25
    elif smoking == "Occasional": cv += 10
    if bmi > 30: cv += 15
    if bp > 130: cv += 15
    if glucose > 125: cv += 10
    if alcohol == "Regular": cv += 8
    if activity == "Sedentary": cv += 10
    if age > 50: cv += 12
    if stress > 7: cv += 5

    # ── OBESITY ──────────────────────────────────────────────────────────────
    ob = 5.0
    if bmi > 35: ob += 60
    elif bmi > 30: ob += 40
    elif bmi > 25: ob += 20
    if activity == "Sedentary": ob += 15
    if sugar == "High": ob += 10
    if alcohol == "Regular": ob += 8
    if age > 40: ob += 5
    if steps and steps > 8000: ob = max(0, ob - 10)

    # Bonus offsets
    if steps and steps > 8000:
        d2 = max(0, d2 - 5)
        ht = max(0, ht - 5)
        cv = max(0, cv - 5)

    if hr and hr > 100:
        cv += 10
        ht += 5

    def cap(v): return round(min(v, 97.0), 1)

    return {
        "type2_diabetes":       cap(d2),
        "hypertension":         cap(ht),
        "cardiovascular":       cap(cv),
        "obesity":              cap(ob),
    }


def simulate_improvement(data: dict) -> dict:
    improved = data.copy()
    if improved.get("Glucose"):
        improved["Glucose"] = improved["Glucose"] * 0.80
    if improved.get("BMI"):
        improved["BMI"] = improved["BMI"] * 0.93
    if improved.get("BloodPressure"):
        improved["BloodPressure"] = improved["BloodPressure"] * 0.92
    if not improved.get("Insulin"):
        improved["Insulin"] = 30
    improved["physical_activity"] = "Moderate"
    improved["sugar_intake"] = "Low"
    improved["stress_level"] = max(int(improved.get("stress_level") or 5) - 2, 1)
    improved["sleep_duration"] = max(float(improved.get("sleep_duration") or 7), 7.0)
    return improved


def get_risk_explanations(data: dict):
    _, reasons = calculate_health_score(data)
    return reasons[:3]


def calculate_risk(score: int) -> str:
    if score < 60: return "High Risk"
    if score < 85: return "Moderate Risk"
    return "Low Risk"
