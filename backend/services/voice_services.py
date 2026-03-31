def process_voice_command(text: str):
    """Simple keyword brain to understand user intent."""
    text = text.lower()
    
    if "risk" in text or "diabetes" in text:
        return "redirect_to_prediction"
    elif "score" in text or "health" in text:
        return "show_health_dashboard"
    elif "hospital" in text or "help" in text:
        return "open_hospital_map"
    else:
        return "general_query"