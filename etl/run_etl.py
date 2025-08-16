from extract import extract_collection
from transform import clean_users, clean_annonces
from load import load_to_csv

def run_etl():
    # Users
    df_users = extract_collection("users")
    df_users_clean = clean_users(df_users)
    load_to_csv(df_users_clean, "users_cleaned.csv")

    

    # Annonces
    df_annonces = extract_collection("annonces")
    df_annonces_clean = clean_annonces(df_annonces)
    load_to_csv(df_annonces_clean, "annonces_cleaned.csv")

    print("🎉 ETL terminé avec succès.")

if __name__ == "__main__":
    run_etl()
