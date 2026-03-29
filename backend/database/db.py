import os
import sqlite3
import certifi
from motor.motor_asyncio import AsyncIOMotorClient

# --- 1. MONGODB (Cloud Folder for Health Logs) ---
MONGODB_URL = "mongodb+srv://shettygmanvil_db_user:P8aMR8XoMQaAxGmj@cluster0.td8fpvn.mongodb.net/?appName=Cluster0"

# Using certifi for a secure connection
client = AsyncIOMotorClient(MONGODB_URL, tlsCAFile=certifi.where())
mongodb = client.lifeguard_db
collection = mongodb.health_history

async def save_health_result(result_data: dict):
    """Saves AI prediction results to MongoDB."""
    await collection.insert_one(result_data)
    return True

# --- 2. SQLITE (Local Locker for User Profiles) ---

def get_db_connection():
    """THE KEY: This defines the connection to your local SQL file."""
    db_path = os.path.join(os.path.dirname(__file__), 'lifeguard.db')
    conn = sqlite3.connect(db_path)
    # This makes data easier to handle later
    conn.row_factory = sqlite3.Row 
    return conn

def create_profile_table():
    """The Cabinet Builder: Creates the structure."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profiles (
            email TEXT PRIMARY KEY,
            full_name TEXT,
            age INTEGER,
            gender TEXT,
            target_weight REAL,
            daily_calorie_goal INTEGER,
            joined_date DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_user_profile(profile_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    # We use UPDATE for existing users to ensure we don't create duplicates
    cursor.execute('''
        INSERT OR REPLACE INTO user_profiles (email, full_name, age, gender, target_weight, daily_calorie_goal)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        profile_data['email'], profile_data['full_name'], profile_data['age'],
        profile_data['gender'], profile_data['target_weight'], profile_data['daily_calorie_goal']
    ))
    conn.commit() # This is the "Save Button"
    conn.close()

def get_user_profile(email):
    """The Messenger: Retrieves data by email."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_profiles WHERE email = ?', (email,))
    user_data = cursor.fetchone() 
    conn.close()
    return user_data

# --- 3. INITIALIZATION ---
# This ensures the 'Cabinet' is ready as soon as the app starts
create_profile_table()