import pandas as pd
import numpy as np
import os

TRAIN_FILE = "data/raw/Train_Mouse.csv"
TEST_FILE = "data/raw/Test_Mouse.csv"
OUTPUT_FILE = "data/processed/cleaned_user_logs.csv"

def clean_data():
    print("Starting Sentinel Data Pipeline...")
    
    try:
        df_train = pd.read_csv(TRAIN_FILE)
        df_train['dataset_type'] = 'train'
        df_test = pd.read_csv(TEST_FILE)
        df_test['dataset_type'] = 'test'
        df = pd.concat([df_train, df_test], ignore_index=True)
        print(f"Successfully loaded {len(df)} raw rows.")
    except FileNotFoundError:
        print("ERROR: Raw files not found.")
        return
    
    df.columns = df.columns.str.strip()
    rename_map = {
        'screen_x': 'mouse_x', 'screen_y': 'mouse_y',
        'Client Timestamp': 'timestamp', 'client_timestamp': 'timestamp', 
        'event_type': 'action_type', 'state': 'action_type'
    }
    df.rename(columns=rename_map, inplace=True)

    print("Calculating Metrics...")
    
    if 'session_id' in df.columns:
        df.sort_values(by=['session_id', 'timestamp'], inplace=True)
    
    df['dt'] = df['timestamp'].diff()
    
    median_dt = df['dt'][df['dt'] > 0].median()
    print(f"DEBUG: Median Time Difference is {median_dt}")

    if median_dt > 10:
        print(">>> DETECTED MILLISECONDS. Converting to Seconds...")
        df['dt'] = df['dt'] / 1000.0

    df = df[df['dt'] < 5.0]
    df = df[df['dt'] > 0] 

    df['dx'] = df['mouse_x'].diff()
    df['dy'] = df['mouse_y'].diff()
    df['distance_pixels'] = np.sqrt(df['dx']**2 + df['dy']**2)
    df['velocity'] = df['distance_pixels'] / df['dt']
    
    df.replace([np.inf, -np.inf], 0, inplace=True)
    df.fillna(0, inplace=True)

    print(f"Saving {len(df)} rows to {OUTPUT_FILE}...")
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True) 
    
    df.to_csv(OUTPUT_FILE, index=False)
    print("Success!")

if __name__ == "__main__":
    clean_data()