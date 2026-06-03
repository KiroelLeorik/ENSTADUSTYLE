"""----------- Author : LARDILLIER Léo / GREGOIRE Louna -------------"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QFrame, QGridLayout, QScrollArea)
from PyQt5.QtCore import Qt, pyqtSignal
from ui.styles import *

ARTICLES_PAR_PAGE = 6


class VendeurProfilPage(QWidget):
    """Page profil d'un vendeur, accessible depuis la fiche article."""

    retour = pyqtSignal()

    def __init__(self, plateforme):
        super().__init__()
        self.plateforme = plateforme
        self.vendeur_user = None
        self.articles_vendeur = []
        self.page_courante = 0
        self.setStyleSheet(f"background-color: {BG_COLOR};")
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(40)

        # --- GAUCHE infos vendeur ---
        self.left = QVBoxLayout()
        self.left.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.left.setSpacing(12)

        self.avatar = QLabel("👤")
        self.avatar.setFixedSize(160, 160)
        self.avatar.setAlignment(Qt.AlignCenter)
        self.avatar.setStyleSheet(
            f"background-color: {PINK_COLOR}; border-radius: 80px; font-size: 70px;"
        )
        self.left.addWidget(self.avatar, alignment=Qt.AlignCenter)

        self.label_pseudo = QLabel()
        self.label_pseudo.setStyleSheet(label_accent(16))
        self.label_pseudo.setAlignment(Qt.AlignCenter)
        self.left.addWidget(self.label_pseudo)

        stats = QHBoxLayout()
        stats.setAlignment(Qt.AlignCenter)
        stats.setSpacing(20)
        for val, lbl in [("243", "ABONNÉS"), ("243", "ABONNEMENTS")]:
            col = QVBoxLayout()
            col.setAlignment(Qt.AlignCenter)
            v = QLabel(val)
            v.setStyleSheet(label_white(16) + " font-weight: bold;")
            v.setAlignment(Qt.AlignCenter)
            l = QLabel(lbl)
            l.setStyleSheet(label_dim(9) + " letter-spacing: 2px;")
            l.setAlignment(Qt.AlignCenter)
            col.addWidget(v)
            col.addWidget(l)
            stats.addLayout(col)
        self.left.addLayout(stats)

        self.label_eval = QLabel()
        self.label_eval.setStyleSheet(f"color: {GOLD_COLOR}; font-size: 20px;")
        self.label_eval.setAlignment(Qt.AlignCenter)
        self.left.addWidget(self.label_eval)

        self.label_nb_eval = QLabel()
        self.label_nb_eval.setStyleSheet(label_white(10) + " letter-spacing: 2px;")
        self.label_nb_eval.setAlignment(Qt.AlignCenter)
        self.left.addWidget(self.label_nb_eval)

        self.label_desc = QLabel("DESCRIPTION: ")
        self.label_desc.setStyleSheet(label_white(11) + " letter-spacing: 1px;")
        self.label_desc.setWordWrap(True)
        self.left.addWidget(self.label_desc)

        self.left.addStretch()
        layout.addLayout(self.left, 1)

        # --- DROITE grille articles ---
        right = QVBoxLayout()
        right.setAlignment(Qt.AlignTop)

        # Navigation
        nav = QHBoxLayout()
        self.btn_prev = QPushButton("<")
        self.btn_prev.setStyleSheet(nav_btn_style())
        self.btn_prev.setFixedWidth(40)
        self.btn_prev.clicked.connect(self._precedent)

        self.grille_container = QWidget()
        self.grille_container.setStyleSheet("background: transparent;")
        self.grille = QGridLayout(self.grille_container)
        self.grille.setSpacing(10)
        self.grille.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.btn_next = QPushButton(">")
        self.btn_next.setStyleSheet(nav_btn_style())
        self.btn_next.setFixedWidth(40)
        self.btn_next.clicked.connect(self._suivant)

        nav.addWidget(self.btn_prev)
        nav.addWidget(self.grille_container)
        nav.addWidget(self.btn_next)
        right.addLayout(nav)
        right.addStretch()
        layout.addLayout(right, 2)

    def set_vendeur(self, utilisateur):
        """Charge et affiche les données du vendeur."""
        self.vendeur_user = utilisateur
        self.label_pseudo.setText(f"@{utilisateur.pseudo.upper()}")

        nb_etoiles = int(utilisateur.evaluation)
        self.label_eval.setText("⭐" * nb_etoiles + "☆" * (5 - nb_etoiles))
        self.label_nb_eval.setText(f"{utilisateur.evaluation} ÉVALUATIONS")

        vendeur = self.plateforme.en_tant_que_vendeur(utilisateur)
        vendus, en_vente = vendeur.mes_articles()
        self.articles_vendeur = en_vente + vendus
        self.page_courante = 0
        self._afficher_articles()

    def _afficher_articles(self):
        for i in reversed(range(self.grille.count())):
            w = self.grille.itemAt(i).widget()
            if w:
                w.setParent(None)

        start = self.page_courante * ARTICLES_PAR_PAGE
        end = min(start + ARTICLES_PAR_PAGE, len(self.articles_vendeur))

        for i, article in enumerate(self.articles_vendeur[start:end]):
            frame = QFrame()
            frame.setFixedSize(185, 145)
            frame.setStyleSheet(f"background-color: {MUTED_COLOR}; border-radius: 4px;")
            fl = QVBoxLayout(frame)
            lbl = QLabel(article.nom.upper()[:22])
            lbl.setStyleSheet(label_accent(9) + " letter-spacing: 1px;")
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setWordWrap(True)
            fl.addStretch()
            fl.addWidget(lbl)
            self.grille.addWidget(frame, i // 3, i % 3)

        self.btn_prev.setEnabled(self.page_courante > 0)
        self.btn_next.setEnabled(end < len(self.articles_vendeur))

    def _precedent(self):
        if self.page_courante > 0:
            self.page_courante -= 1
            self._afficher_articles()

    def _suivant(self):
        if (self.page_courante + 1) * ARTICLES_PAR_PAGE < len(self.articles_vendeur):
            self.page_courante += 1
            self._afficher_articles()
