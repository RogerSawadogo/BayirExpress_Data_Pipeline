import pandas as pd

def clean_users(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop(columns=["_id", "password"], errors="ignore")
    df = df.rename(columns={
        "username": "name",
        "email": "email",
        "phone": "phone_number",
        "city": "city"
    })
    return df

def clean_annonces(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop(columns=["_id"], errors="ignore")
    df = df.rename(columns={
        "type": "annonce_type",
        "description": "annonce_description",
        "ville_depart": "depart_city",
        "ville_arrivee": "arrival_city",
        "date_depart": "departure_date",
        "poids_disponible": "available_weight",
        "devise": "currency",
        "createdAt": "created_at",
    })
    if "departure_date" in df.columns:
        df["departure_date"] = pd.to_datetime(df["departure_date"], errors="coerce")
    if "created_at" in df.columns:
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    return df
