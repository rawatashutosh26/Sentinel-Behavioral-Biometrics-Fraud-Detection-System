# 🛡️ Sentinel: Behavioral Biometrics & Fraud Detection System

**Tech Stack:** Python, SQL (SQLite), Scikit-Learn (Isolation Forest), Pandas, Excel

<img width="1540" height="659" alt="Screenshot 2026-02-15 155554" src="https://github.com/user-attachments/assets/e83bb4bb-a2c2-4ed9-93fd-15406941bccc" />
*Figure 1: Final Analysis Dashboard showing the clear separation between Human users (clustered left) and Bot anomalies (outliers right).*

---

## 🔍 Project Overview
Sentinel is a real-time anomaly detection engine designed to identify non-human (bot) actors during digital onboarding. Unlike traditional fraud checks that rely on static transaction data, Sentinel analyzes **behavioral biometrics** (mouse velocity, keystroke flight time, and path efficiency) to flag synthetic identities *before* they damage the system.

## 🚀 Key Features
- **ETL Pipeline:** Ingests raw user telemetry logs and normalizes time-series data (handling ms/sec unit mismatches).
- **Behavioral Profiling:** Uses SQL aggregations to calculate `speed_variance`, `max_burst_velocity`, and `path_efficiency`.
- **Unsupervised ML:** Implements an **Isolation Forest** model to detect anomalies without labeled training data.
- **Risk Scoring:** Assigns a risk score to every session; flagged **2 high-risk bot accounts** (Avg Speed > 4000px/s) in a sample of 15,000 users.

---

## 📊 Visual Insights

### 1. Anomaly Detection (The "Bot Cluster")
The scatter plot above visualizes the relationship between **Average Speed** (X-axis) and **Risk Score** (Y-axis). 
- **Humans:** Cluster in the top-left (Low speed, High safety score).
- **Bots:** Isolated in the bottom-right (Impossible speed, Negative risk score).

### 2. Risk Profiling Data
<img width="1009" height="527" alt="Screenshot 2026-02-15 155634" src="https://github.com/user-attachments/assets/47de86f0-4d04-4f52-9841-1e05af841960" />
*Figure 2: The processed output showing specific User IDs flagged as `-1` (Anomaly) by the Isolation Forest model.*

---

## 🛠️ How It Works (The Pipeline)
The project follows a standard Data Analysis lifecycle:

1.  **Data Ingestion (`01_data_cleaning.py`)**: 
    - Merges Train/Test datasets.
    - cleans null values.
    - calculates velocity vectors.
2.  **SQL Analysis (`02_sql_analysis.py`)**: 
    - Loads data into a local SQLite database.
    - Aggregates millions of rows into unique "User Profiles".
3.  **Machine Learning (`03_anomaly_detection.py`)**: 
    - Feeds user profiles into an Isolation Forest.
    - Scores every user from 1 (Normal) to -1 (Anomaly).

---

## ⚙️ Setup & Usage
To run this project locally:

1. **Clone the repo:**
   ```console
   git clone [https://github.com/YOUR_USERNAME/Sentinel_Project.git](https://github.com/YOUR_USERNAME/Sentinel_Project.git)
   ```
2. **Install Dependencies:**

   ```console
   pip install -r requirements.txt
   ```

3. **Run the Pipeline:**

   ```console
   python scripts/01_data_cleaning.py
   python scripts/02_sql_analysis.py
   python scripts/03_anomaly_detection.py
   ```
