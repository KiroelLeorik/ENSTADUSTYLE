"""----------- Author : LARDILLIER Léo / GREGOIRE Louna -------------"""

import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QFrame, QGridLayout, QScrollArea)
from PyQt5.QtCore import Qt, pyqtSignal
from ui.styles import *

ARTICLES_PAR_PAGE = 6
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _pix_absolu(chemin, largeur, hauteur):
    from PyQt5.QtGui import QPixmap
    from PyQt5.QtCore import Qt
    if not chemin:
        return None
    absolu = chemin if os.path.isabs(chemin) else os.path.join(BASE_DIR, chemin)
    if not os.path.exists(absolu):
        return None
    pix = QPixmap(absolu)
    if pix.isNull():
        return None
    return pix.scaled(largeur, hauteur, Qt.KeepAspectRatio, Qt.SmoothTransformation)


class VendeurProfilPage(QWidget):
    """Page profil d'un vendeur, accessible depuis la fiche article."""

    retour = pyqtSignal()

    def __init__(self, plateforme, utilisateur):
        super().__init__()
        self.plateforme = plateforme
        self.utilisateur = utilisateur
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

        self.avatar = QLabel()
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

        self.stats_layout = QHBoxLayout()
        self.stats_layout.setAlignment(Qt.AlignCenter)
        self.stats_layout.setSpacing(20)
        self.left.addLayout(self.stats_layout)

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

        self.btn_suivre = QPushButton("SUIVRE")
        self.btn_suivre.setFixedWidth(140)
        self.btn_suivre.setStyleSheet(btn_accent_style())
        self.btn_suivre.clicked.connect(self._toggle_abonnement)
        self.btn_suivre.hide()
        self.left.addWidget(self.btn_suivre, alignment=Qt.AlignCenter)

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

    def _maj_stats(self, id_utilisateur):
        while self.stats_layout.count():
            item = self.stats_layout.takeAt(0)
            if item.layout():
                while item.layout().count():
                    w = item.layout().takeAt(0).widget()
                    if w:
                        w.setParent(None)
        from db.db import get_nb_abonnes, get_nb_abonnements
        for val, lbl in [(get_nb_abonnes(id_utilisateur), "ABONNÉS"),
                         (get_nb_abonnements(id_utilisateur), "ABONNEMENTS")]:
            col = QVBoxLayout()
            col.setAlignment(Qt.AlignCenter)
            v = QLabel(str(val))
            v.setStyleSheet(label_white(16) + " font-weight: bold;")
            v.setAlignment(Qt.AlignCenter)
            l = QLabel(lbl)
            l.setStyleSheet(label_dim(9) + " letter-spacing: 2px;")
            l.setAlignment(Qt.AlignCenter)
            col.addWidget(v)
            col.addWidget(l)
            self.stats_layout.addLayout(col)

    def set_vendeur(self, utilisateur):
        """Charge et affiche les données du vendeur."""
        self.vendeur_user = utilisateur
        pix = _pix_absolu(getattr(utilisateur, 'photo', None), 160, 160)
        if pix:
            self.avatar.setPixmap(pix)
            self.avatar.setText("")
            self.avatar.setStyleSheet("border-radius: 80px;")
        else:
            self.avatar.clear()
            self.avatar.setText("👤")
            self.avatar.setStyleSheet(
                f"background-color: {PINK_COLOR}; border-radius: 80px; font-size: 70px;"
            )
        self.label_pseudo.setText(f"@{utilisateur.pseudo.upper()}")
        self._maj_stats(utilisateur.id)

        nb_etoiles = int(utilisateur.evaluation)
        self.label_eval.setText("⭐" * nb_etoiles + "☆" * (5 - nb_etoiles))
        self.label_nb_eval.setText(f"{utilisateur.evaluation} ÉVALUATIONS")

        # Bouton Suivre — masqué si c'est son propre profil
        if self.utilisateur and self.utilisateur.id != utilisateur.id:
            self._maj_btn_suivre()
            self.btn_suivre.show()
        else:
            self.btn_suivre.hide()

        vendeur = self.plateforme.en_tant_que_vendeur(utilisateur)
        vendus, en_vente = vendeur.mes_articles()
        self.articles_vendeur = en_vente + vendus
        self.page_courante = 0
        self._afficher_articles()

    def _maj_btn_suivre(self):
        from db.db import is_abonne
        if is_abonne(self.utilisateur.id, self.vendeur_user.id):
            self.btn_suivre.setText("NE PLUS SUIVRE")
        else:
            self.btn_suivre.setText("SUIVRE")

    def _toggle_abonnement(self):
        from db.db import is_abonne, insert_abonnement, delete_abonnement
        if is_abonne(self.utilisateur.id, self.vendeur_user.id):
            delete_abonnement(self.utilisateur.id, self.vendeur_user.id)
        else:
            insert_abonnement(self.utilisateur.id, self.vendeur_user.id)
        self._maj_btn_suivre()
        self._maj_stats(self.vendeur_user.id)

    def _afficher_articles(self):
        for i in reversed(range(self.grille.count())):
            w = self.grille.itemAt(i).widget()
            if w:
                w.setParent(None)

        start = self.page_courante * ARTICLES_PAR_PAGE
        end = min(start + ARTICLES_PAR_PAGE, len(self.articles_vendeur))

        for i, article in enumerate(self.articles_vendeur[start:end]):
            frame = QFrame()
            frame.setFixedSize(185, 210)
            frame.setStyleSheet(f"background-color: {MUTED_COLOR}; border-radius: 4px;")
            fl = QVBoxLayout(frame)
            fl.setContentsMargins(0, 0, 0, 8)
            fl.setSpacing(4)

            photo_lbl = QLabel()
            photo_lbl.setFixedSize(185, 150)
            photo_lbl.setAlignment(Qt.AlignCenter)
            pix = _pix_absolu(getattr(article, 'photo', None), 185, 150)
            if pix:
                photo_lbl.setPixmap(pix)
            else:
                photo_lbl.setText("📷")
                photo_lbl.setStyleSheet(photo_placeholder_style() + " font-size: 30px;")
            fl.addWidget(photo_lbl)

            lbl = QLabel(article.nom.upper()[:22])
            lbl.setStyleSheet(label_accent(9) + " letter-spacing: 1px;")
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setWordWrap(True)
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
