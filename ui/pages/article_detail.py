"""----------- Author : LARDILLIER Léo / GREGOIRE Louna -------------"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QMessageBox, QInputDialog)
from PyQt5.QtCore import Qt, pyqtSignal
from ui.styles import *


class ArticleDetailPage(QWidget):
    """Page de détail d'un article avec boutons Favoris et Acheter."""

    vendeur_clique = pyqtSignal(object)
    retour = pyqtSignal()

    def __init__(self, plateforme, utilisateur):
        super().__init__()
        self.plateforme = plateforme
        self.utilisateur = utilisateur
        self.article = None
        self._vendeur = None
        self.setStyleSheet(f"background-color: {BG_COLOR};")
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(40)

        # --- PHOTO gauche ---
        left = QVBoxLayout()
        left.setAlignment(Qt.AlignTop)

        self.photo = QLabel("📷")
        self.photo.setFixedSize(320, 380)
        self.photo.setAlignment(Qt.AlignCenter)
        self.photo.setStyleSheet(photo_placeholder_style() + " font-size: 80px;")
        self.photo.setScaledContents(False)
        left.addWidget(self.photo)
        left.addStretch()
        layout.addLayout(left)

        # --- INFOS droite ---
        right = QVBoxLayout()
        right.setSpacing(12)
        right.setAlignment(Qt.AlignTop)

        self.label_nom = QLabel()
        self.label_nom.setStyleSheet(label_accent(22))
        right.addWidget(self.label_nom)

        self.label_desc = QLabel()
        self.label_desc.setStyleSheet(label_dim(12))
        self.label_desc.setWordWrap(True)
        right.addWidget(self.label_desc)

        # Champs détail
        self.champs = {}
        for clé, label in [("taille", "TAILLE"), ("couleur", "COULEUR"),
                            ("matiere", "MATIÈRE"), ("etat", "ÉTAT"), ("marque", "MARQUE")]:
            row = QHBoxLayout()
            lbl = QLabel(f"{label}:")
            lbl.setStyleSheet(label_white(13) + " font-weight: bold; letter-spacing: 2px;")
            lbl.setFixedWidth(90)
            val = QLabel()
            val.setStyleSheet(label_white(13) + " letter-spacing: 1px;")
            self.champs[clé] = val
            row.addWidget(lbl)
            row.addWidget(val)
            row.addStretch()
            right.addLayout(row)

        # Prix
        self.label_prix = QLabel()
        self.label_prix.setStyleSheet(label_accent(20))
        right.addWidget(self.label_prix)

        # Bouton vendeur (cliquable)
        self.btn_vendeur = QPushButton()
        self.btn_vendeur.setStyleSheet(f"""
            QPushButton {{
                color: {PINK_COLOR}; background: transparent;
                border: none; font-size: 14px; text-align: left;
                letter-spacing: 1px;
            }}
            QPushButton:hover {{ color: {WHITE}; }}
        """)
        self.btn_vendeur.clicked.connect(self._voir_vendeur)
        right.addWidget(self.btn_vendeur)

        right.addStretch()

        # Boutons action
        btns = QVBoxLayout()
        btns.setSpacing(12)

        self.btn_favoris = QPushButton("+ FAVORIS")
        self.btn_favoris.setStyleSheet(btn_accent_style())
        self.btn_favoris.setFixedWidth(180)
        self.btn_favoris.clicked.connect(self._toggle_favori)
        btns.addWidget(self.btn_favoris)

        self.btn_acheter = QPushButton("ACHETER")
        self.btn_acheter.setStyleSheet(btn_accent_style())
        self.btn_acheter.setFixedWidth(180)
        self.btn_acheter.clicked.connect(self._faire_offre)
        btns.addWidget(self.btn_acheter)

        right.addLayout(btns)
        layout.addLayout(right)

    def set_article(self, article):
        """Met à jour la page avec les données de l'article."""
        self.article = article
        pix = charger_pixmap(getattr(article, 'photo', None), 320, 380)
        if pix:
            self.photo.setPixmap(pix)
            self.photo.setText("")
            self.photo.setStyleSheet("")
        else:
            self.photo.clear()
            self.photo.setText("📷")
            self.photo.setStyleSheet(photo_placeholder_style() + " font-size: 80px;")
        self.label_nom.setText(article.nom.upper())
        self.label_desc.setText(article.description or "")
        self.champs["taille"].setText(getattr(article, "taille", "-") or "-")
        self.champs["couleur"].setText(getattr(article, "couleur", "-") or "-")
        self.champs["matiere"].setText(getattr(article, "matiere", "-") or "-")
        self.champs["etat"].setText(article.etat or "-")
        self.champs["marque"].setText(getattr(article, "marque", "-") or "-")
        self.label_prix.setText(f"PRIX: {article.prix_vendeur}€")

        vendeur = self.plateforme.trouver_utilisateur_id(article.id_vendeur)
        self._vendeur = vendeur
        if vendeur:
            self.btn_vendeur.setText(f"👤 @{vendeur.pseudo}")
        else:
            self.btn_vendeur.setText("@vendeur inconnu")

        acheteur = self.plateforme.en_tant_que_acheteur(self.utilisateur)
        deja = any(a.id == article.id for a in acheteur.favoris)
        self.btn_favoris.setText("♥ FAVORIS" if deja else "+ FAVORIS")

        if article.vendu:
            self.btn_acheter.setText("VENDU")
            self.btn_acheter.setEnabled(False)
        else:
            self.btn_acheter.setText("ACHETER")
            self.btn_acheter.setEnabled(True)

    def _voir_vendeur(self):
        if self._vendeur:
            self.vendeur_clique.emit(self._vendeur)

    def _toggle_favori(self):
        """Ajoute ou retire l'article des favoris de l'utilisateur connecté et met à jour le bouton."""
        if not self.article:
            return
        acheteur = self.plateforme.en_tant_que_acheteur(self.utilisateur)
        deja = any(a.id == self.article.id for a in acheteur.favoris)
        if deja:
            acheteur.retirer_favori(self.article)
            self.btn_favoris.setText("+ FAVORIS")
        else:
            acheteur.ajouter_favori(self.article)
            self.btn_favoris.setText("♥ FAVORIS")

    def _faire_offre(self):
        if not self.article:
            return
        if self.article.vendu:
            QMessageBox.warning(self, "Indisponible", "Cet article a déjà été vendu.")
            return
        prix, ok = QInputDialog.getDouble(
            self, "Faire une offre",
            f"Prix vendeur: {self.article.prix_vendeur}€  |  Prix min: {self.article.prix_min}€\n\nVotre offre (€):",
            self.article.prix_vendeur, 0, 99999, 2
        )
        if ok:
            from services.matching import proposer_achat
            acheteur = self.plateforme.en_tant_que_acheteur(self.utilisateur)
            statut = proposer_achat(acheteur, self.article, prix)
            messages = {
                "acceptee": "Offre acceptée ! L'article vous appartient.",
                "negociation": "Négociation proposée. Le vendeur va vous contacter.",
                "refusee": "Offre refusée. Essayez un prix plus élevé."
            }
            QMessageBox.information(self, "Résultat de l'offre", messages.get(statut, statut))
            if statut == "acceptee":
                self.btn_acheter.setText("VENDU")
                self.btn_acheter.setEnabled(False)
