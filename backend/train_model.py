import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
# Load the data from your new folder
df = pd.read_csv("dataset/diabetes.csv")

# Look at the first 5 rows to make sure it's correct
print(df.head())
# 1. Separate the Questions (X) from the Answer (y)
X = df.drop(columns=['Outcome'])
y = df['Outcome']

# 2. Split into Study Material (80%) and Final Exam (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Data split successful! AI is ready to study.")

# 1. Create the 'Brain' (The Model)
model = RandomForestClassifier(n_estimators=100, random_state=42)

# 2. Start the 'Study Session' (Training)
model.fit(X_train, y_train)

print("Training Complete! The AI has learned the patterns.")

from sklearn.metrics import accuracy_score

# 1. Ask the AI to guess the answers for the 'Final Exam'
predictions = model.predict(X_test)

# 2. Compare the AI's guesses to the REAL answers
score = accuracy_score(y_test, predictions)

print(f"Model Accuracy: {score * 100:.2f}%")

import joblib

# Save the trained model to a file
joblib.dump(model, "backend/diabetes_model.pkl")

print("Brain saved as 'diabetes_model.pkl'!")