# 🎯 Prédiction de Tumeurs du Sein avec Streamlit

Bienvenue dans ce projet de **diagnostic prédictif de tumeurs du sein** à l’aide d’un modèle de machine learning.  
Ce projet a été réalisé dans le cadre d’un Projet de Fin d’Études (PFE) et propose une application web interactive permettant de :

✅ Saisir manuellement les caractéristiques d'une tumeur  
✅ Obtenir instantanément une prédiction (bénigne ou maligne)  
✅ Analyser l'historique des prédictions  
✅ Réaliser des prédictions en masse via des fichiers CSV  
✅ Sécuriser l’accès via une authentification par mot de passe

---

## 📊 Objectif du projet

L'objectif est de développer un outil fiable et intuitif pour **aider à la détection précoce du cancer du sein**, en exploitant l'apprentissage automatique et les technologies web modernes.

---

## 🧪 Technologies utilisées

- **Python 3**
- **Streamlit** – Interface web simple et rapide
- **Scikit-learn** – Modélisation avec Random Forest
- **Pandas / NumPy** – Manipulation de données
- **Matplotlib / Seaborn** – Visualisation des données
- **SQLite3** – Stockage des utilisateurs et prédictions
- **bcrypt** – Authentification sécurisée par hachage de mot de passe
- **Joblib** – Sérialisation du modèle et du scaler

---

## 🧠 Modèle Machine Learning

Le modèle utilisé est un **Random Forest Classifier** entraîné sur la base de données **Breast Cancer Wisconsin (Diagnostic)**.  
Il a été évalué selon plusieurs métriques : F1-Score, Précision, Rappel, Matrice de confusion.

---

## 🚀 Démarrer l’application

### 1. Cloner le projet (ou copier le dossier)
```bash
git clone <url-du-dépôt>
cd streamlit-tumeur-prediction
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv
venv\Scripts\activate  # Sur Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Lancer l’application Streamlit
```bash
streamlit run app.py
```

---

## 🔐 Authentification

Les utilisateurs doivent s’enregistrer ou se connecter via un formulaire sécurisé.  
Les mots de passe sont stockés sous forme chiffrée grâce à `bcrypt` dans une base de données locale (`SQLite`).

---

## 📝 Exemple de prédiction

- Entrée de 30 caractéristiques via des champs numériques
- Affichage d’un message stylisé indiquant le résultat :
  - 🔴 Tumeur maligne
  - 🟢 Tumeur bénigne
- Affichage de la **probabilité** de prédiction
- Sauvegarde automatique dans l’historique personnel

---
## 📂 Structure du projet

```
streamlit-tumeur-prediction/
│
├── app.py                    # Application principale Streamlit
├── requirements.txt         # Dépendances
├── README.md                # Présentation du projet
├── model/
│   ├── random_forest_model.pkl
│   └── scaler.pkl
├── data/
│   ├── users.db             # Base de données utilisateurs
│   ├── historique.db        # Historique des prédictions
│   └── last_user.txt
```


```

---

## 👩‍💻 Réalisé par

Aya Nil & Nouha Aitsaad  
Projet réalisé dans le cadre du PFE – 2025  
Encadré par : PROF MARIA EL BADAOUI
---

## 🧠 Remerciements

Merci à notre établissement et notre encadrante pour le soutien et l'accompagnement dans la réalisation de ce projet.  
Une pensée particulière à toutes les personnes concernées par le cancer du sein 💗
