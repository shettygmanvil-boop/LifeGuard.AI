# 🚀 LifeGuard.AI - Backend API Directory

### 1. Dashboard Data
- **Endpoint:** `GET /dashboard/{google_id}`
- [cite_start]**Purpose:** Fetches the user's Health Score and historical lifestyle data from MongoDB[cite: 16, 39].

### 2. AI Risk Prediction
- **Endpoint:** `POST /predict`
- [cite_start]**Purpose:** Analyzes lifestyle inputs (Sleep, Diet, Stress) to predict risks for Diabetes, Hypertension, and more[cite: 15, 69].

### 3. Hospital Finder
- **Endpoint:** `GET /hospitals`
- [cite_start]**Purpose:** Suggests nearby hospitals based on the user's current GPS coordinates using Google Maps[cite: 20, 41].

### 4. Voice Processing
- **Endpoint:** `POST /voice-assist`
- [cite_start]**Purpose:** Handles voice commands for hands-free health checks[cite: 19, 40].