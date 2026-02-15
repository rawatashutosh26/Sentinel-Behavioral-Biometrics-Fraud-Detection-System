import pandas as pd
import sqlite3
import os

INPUT_CSV = "data/processed/cleaned_user_logs.csv"
DB_NAME = "data/sentinel.db"
OUTPUT_REPORT = "data/processed/user_risk_profiles.csv"

def analyze_with_sql():
    print("Starting SQL Analysis Phase...")
    
    try:
        df = pd.read_csv(INPUT_CSV)
        print(f"Loaded {len(df)} rows from CSV.")
    except FileNotFoundError:
        print("ERROR: Cleaned CSV not found. Run script 01 first.")
        return
    conn = sqlite3.connect(DB_NAME)
    
    print("Uploading data to SQL database...")
    df.to_sql('mouse_activity', conn, if_exists='replace', index=False)
    
    print("\nRunning SQL Queries to build User Profiles...")
    
    query = """
    SELECT 
        user_id,
        COUNT(*) as total_actions,
        AVG(velocity) as avg_speed,
        -- SQLite doesn't have STDDEV by default, so we calculate Variance roughly
        -- (In a real Postgres/MySQL DB, you would just use STDDEV(velocity))
        AVG(velocity*velocity) - AVG(velocity)*AVG(velocity) as speed_variance,
        MAX(velocity) as max_burst_speed,
        SUM(distance_pixels) as total_distance
    FROM mouse_activity
    GROUP BY user_id
    HAVING total_actions > 10  -- Filter out noise (sessions with < 10 events)
    ORDER BY avg_speed DESC;
    """

    user_profiles = pd.read_sql_query(query, conn)
    conn.close()
    
    print("\n--- SQL Analysis Results (Top 5 Fastest Users) ---")
    print(user_profiles.head(5))
    user_profiles.to_csv(OUTPUT_REPORT, index=False)
    print(f"\nSuccess! User profiles saved to: {OUTPUT_REPORT}")
    print("You can now visualize this data in Power BI or Excel.")

if __name__ == "__main__":
    analyze_with_sql()