"""----------- Author : LARDILLIER Léo / GREGOIRE Louna -------------"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QFrame, QGridLayout, QScrollArea)
from PyQt5.QtCore import Qt, pyqtSignal
from ui.styles import *


class FavorisPage(QWidget):
    """Page affichant les articles favoris de l'acheteur."""

    article_clique = pyqtSignal(object)

    def __init__(self, plateforme, utilisateur):
        super().__init__()
        self.plateforme = plateforme
        self.utilisateur = utilisateur
        self.setStyleSheet(f"background-color: {BG_COLOR};")
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(15)

        titre = QLabel("FAVORIS")
        titre.setStyleSheet(label_accent(28) + " letter-spacing: 3px;")
        layout.addWidget(titre)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: transparent;")

        self.container = QWidget()
        self.container.setStyleSheet("background: transparent;")
        self.grid = QGridLayout(self.container)
        self.grid.setSpacing(15)
        self.grid.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        scroll.setWidget(self.container)
        layout.addWidget(scroll)

    def _charger_favoris(self):
        # Vider la grille
        for i in reversed(range(self.grid.count())):
            w = self.grid.itemAt(i).widget()
            if w:
                w.setParent(None)

        acheteur = self.plateforme.en_tant_que_acheteur(self.utilisateur)

        if not acheteur.favoris:
            vide = QLabel("Aucun favori pour l'instant.")
            vide.setStyleSheet(label_dim(14))
            self.grid.addWidget(vide, 0, 0)
            return

        for i, article in enumerate(acheteur.favoris):
            frame = QFrame()
            frame.setFixedSize(185, 255)
            frame.setStyleSheet(f"background-color: {CARD_COLOR}; border-radius: 4px;")
            fl = QVBoxLayout(frame)
            fl.setContentsMargins(0, 0, 0, 8)
            fl.setSpacing(5)

            # Photo
            photo = QLabel("📷")
            photo.setFixedHeight(165)
            photo.setAlignment(Qt.AlignCenter)
            photo.setStyleSheet(photo_placeholder_style())
            fl.addWidget(photo)

            # Nom
            nom = QLabel(article.nom.upper())
            nom.setStyleSheet(label_accent(9) + " letter-spacing: 1px;")
            nom.setAlignment(Qt.AlignCenter)
            nom.setWordWrap(True)
            nom.setMaximumHeight(30)
            fl.addWidget(nom)

            # Prix
            prix = QLabel(f"{article.prix_vendeur}€")
            prix.setStyleSheet(label_white(11))
            prix.setAlignment(Qt.AlignCenter)
            fl.addWidget(prix)

            # Boutons ACHETER + supprimer
            btn_row = QHBoxLayout()
            btn_row.setContentsMargins(8, 0, 8, 0)

            btn_acheter = QPushButton("ACHETER")
            btn_acheter.setStyleSheet(f"""
                QPushButton {{
                    color: {ACCENT_COLOR}; background: transparent;
                    border: 1px solid {ACCENT_COLOR}; border-radius: 10px;
                    padding: 3px 10px; font-size: 9px; font-weight: bold; letter-spacing: 1px;
                }}
                QPushButton:hover {{
                    background-color: {ACCENT_COLOR}; color: {BG_COLOR};
                }}
            """)
            btn_acheter.clicked.connect(lambda checked, a=article: self.article_clique.emit(a))

            btn_sup = QPushButton("🗑")
            btn_sup.setStyleSheet(
                f"background: transparent; border: none; color: {DIM_COLOR}; font-size: 15px;"
            )
            btn_sup.clicked.connect(lambda checked, a=article: self._retirer(a))

            btn_row.addWidget(btn_acheter)
            btn_row.addStretch()
            btn_row.addWidget(btn_sup)
            fl.addLayout(btn_row)

            self.grid.addWidget(frame, i // 5, i % 5)

    def _retirer(self, article):
        acheteur = self.plateforme.en_tant_que_acheteur(self.utilisateur)
        acheteur.retirer_favori(article)
        self._charger_favoris()

    def showEvent(self, event):
        super().showEvent(event)
        self._charger_favoris()
