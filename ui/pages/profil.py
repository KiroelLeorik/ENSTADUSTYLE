"""----------- Author : LARDILLIER Léo / GREGOIRE Louna -------------"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QFrame, QGridLayout, QScrollArea)
from PyQt5.QtCore import Qt
from ui.styles import *


class ProfilPage(QWidget):
    """Page profil de l'utilisateur connecté."""

    def __init__(self, plateforme, utilisateur):
        super().__init__()
        self.plateforme = plateforme
        self.utilisateur = utilisateur
        self.setStyleSheet(f"background-color: {BG_COLOR};")
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(50)

        # --- GAUCHE ---
        left = QVBoxLayout()
        left.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        left.setSpacing(14)

        # Avatar rose
        avatar = QLabel("👤")
        avatar.setFixedSize(180, 180)
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setStyleSheet(
            f"background-color: {PINK_COLOR}; border-radius: 90px; font-size: 75px;"
        )
        left.addWidget(avatar, alignment=Qt.AlignCenter)

        # Pseudo
        pseudo = QLabel(f"@{self.utilisateur.pseudo.upper()}")
        pseudo.setStyleSheet(label_accent(18))
        pseudo.setAlignment(Qt.AlignCenter)
        left.addWidget(pseudo)

        # Stats abonnés / abonnements
        stats = QHBoxLayout()
        stats.setAlignment(Qt.AlignCenter)
        stats.setSpacing(30)
        from db.db import get_nb_abonnes, get_nb_abonnements
        abonnes = get_nb_abonnes(self.utilisateur.id)
        abonnements = get_nb_abonnements(self.utilisateur.id)
        for valeur, libelle in [(abonnes, "ABONNÉS"), (abonnements, "ABONNEMENTS")]:
            col = QVBoxLayout()
            col.setAlignment(Qt.AlignCenter)
            v = QLabel(str(valeur))
            v.setStyleSheet(label_white(18) + " font-weight: bold;")
            v.setAlignment(Qt.AlignCenter)
            l = QLabel(libelle)
            l.setStyleSheet(label_dim(9) + " letter-spacing: 2px;")
            l.setAlignment(Qt.AlignCenter)
            col.addWidget(v)
            col.addWidget(l)
            stats.addLayout(col)
        left.addLayout(stats)

        # Boutons gauche
        for texte in ["PORTE MONNAIE", "MES ANNONCES"]:
            btn = self._btn_texte(texte)
            left.addWidget(btn)

        left.addStretch()
        layout.addLayout(left)

        # --- DROITE ---
        right = QVBoxLayout()
        right.setAlignment(Qt.AlignTop)
        right.setSpacing(10)

        for texte in ["PARAMETRES", "MES EVALUATIONS"]:
            btn = self._btn_texte(texte)
            right.addWidget(btn, alignment=Qt.AlignRight)

        # Grille annonces
        vendeur = self.plateforme.en_tant_que_vendeur(self.utilisateur)
        vendus, en_vente = vendeur.mes_articles()
        tous = en_vente + vendus

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: transparent;")
        scroll.setMaximumHeight(380)

        container = QWidget()
        container.setStyleSheet("background: transparent;")
        grid = QGridLayout(container)
        grid.setSpacing(10)
        grid.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        for i, article in enumerate(tous[:9]):
            frame = QFrame()
            frame.setFixedSize(170, 130)
            frame.setStyleSheet(f"background-color: {MUTED_COLOR}; border-radius: 4px;")
            fl = QVBoxLayout(frame)
            lbl = QLabel(article.nom.upper()[:22])
            lbl.setStyleSheet(label_accent(9) + " letter-spacing: 1px;")
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setWordWrap(True)
            statut = QLabel("VENDU" if article.vendu else "EN VENTE")
            statut.setStyleSheet(
                f"color: {'#ff4444' if article.vendu else '#44ff88'}; font-size: 9px; letter-spacing: 1px;"
            )
            statut.setAlignment(Qt.AlignCenter)
            fl.addStretch()
            fl.addWidget(lbl)
            fl.addWidget(statut)
            grid.addWidget(frame, i // 3, i % 3)

        scroll.setWidget(container)
        right.addWidget(scroll)
        right.addStretch()
        layout.addLayout(right)

    def _btn_texte(self, texte):
        btn = QPushButton(texte)
        btn.setStyleSheet(f"""
            QPushButton {{
                color: {WHITE}; background: transparent; border: none;
                font-size: 13px; font-weight: bold; letter-spacing: 2px;
                padding: 6px 0;
            }}
            QPushButton:hover {{ color: {ACCENT_COLOR}; }}
        """)
        return btn
