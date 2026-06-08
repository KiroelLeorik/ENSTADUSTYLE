"""----------- Author : LARDILLIER Léo / GREGOIRE Louna -------------"""

import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from ui.styles import *

ARTICLES_PAR_PAGE = 4
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


class CarteArticle(QFrame):
    """Carte cliquable représentant un article dans le catalogue."""

    clique = pyqtSignal(object)

    def __init__(self, article):
        super().__init__()
        self.article = article
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(185, 240)
        self.setStyleSheet(f"background-color: {CARD_COLOR}; border-radius: 4px;")
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 10)
        layout.setSpacing(6)

        photo = QLabel()
        photo.setFixedSize(185, 170)
        photo.setAlignment(Qt.AlignCenter)
        pix = _pix_absolu(getattr(self.article, 'photo', None), 185, 170)
        if pix:
            photo.setPixmap(pix)
        else:
            photo.setText("📷")
            photo.setStyleSheet(photo_placeholder_style())
        layout.addWidget(photo)

        # Nom article
        nom = QLabel(self.article.nom.upper())
        nom.setStyleSheet(label_accent(10))
        nom.setAlignment(Qt.AlignCenter)
        nom.setWordWrap(True)
        nom.setMaximumHeight(36)
        layout.addWidget(nom)

        # Prix
        prix = QLabel(f"{self.article.prix_vendeur}€")
        prix.setStyleSheet(label_white(11))
        prix.setAlignment(Qt.AlignCenter)
        layout.addWidget(prix)

    def mousePressEvent(self, event):
        self.clique.emit(self.article)


class CataloguePage(QWidget):
    """Page catalogue affichant les articles par pages de 4."""

    article_clique = pyqtSignal(object)

    def __init__(self, plateforme):
        super().__init__()
        self.plateforme = plateforme
        self.page_courante = 0
        self.articles = []
        self.setStyleSheet(f"background-color: {BG_COLOR};")
        self._init_ui()
        self.filtres_actifs = False  # ← nouveau flag

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()

        # Navigation avec flèches
        nav = QHBoxLayout()
        nav.setContentsMargins(10, 0, 10, 0)

        self.btn_prev = QPushButton("<")
        self.btn_prev.setStyleSheet(nav_btn_style())
        self.btn_prev.setFixedWidth(50)
        self.btn_prev.clicked.connect(self._precedent)
        nav.addWidget(self.btn_prev)

        # Zone cartes
        self.zone_cartes = QHBoxLayout()
        self.zone_cartes.setSpacing(25)
        self.zone_cartes.setAlignment(Qt.AlignCenter)
        nav.addLayout(self.zone_cartes)

        self.btn_next = QPushButton(">")
        self.btn_next.setStyleSheet(nav_btn_style())
        self.btn_next.setFixedWidth(50)
        self.btn_next.clicked.connect(self._suivant)
        nav.addWidget(self.btn_next)

        layout.addLayout(nav)
        layout.addStretch()

    def _charger_articles(self):
        from services.recommendation import recommander
        if not self.plateforme.utilisateur_courant:
            self.articles = [a for a in self.plateforme.articles if not a.vendu]
        else:
            acheteur = self.plateforme.en_tant_que_acheteur(self.plateforme.utilisateur_courant)
            if acheteur.favoris:
                resultat = recommander(acheteur, self.plateforme.articles, 50)
                self.articles = [a[0] for a in resultat]
            else:
                self.articles = [a for a in self.plateforme.articles if not a.vendu]
        self.page_courante = 0
        self._afficher_page()

    def appliquer_filtres(self, articles):
        """Appelé depuis main_window avec les articles filtrés."""
        self.filtres_actifs = True  # ← on signale qu'on est en mode filtre
        self.articles = articles
        self.page_courante = 0
        self._afficher_page()

    def _afficher_page(self):
        # Vider
        for i in reversed(range(self.zone_cartes.count())):
            w = self.zone_cartes.itemAt(i).widget()
            if w:
                w.setParent(None)

        start = self.page_courante * ARTICLES_PAR_PAGE
        end = min(start + ARTICLES_PAR_PAGE, len(self.articles))

        for article in self.articles[start:end]:
            carte = CarteArticle(article)
            carte.clique.connect(self.article_clique.emit)
            self.zone_cartes.addWidget(carte)

        self.btn_prev.setEnabled(self.page_courante > 0)
        self.btn_next.setEnabled(end < len(self.articles))

    def _precedent(self):
        if self.page_courante > 0:
            self.page_courante -= 1
            self._afficher_page()

    def _suivant(self):
        if (self.page_courante + 1) * ARTICLES_PAR_PAGE < len(self.articles):
            self.page_courante += 1
            self._afficher_page()

    def showEvent(self, event):
        super().showEvent(event)
        if not self.filtres_actifs:
            self._charger_articles()  # ← seulement si pas de filtres actifs
        self.filtres_actifs = False  # ← reset après affichage
