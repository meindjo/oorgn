# meindjo - Page de connexion (Flask)

Application Flask simple qui reproduit une page de connexion en deux étapes (email → mot de passe) au style Orange.

## Structure

```
meindjo/
├── app.py                      # Application Flask
├── requirements.txt            # Dépendances Python
├── templates/
│   ├── login_email.html        # Étape 1 : saisie de l'email
│   ├── login_password.html     # Étape 2 : saisie du mot de passe
│   └── success.html            # Page "Connexion réussie"
└── static/
    └── style.css               # Styles CSS
```

## Installation

```bash
pip install -r requirements.txt
```

## Lancement

```bash
python app.py
```

Puis ouvrir : http://localhost:5000

## Identifiants valides

- **Email** : `dadoumeindjo@meindjo.fr`
- **Mot de passe** : `Admin123@`

Toute autre combinaison affiche : **mot de passe incorrect**
