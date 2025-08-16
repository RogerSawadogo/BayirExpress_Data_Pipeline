import streamlit as st
import pandas as pd
import os
import plotly.express as px

# --- Configuration de la page ---
st.set_page_config(page_title="BayirExpress Dashboard", layout="wide")

# --- Fonction pour charger les CSV ---
def load_csv(file_name):
    file_path = os.path.join("data", file_name)
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        st.error(f"Fichier introuvable : {file_name}")
        return pd.DataFrame()

# --- Chargement des données ---
df_users = load_csv("users.csv")
if not df_users.empty and "phone_number" in df_users.columns:
    df_users["phone_number"] = df_users["phone_number"].astype(str)

df_annonces = load_csv("annonces.csv")

# --- Prétraitement : conversion des dates ---
for df in [df_users, df_annonces]:
    if "createdAt" in df.columns:
        df["createdAt"] = pd.to_datetime(df["createdAt"], errors="coerce")

# --- Barre latérale ---
st.sidebar.title("📊 Navigation")
view = st.sidebar.radio("Sélectionner une vue :", ["👥 Utilisateurs", "📦 Annonces", "📈 Statistiques globales"])

st.title("📌 Dashboard BayirExpress")

# ----------------- VUE UTILISATEURS -----------------
if view == "👥 Utilisateurs":
    if "city" in df_users.columns and not df_users.empty:
        col1, col2 = st.columns(2)

        with col1:
            top_cities = df_users["city"].value_counts().head(5)
            fig = px.bar(
                top_cities,
                x=top_cities.index,
                y=top_cities.values,
                title="🏙️ Top villes des utilisateurs",
                labels={"x": "Ville", "y": "Nombre"}
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            pie_data = df_users["city"].value_counts().reset_index()
            pie_data.columns = ["Ville", "Nombre"]
            fig = px.pie(pie_data, names="Ville", values="Nombre", title="Répartition par ville")
            st.plotly_chart(fig, use_container_width=True)

    st.subheader("👥 Liste des utilisateurs")
    st.dataframe(df_users.fillna(""), use_container_width=True)
    st.markdown(f"**Total utilisateurs :** {len(df_users)}")

# ----------------- VUE ANNONCES -----------------
elif view == "📦 Annonces":
    if not df_annonces.empty:
        col1, col2 = st.columns(2)

        if "annonce_type" in df_annonces.columns:
            with col1:
                annonce_counts = df_annonces["annonce_type"].value_counts()
                fig = px.bar(
                    annonce_counts,
                    x=annonce_counts.index,
                    y=annonce_counts.values,
                    title="Répartition des types d'annonces",
                    labels={"x": "Type d'annonce", "y": "Nombre"}
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                pie_data = df_annonces["annonce_type"].value_counts().reset_index()
                pie_data.columns = ["Type", "Nombre"]
                fig = px.pie(pie_data, names="Type", values="Nombre", title="Part des types d'annonces")
                st.plotly_chart(fig, use_container_width=True)

        if "depart_city" in df_annonces.columns:
            col3, col4 = st.columns(2)
            with col3:
                depart_counts = df_annonces["depart_city"].value_counts().head(5)
                fig = px.bar(depart_counts, x=depart_counts.index, y=depart_counts.values,
                             title="Top villes de départ")
                st.plotly_chart(fig, use_container_width=True)

            with col4:
                arrivee_counts = df_annonces["arrivee_city"].value_counts().head(5)
                fig = px.bar(arrivee_counts, x=arrivee_counts.index, y=arrivee_counts.values,
                             title="Top villes d'arrivée")
                st.plotly_chart(fig, use_container_width=True)

    st.subheader("📦 Annonces publiées")
    st.dataframe(df_annonces.fillna(""), use_container_width=True)
    st.markdown(f"**Total annonces :** {len(df_annonces)}")

# ----------------- STATISTIQUES GLOBALES -----------------
elif view == "📈 Statistiques globales":
    st.subheader("📈 Vue d'ensemble")

    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Utilisateurs", len(df_users))
    col2.metric("📦 Annonces", len(df_annonces))
    if "annonce_type" in df_annonces.columns:
        col3.metric("🛒 Types d'annonces", df_annonces["annonce_type"].nunique())

    # Harmonisation des noms de colonnes dates
    # --- Harmonisation colonnes dates ---
    if "created_at" in df_annonces.columns:
        df_annonces.rename(columns={"created_at": "createdAt"}, inplace=True)
    elif "date" in df_annonces.columns:
        df_annonces.rename(columns={"date": "createdAt"}, inplace=True)

    # --- Conversion en datetime ---
    for df in [df_users, df_annonces]:
        if "createdAt" in df.columns:
            df["createdAt"] = pd.to_datetime(df["createdAt"], errors="coerce")

    # --- Comptage journalier ---
    if "createdAt" in df_annonces.columns and "createdAt" in df_users.columns:
        # Utilisateurs
        users_per_day = df_users.groupby(df_users["createdAt"].dt.date).size()
        users_per_day = users_per_day.asfreq("D", fill_value=0) if hasattr(users_per_day, 'asfreq') else users_per_day.reindex(
            pd.date_range(users_per_day.index.min(), users_per_day.index.max(), freq="D"), fill_value=0
        )
        users_cumulative = users_per_day.cumsum()

        # Annonces
        annonces_per_day = df_annonces.groupby(df_annonces["createdAt"].dt.date).size()
        annonces_per_day = annonces_per_day.asfreq("D", fill_value=0) if hasattr(annonces_per_day, 'asfreq') else annonces_per_day.reindex(
            pd.date_range(annonces_per_day.index.min(), annonces_per_day.index.max(), freq="D"), fill_value=0
        )
        annonces_cumulative = annonces_per_day.cumsum()

        # DataFrame pour le graphique
        evolution_df = pd.DataFrame({
            "Utilisateurs cumulés": users_cumulative,
            "Annonces cumulées": annonces_cumulative
        })

        # Graphique journalier cumulatif
        fig = px.line(
            evolution_df,
            x=evolution_df.index,
            y=["Utilisateurs cumulés", "Annonces cumulées"],
            title="📈 Évolution journalière cumulative des utilisateurs et annonces",
            markers=True
        )
        fig.update_layout(xaxis_title="Jour", yaxis_title="Nombre total")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Impossible d'afficher l'évolution : colonnes dates manquantes")
