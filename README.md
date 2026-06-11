# ENST'AS DU STYLE

Marketplace de vêtements entre étudiants de l'ENSTA campus de Brest.  
Application desktop Python/PyQt5 avec base de données SQLite.

---

## Prérequis

- Python 3.9+
- Les dépendances listées ci-dessous

```bash
pip install PyQt5 numpy pillow
```

---

## Lancement

```bash
python main_app.py
```

---

## Comptes de test

| Pseudo | Mot de passe | Rôle |
|---|---|---|
| `superadmin` | `superadmin` | Administrateur |
| `bob_style` | `bobstyle99` | Utilisateur |
| `sophie_mode` | `sophie2025` | Utilisateur |

---

## Structure du projet

```
ENSTADUSTYLE/
├── main_app.py              # Point d'entrée
├── db/
│   ├── db.py                # Toutes les fonctions CRUD (SQLite)
│   └── marche.db            # Base de données principale
├── models/
│   ├── article.py           # Article, Vetement
│   ├── utilisateur.py       # Utilisateur, Vendeur, Acheteur
│   ├── transaction.py       # Transaction
│   └── plateforme.py        # Plateforme (contrôleur central, extends Observable)
├── services/
│   ├── observer.py          # Pattern Observer (Observable, Observateur)
│   ├── matching.py          # Algorithme de négociation de prix
│   ├── recherche.py         # Scoring vectoriel NumPy des articles
│   └── recommendation.py   # Recommandations personnalisées
├── ui/
│   ├── main_window.py       # Fenêtre principale + navigation
│   ├── login_window.py      # Écran de connexion
│   ├── styles.py            # Feuilles de style globales
│   └── pages/
│       ├── catalogue.py     # Grille des articles disponibles
│       ├── profil.py        # Profil utilisateur + gestion des annonces
│       ├── article_detail.py# Fiche article + offre d'achat
│       ├── vendeur_profil.py# Profil public d'un vendeur
│       ├── vendre.py        # Formulaire de mise en vente
│       ├── favoris.py       # Liste des favoris
│       ├── filtres.py       # Recherche par critères
│       └── notifications.py # Notifications d'abonnements
├── assets/
│   └── photos/              # Photos des articles et avatars utilisateurs
└── test/
    ├── test_observer.py           # Tests unitaires — pattern Observer
    ├── test_db_fonctionnalites.py # Tests unitaires — fonctions DB
    └── test_matching_recherche.py # Tests unitaires — matching et recherche
```

---

## Fonctionnalités principales

- **Catalogue** — parcourir les articles disponibles avec pagination
- **Vendre** — mettre un article en vente avec photo, taille, couleur, prix
- **Offre d'achat** — négociation de prix (acceptée / négociation / refusée)
- **Favoris** — ajouter / retirer des articles
- **Abonnements** — suivre un vendeur (social)
- **Notifications** — recevoir une alerte quand un article correspond à des critères sauvegardés (pattern Observer)
- **Profil** — modifier ses informations, ses articles et sa photo

---

## Auteurs

- LARDILLIER Léo
- GREGOIRE Louna
