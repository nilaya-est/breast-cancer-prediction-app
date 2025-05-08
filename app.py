import bcrypt
import sqlite3
import streamlit as st
from datetime import datetime
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import seaborn as sns
import os


# Fonction de vérification
def verify_login(username, password):
    conn = sqlite3.connect("data/users.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password BLOB)")
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    if user:
        if bcrypt.checkpw(password.encode(), user[1]):
            conn.close()
            return True
        else:
            conn.close()
            return False
    else:
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()
        return True

# Authentification
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# 🔁 Reconnexion automatique
if not st.session_state.authenticated:
    if os.path.exists("data/last_user.txt"):
        with open("data/last_user.txt", "r") as f:
            last_user = f.read().strip()
            if last_user:
                st.session_state.authenticated = True
                st.session_state.username = last_user

# Formulaire de connexion
if not st.session_state.authenticated:
    st.title("Page de connexion")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        if verify_login(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            with open("data/last_user.txt", "w") as f:
                f.write(username)
            st.success("Connexion réussie !")
        else:
            st.error("Identifiants incorrects. Essayez à nouveau.")

# Interface principale
if st.session_state.authenticated:
    st.sidebar.success(f"Bienvenue {st.session_state.username}")

    conn = sqlite3.connect("data/historique.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS predictions (
                 user TEXT, date TEXT, features TEXT, prediction TEXT, probability REAL)''')
    conn.commit()

    model = joblib.load("model/random_forest_model.pkl")
    scaler = joblib.load("model/scaler.pkl")

    st.markdown("""<h2 style='color:#003366;'>Interface de prédiction du cancer du sein</h2>""", unsafe_allow_html=True)
    st.write("Saisissez les 30 caractéristiques pour une prédiction individuelle :")

    features = []
    for i in range(1, 31):
        val = st.number_input(f"Caractéristique {i}", value=0.0, format="%.10f")
        features.append(val)

    if st.button("Prédire"):
        X_input = np.array([features])
        X_scaled = scaler.transform(X_input)
        pred = model.predict(X_scaled)[0]
        proba = model.predict_proba(X_scaled)[0][1]

        c.execute("INSERT INTO predictions VALUES (?, ?, ?, ?, ?)",
                  (st.session_state.username, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(features), str(pred), float(proba)))
        conn.commit()

        if pred == 1:
            st.markdown(f"""<div style='background-color:#ffcccc;padding:10px;border-radius:10px'>
                            <b style='color:#cc0000'>🔴 Tumeur maligne détectée (probabilité: {proba:.2f})</b>
                            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div style='background-color:#ccffcc;padding:10px;border-radius:10px'>
                            <b style='color:#006600'>🟢 Tumeur bénigne détectée (probabilité: {1 - proba:.2f})</b>
                            </div>""", unsafe_allow_html=True)

    st.write("---")
    st.subheader("📁 Prédictions en masse via CSV")
    csv_file = st.file_uploader("Uploader votre fichier CSV", type=["csv"])
    if csv_file:
        df = pd.read_csv(csv_file)
        df_scaled = scaler.transform(df)
        predictions = model.predict(df_scaled)
        st.write("Prédictions :", predictions)

    st.write("---")
    st.subheader("📜 Historique des prédictions")
    c.execute("SELECT * FROM predictions WHERE user = ?", (st.session_state.username,))
    rows = c.fetchall()
    if rows:
        df_hist = pd.DataFrame(rows, columns=["Utilisateur", "Date", "Caractéristiques", "Prédiction", "Probabilité"])
        st.dataframe(df_hist)
    else:
        st.info("Aucune prédiction enregistrée.")

    st.write("---")
    st.markdown("""
    <div style='background-color:#f0f8ff; padding: 20px; border-radius: 10px; border: 1px solid #dddddd; box-shadow: 2px 2px 8px rgba(0,0,0,0.1);'>
        <h3 style='color:#003366; text-align:center;'>📘 À propos du projet</h3>
        <p style='text-align:center; color:#333333;'>
            Ce projet utilise un modèle <b>Random Forest</b> pour prédire si une tumeur est <b>bénigne</b> ou <b>maligne</b>,<br>
            à partir de 30 caractéristiques extraites d'imageries médicales.
        </p>
        <p style='text-align:center; color:#555555;'>
            ✅ Interface développée avec <b>Streamlit</b><br>
            ✅ Modèle de machine learning avec <b>scikit-learn</b><br>
            ✅ Authentification sécurisée avec <b>bcrypt</b><br>
            ✅ Stockage de l'historique avec <b>SQLite</b>
        </p>
        <p style='text-align:center; color:#888888;'>
            <i>Développé par AYA NIL & NOUHA AITSAAD</i>
        </p>
    </div>
    """, unsafe_allow_html=True)
