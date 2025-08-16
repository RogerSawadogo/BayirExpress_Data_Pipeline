import pandas as pd
import os

def load_to_csv(df: pd.DataFrame, filename: str):
    output_dir = "/opt/airflow/project/data"
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, filename)
    df.to_csv(path, index=False)
    print(f"✅ Sauvegardé : {path}")
