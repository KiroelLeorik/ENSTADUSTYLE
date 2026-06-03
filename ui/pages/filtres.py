"""----------- Author : LARDILLIER Léo / GREGOIRE Louna -------------"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton)
from PyQt5.QtCore import Qt, pyqtSignal
from ui.styles import *


class FiltresPage(QWidget):
    """Page de filtres par catégorie et sous-catégorie."""

    filtres_appliques = pyqtSignal(dict)

    def __init__(self, plateforme):
        super().__init__()
        self.plateforme = plateforme
        self.filtres_actifs = {}
        self.setStyleSheet(f"background-color: {BG_COLOR};")
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 25, 40, 25)
        layout.setSpacing(25)


        titre = QLabel("FILTRES")
        titre.setStyleSheet(label_accent(28) + " letter-spacing: 3px;")
        layout.addWidget(titre)

        cols = QHBoxLayout()
        cols.setSpacing(80)
        cols.setAlignment(Qt.AlignTop)

        # --- CATÉGORIE ---
        cat_col = QVBoxLayout()
        cat_col.setSpacing(14)
        cat_col.setAlignment(Qt.AlignTop)

        cat_lbl = QLabel("CATÉGORIE")
        cat_lbl.setStyleSheet(label_white(16) + " font-weight: bold; letter-spacing: 3px;")
        cat_col.addWidget(cat_lbl)

        categories = sorted(set(a.categorie for a in self.plateforme.articles if a.categorie))
        for cat in categories:
            btn = self._creer_filtre_btn(cat, "categorie")
            cat_col.addWidget(btn)

        cat_col.addStretch()
        cols.addLayout(cat_col)

        # --- SOUS-CATÉGORIE (liste des champs filtrables) ---
        scat_col = QVBoxLayout()
        scat_col.setSpacing(14)
        scat_col.setAlignment(Qt.AlignTop)

        scat_lbl = QLabel("SOUS-CATÉGORIE")
        scat_lbl.setStyleSheet(label_white(16) + " font-weight: bold; letter-spacing: 3px;")
        scat_col.addWidget(scat_lbl)

        sous_cats = sorted(set(
            a.sous_categorie for a in self.plateforme.articles
            if getattr(a, "sous_categorie", None)
        ))
        for sc in sous_cats:
            btn = self._creer_filtre_btn(sc, "sous_categorie")
            scat_col.addWidget(btn)

        scat_col.addStretch()
        cols.addLayout(scat_col)

        # --- Autres attributs ---
        autres_col = QVBoxLayout()
        autres_col.setSpacing(14)
        autres_col.setAlignment(Qt.AlignTop)

        autres_lbl = QLabel("FILTRES DÉTAILLÉS")
        autres_lbl.setStyleSheet(label_white(16) + " font-weight: bold; letter-spacing: 3px;")
        autres_col.addWidget(autres_lbl)

        for label, clé in [("GENRE", "genre"), ("TAILLE", "taille"),
                            ("COULEUR", "couleur"), ("MARQUE", "marque"),
                            ("ÉTAT", "etat"), ("MATIÈRE", "matiere")]:
            lbl = QLabel(label)
            lbl.setStyleSheet(label_white(13) + " letter-spacing: 2px;")
            autres_col.addWidget(lbl)

        autres_col.addStretch()
        cols.addLayout(autres_col)

        cols.addStretch()
        layout.addLayout(cols)

        btn_row = QHBoxLayout()

        btn_appliquer = QPushButton("APPLIQUER")
        btn_appliquer.setStyleSheet(btn_accent_style())
        btn_appliquer.setFixedWidth(200)
        btn_appliquer.clicked.connect(self._appliquer)
        btn_row.addWidget(btn_appliquer)  # ← ajouté au layout !

        btn_reset = QPushButton("RÉINITIALISER")
        btn_reset.setStyleSheet(btn_accent_style())
        btn_reset.setFixedWidth(200)
        btn_reset.clicked.connect(self._reinitialiser)
        btn_row.addWidget(btn_reset)

        layout.addLayout(btn_row)  # ← ajouté au layout !
        layout.addStretch()

    def _creer_filtre_btn(self, texte, champ):
        btn = QPushButton(texte.upper())
        btn.setCheckable(True)
        btn.setStyleSheet(f"""
            QPushButton {{
                color: {WHITE}; background: transparent; border: none;
                font-size: 13px; letter-spacing: 2px; text-align: left; padding: 3px;
            }}
            QPushButton:hover {{ color: {ACCENT_COLOR}; }}
            QPushButton:checked {{
                color: {ACCENT_COLOR}; font-weight: bold;
                border-left: 2px solid {ACCENT_COLOR}; padding-left: 8px;
            }}
        """)
        btn.clicked.connect(lambda checked, c=champ, v=texte: self._toggle(c, v, btn))
        return btn

    def _toggle(self, champ, valeur, btn):
        if champ in self.filtres_actifs and self.filtres_actifs[champ] == valeur:
            del self.filtres_actifs[champ]
            btn.setChecked(False)
        else:
            self.filtres_actifs[champ] = valeur


    def _appliquer(self):
        self.filtres_appliques.emit(self.filtres_actifs)  #seulement quand on clique Appliquer

    def _reinitialiser(self):
        self.filtres_actifs = {}
        self.filtres_appliques.emit({})
