# Replace the old localhost line with your real Cloud URL
MONGODB_URL = "mongodb+srv://shettygmanvil_db_user:P8aMR8XoMQaAxGmj@cluster0.td8fpvn.mongodb.net/?appName=Cluster0"

from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(MONGODB_URL)
database = client.lifeguard_db
collection = database.health_history
async def save_health_result(result_data: dict):
    # This line 'Inserts' a single document into your Cloud Folder
    await collection.insert_one(result_data)
    return True