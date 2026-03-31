from database.db import collection # This imports your MongoDB connection

async def get_user_health_history(google_id: str):
    """Retrieves real health logs from MongoDB Cloud."""
    # Search the cloud collection for matches
    cursor = collection.find({"google_id": google_id}).sort("timestamp", -1)
    
    # Convert MongoDB results into a list for Postman
    history = []
    async for document in cursor:
        history.append({
            "score": document.get("prediction_score"),
            "date": document.get("timestamp"),
            "risk": document.get("risk_level")
        })
    return history