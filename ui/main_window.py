"""----------- Author : LARDILLIER Léo / GREGOIRE Louna -------------"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QStackedWidget,
                              QVBoxLayout, QHBoxLayout, QPushButton, QLabel)
from PyQt5.QtCore import Qt
from ui.styles import *


class Sidebar(QWidget):
    """Menu latéral superposé, s'affiche sur le contenu."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(210)
        self.setStyleSheet(f"background-color: {SIDEBAR_COLOR};")
        self.btns = {}
        self._init_ui()
        self.hide()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 30, 20, 30)
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignTop)

        for item in ["profil", "messagerie", "filtres", "fil d'actu", "favoris", "panier", "vendre"]:
            btn = QPushButton(item)
            btn.setStyleSheet(sidebar_btn_style())
            self.btns[item] = btn
            layout.addWidget(btn)

        layout.addStretch()


class TopBar(QWidget):
    """Barre supérieure avec hamburger menu et cloche de notification."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(55)
        self.setStyleSheet(f"background-color: {SIDEBAR_COLOR};")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 8, 15, 8)

        self.btn_menu = QPushButton("≡")
        self.btn_menu.setStyleSheet(icon_btn_style())
        self.btn_menu.setFixedSize(40, 38)
        layout.addWidget(self.btn_menu)

        layout.addStretch()

        self.btn_notif = QPushButton("🔔")
        self.btn_notif.setStyleSheet(icon_btn_style())
        self.btn_notif.setFixedSize(40, 38)
        layout.addWidget(self.btn_notif)


class MainWindow(QMainWindow):
    """Fenêtre principale de l'application ENST'AS DU STYLE."""

    def __init__(self, plateforme, utilisateur):
        super().__init__()
        self.plateforme = plateforme
        self.utilisateur = utilisateur
        self.setWindowTitle("ENST'AS DU STYLE")
        self.setMinimumSize(950, 620)
        self.setStyleSheet(f"background-color: {BG_COLOR};")
        self._init_ui()
        self._connecter_sidebar()

    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        main = QVBoxLayout(central)
        main.setContentsMargins(0, 0, 0, 0)
        main.setSpacing(0)

        # TopBar
        self.topbar = TopBar()
        self.topbar.btn_menu.clicked.connect(self._toggle_sidebar)
        self.topbar.btn_notif.clicked.connect(lambda: self._nav("notifications"))
        main.addWidget(self.topbar)

        # Contenu principal (QStackedWidget)
        self.stack = QStackedWidget()
        self.stack.setStyleSheet(f"background-color: {BG_COLOR};")
        main.addWidget(self.stack)

        # Charger les pages
        self._charger_pages()

        # Sidebar (overlay par-dessus tout)
        self.sidebar = Sidebar(self)
        self.sidebar.raise_()

    def _charger_pages(self):
        # Juste la page d'accueil au démarrage
        from ui.pages.accueil import AccueilPage
        self.pages = {}
        self.pages["accueil"] = AccueilPage(self.plateforme)
        self.stack.addWidget(self.pages["accueil"])
        self._nav("accueil")

    def _get_page(self, nom):
        """Charge une page seulement si elle n'existe pas encore."""
        if nom not in self.pages:
            self._creer_page(nom)
        return self.pages[nom]

    def _creer_page(self, nom):
        from ui.pages.catalogue import CataloguePage
        from ui.pages.profil import ProfilPage
        from ui.pages.favoris import FavorisPage
        from ui.pages.filtres import FiltresPage
        from ui.pages.vendre import VendrePage
        from ui.pages.notifications import NotificationsPage
        from ui.pages.article_detail import ArticleDetailPage
        from ui.pages.vendeur_profil import VendeurProfilPage

        pages_map = {
            "catalogue": lambda: CataloguePage(self.plateforme),
            "profil": lambda: ProfilPage(self.plateforme, self.utilisateur),
            "favoris": lambda: FavorisPage(self.plateforme, self.utilisateur),
            "filtres": lambda: FiltresPage(self.plateforme),
            "vendre": lambda: VendrePage(self.plateforme, self.utilisateur),
            "notifications": lambda: NotificationsPage(self.plateforme),
            "article_detail": lambda: ArticleDetailPage(self.plateforme, self.utilisateur),
            "vendeur_profil": lambda: VendeurProfilPage(self.plateforme),
        }

        if nom in pages_map:
            page = pages_map[nom]()
            self.pages[nom] = page
            self.stack.addWidget(page)
            self._connecter_signaux(nom)

    def _connecter_signaux(self, nom):
        if nom == "catalogue":
            self.pages["catalogue"].article_clique.connect(self._ouvrir_article)
        elif nom == "favoris":
            self.pages["favoris"].article_clique.connect(self._ouvrir_article)
        elif nom == "article_detail":
            self.pages["article_detail"].vendeur_clique.connect(self._ouvrir_vendeur)
            self.pages["article_detail"].retour.connect(lambda: self._nav("catalogue"))
        elif nom == "filtres":
            self.pages["filtres"].filtres_appliques.connect(self._appliquer_filtres)
        elif nom == "notifications":
            self.pages["notifications"].article_clique.connect(self._ouvrir_article)
        elif nom == "vendeur_profil":
            self.pages["vendeur_profil"].retour.connect(lambda: self._nav("article_detail"))

    def _connecter_sidebar(self):
        mapping = {
            "profil": "profil",
            "fil d'actu": "catalogue",
            "favoris": "favoris",
            "filtres": "filtres",
            "vendre": "vendre",
        }
        for label, page in mapping.items():
            if label in self.sidebar.btns:
                self.sidebar.btns[label].clicked.connect(
                    lambda checked, p=page: self._nav_et_fermer(p)
                )

    def _nav(self, page_name):
        page = self._get_page(page_name)
        self.stack.setCurrentWidget(page)

    def _nav_et_fermer(self, page_name):
        self._nav(page_name)
        self.sidebar.hide()

    def _toggle_sidebar(self):
        if self.sidebar.isVisible():
            self.sidebar.hide()
        else:
            h = self.height() - self.topbar.height()
            self.sidebar.setGeometry(0, self.topbar.height(), 210, h)
            self.sidebar.show()
            self.sidebar.raise_()

    def _ouvrir_article(self, article):
        page = self._get_page("article_detail")
        page.set_article(article)
        self._nav("article_detail")

    def _ouvrir_vendeur(self, utilisateur):
        self.pages["vendeur_profil"].set_vendeur(utilisateur)
        self._nav("vendeur_profil")

    def _appliquer_filtres(self, filtres):
        """Applique les filtres sur le catalogue et navigue vers lui."""
        from services.recherche import scorer_articles
        resultats = scorer_articles(self.plateforme.articles, filtres)
        catalogue = self._get_page("catalogue")
        if resultats and isinstance(resultats[0], tuple):
            catalogue.articles = [a for a, _ in resultats]
        else:
            catalogue.articles = list(resultats)
        catalogue.page_courante = 0
        catalogue.appliquer_filtres(catalogue.articles)
        self._nav("catalogue")

    def mousePressEvent(self, event):
        if self.sidebar.isVisible():
            if not self.sidebar.geometry().contains(event.pos()):
                self.sidebar.hide()
        super().mousePressEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.sidebar.isVisible():
            h = self.height() - self.topbar.height()
            self.sidebar.setGeometry(0, self.topbar.height(), 210, h)
