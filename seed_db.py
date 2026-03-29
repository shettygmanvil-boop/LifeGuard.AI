import sqlite3
import os

# 1. Ensure the database path is correct (relative to the root)
db_path = 'backend/database/lifeguard.db'

# 2. Connect to the 'Cabinet'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 3. THE FIX: Create the table first!
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

# 4. Now add 'Manvil'
cursor.execute('''
    INSERT OR REPLACE INTO user_profiles (email, full_name, age, gender, target_weight, daily_calorie_goal)
    VALUES (?, ?, ?, ?, ?, ?)
''', ("manvil@bmsit.com", "Manvil", 20, "Male", 70.0, 2200))

# 5. Save and Close
conn.commit()
conn.close()
print("Success! Table created and Manvil's profile seeded.")