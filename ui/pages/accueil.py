"""----------- Author : LARDILLIER Léo / GREGOIRE Louna -------------"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from ui.styles import *


class AccueilPage(QWidget):
    """Page d'accueil avec le logo ENST'AS DU STYLE."""

    def __init__(self, plateforme):
        super().__init__()
        self.plateforme = plateforme
        self.setStyleSheet(f"background-color: {BG_COLOR};")
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(10)

        titre = QLabel("ENST'AS")
        titre.setStyleSheet(
            f"color: {ACCENT_COLOR}; font-size: 80px; font-weight: bold; letter-spacing: 8px;"
        )
        titre.setAlignment(Qt.AlignCenter)
        layout.addWidget(titre)

        sous_titre = QLabel("DU STYLE")
        sous_titre.setStyleSheet(
            f"color: {ACCENT_COLOR}; font-size: 36px; letter-spacing: 14px; font-weight: 300;"
        )
        sous_titre.setAlignment(Qt.AlignCenter)
        layout.addWidget(sous_titre)

        hint = QLabel("≡  Ouvre le menu pour naviguer")
        hint.setStyleSheet(f"color: {DIM_COLOR}; font-size: 13px; margin-top: 40px;")
        hint.setAlignment(Qt.AlignCenter)
        layout.addWidget(hint)
