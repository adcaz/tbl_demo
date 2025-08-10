# Démo de Table avec Streamlit

Cette application est une démonstration simple qui permet d'afficher et de filtrer des données provenant d'un fichier CSV ou d'une feuille Google Sheets à l'aide de [Streamlit](https://streamlit.io/).

## Fonctionnalités
- Chargement des données depuis un fichier CSV ou une feuille Google Sheets.
- Affichage des données dans une table interactive.
- Filtres dynamiques sur les colonnes sélectionnées.
- Bouton pour réinitialiser tous les filtres.

## Installation

### 1. Installer les dépendances
Assurez-vous d'avoir Python installé sur votre machine. Ensuite, installez les dépendances nécessaires :

```bash
pip install -r requirements.txt
```

### 2. Configurer l'authentification Google Sheets

Pour accéder aux données Google Sheets, suivez les étapes ci-dessous :

1. **Créer un projet Google Cloud** :
   - Rendez-vous sur [Google Cloud Console](https://console.cloud.google.com/).
   - Créez un nouveau projet ou sélectionnez un projet existant.

2. **Activer l'API Google Sheets** :
   - Dans le menu de navigation, allez dans **API et services > Bibliothèque**.
   - Recherchez "Google Sheets API" et cliquez sur **Activer**.

3. **Créer un compte de service** :
   - Allez dans **API et services > Identifiants**.
   - Cliquez sur **Créer des identifiants** et sélectionnez **Compte de service**.
   - Remplissez les informations requises et cliquez sur **Créer et continuer**.

4. **Attribuer des rôles au compte de service** :
   - Lors de la création du compte de service, attribuez-lui le rôle **Éditeur** ou un rôle personnalisé avec les permissions nécessaires.

5. **Générer une clé JSON** :
   - Une fois le compte de service créé, allez dans la section **Clés**.
   - Cliquez sur **Ajouter une clé > Créer une clé** et sélectionnez le format JSON.
   - Téléchargez le fichier JSON et placez-le dans le dossier `.streamlit` de votre projet.
   - Renommez le fichier si nécessaire (par exemple, `main-composite-...json`).

6. **Partager la feuille Google Sheets avec le compte de service** :
   - Ouvrez votre feuille Google Sheets.
   - Cliquez sur **Partager** et ajoutez l'adresse e-mail du compte de service (elle se termine généralement par `@<project-id>.iam.gserviceaccount.com`).
   - Donnez-lui les permissions nécessaires (par exemple, **Lecteur** ou **Éditeur**).

7. **Ajouter les informations d'identification au fichier secrets.toml** :
   - **Localement** :
     - Ouvrez ou créez un fichier `secrets.toml` dans le dossier `.streamlit` de votre projet.
     - Ajoutez le contenu du fichier JSON sous la clé `gspread_creds` :
       ```toml
       [gspread_creds]
       type = "service_account"
       project_id = "<project-id>"
       private_key_id = "<private-key-id>"
       private_key = "<private-key>"
       client_email = "<client-email>"
       client_id = "<client-id>"
       auth_uri = "https://accounts.google.com/o/oauth2/auth"
       token_uri = "https://oauth2.googleapis.com/token"
       auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
       client_x509_cert_url = "<client-cert-url>"
       ```
   - **Sur Streamlit Community Cloud** :
     - Allez dans les paramètres de votre application sur [Streamlit Community Cloud](https://streamlit.io/cloud).
     - Ajoutez le contenu du fichier JSON comme variable secrète sous la clé `GSHEET_CREDENTIALS`.

### 3. Lancer l'application
Exécutez la commande suivante pour démarrer l'application :

```bash
streamlit run main.py
```

## Structure des fichiers
- `main.py` : Point d'entrée de l'application Streamlit.
- `pages/` : Contient les différentes pages de l'application.
  - `public_source.py` : Page publique pour afficher les données.
  - `protected_user.py` : Page protégée par un mot de passe en lecture seule.
  - `protected_admin.py` : Page protégée par un mot de passe avec lecture et écriture.
- `utils/` : Contient les utilitaires.
  - `filters.py` : Affichage dynamique des filtres.
  - `require_password.py` : Protège une page avec un mot de passe. 
- `.gitignore` : Fichier pour ignorer les fichiers inutiles dans le dépôt Git.

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---
N'hésitez pas à modifier le CSV, la feuille Google Sheets ou le code de l'application pour vos propres expériences !
