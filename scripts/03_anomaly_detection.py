import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib 
import os

INPUT_PROFILE = "data/processed/user_risk_profiles.csv"
MODEL_PATH = "models/sentinel_isolation_forest.pkl"
OUTPUT_SCORES = "data/processed/final_fraud_scores.csv"

def train_model():
    print("AI Anomaly Detection...")
    try:
        df = pd.read_csv(INPUT_PROFILE)
        print(f"Loaded profiles for {len(df)} users.")
    except FileNotFoundError:
        print("ERROR: User profiles not found. Run script 02 first!")
        return
    features = ['avg_speed', 'speed_variance', 'max_burst_speed']
    scaler = StandardScaler()
    X = scaler.fit_transform(df[features])
    print("Training Isolation Forest Model...")
    model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
    model.fit(X)
    df['anomaly_label'] = model.predict(X)
    df['risk_score'] = model.decision_function(X) 
    bots = df[df['anomaly_label'] == -1]
    humans = df[df['anomaly_label'] == 1]
    
    print(f"\n--- SENTINEL AI RESULTS ---")
    print(f"Total Users Analyzed: {len(df)}")
    print(f"Detected BOTS:   {len(bots)}  (High Risk)")
    print(f"Detected HUMANS: {len(humans)} (Normal Behavior)")
    
    print("\n TOP 5 SUSPECTED BOTS ---")
    print(bots.sort_values(by='risk_score').head(5)[['user_id', 'avg_speed', 'risk_score']])

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    
    df.to_csv(OUTPUT_SCORES, index=False)
    print(f"\nSuccess! Final fraud scores saved to {OUTPUT_SCORES}")
    print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_model()