"""----------- Author : LARDILLIER Léo / GREGOIRE Louna -------------"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QFrame, QScrollArea, QPushButton)
from PyQt5.QtCore import Qt, pyqtSignal
from ui.styles import *


class NotificationsPage(QWidget):
    """Page affichant les notifications reçues et les abonnements actifs."""

    article_clique = pyqtSignal(object)

    def __init__(self, plateforme, utilisateur):
        super().__init__()
        self.plateforme = plateforme
        self.utilisateur = utilisateur
        self.setStyleSheet(f"background-color: {BG_COLOR};")
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(40)

        # --- GAUCHE : notifications reçues ---
        left = QVBoxLayout()
        left.setSpacing(15)

        titre_notif = QLabel("NOTIFICATIONS")
        titre_notif.setStyleSheet(label_accent(22) + " letter-spacing: 3px;")
        left.addWidget(titre_notif)

        scroll_notif = QScrollArea()
        scroll_notif.setWidgetResizable(True)
        scroll_notif.setStyleSheet("border: none; background: transparent;")

        self.container_notif = QWidget()
        self.container_notif.setStyleSheet("background: transparent;")
        self.notif_layout = QVBoxLayout(self.container_notif)
        self.notif_layout.setSpacing(12)
        self.notif_layout.setAlignment(Qt.AlignTop)

        scroll_notif.setWidget(self.container_notif)
        left.addWidget(scroll_notif)
        layout.addLayout(left, 3)

        # --- DROITE : abonnements actifs ---
        right = QVBoxLayout()
        right.setSpacing(15)

        titre_abo = QLabel("MES ABONNEMENTS")
        titre_abo.setStyleSheet(label_accent(22) + " letter-spacing: 3px;")
        right.addWidget(titre_abo)

        scroll_abo = QScrollArea()
        scroll_abo.setWidgetResizable(True)
        scroll_abo.setStyleSheet("border: none; background: transparent;")

        self.container_abo = QWidget()
        self.container_abo.setStyleSheet("background: transparent;")
        self.abo_layout = QVBoxLayout(self.container_abo)
        self.abo_layout.setSpacing(12)
        self.abo_layout.setAlignment(Qt.AlignTop)

        scroll_abo.setWidget(self.container_abo)
        right.addWidget(scroll_abo)
        layout.addLayout(right, 2)

    def _charger_notifications(self):
        while self.notif_layout.count():
            w = self.notif_layout.takeAt(0).widget()
            if w:
                w.setParent(None)

        notifs = getattr(self.plateforme, "notifications", [])
        if not notifs:
            vide = QLabel("Aucune notification pour l'instant.")
            vide.setStyleSheet(label_dim(13))
            self.notif_layout.addWidget(vide)
            return

        for article in reversed(notifs):
            self.notif_layout.addWidget(self._carte_notif(article))

    def _carte_notif(self, article):
        frame = QFrame()
        frame.setCursor(Qt.PointingHandCursor)
        frame.setStyleSheet(
            f"background-color: {MUTED_COLOR}; border-radius: 6px; border-left: 3px solid {ACCENT_COLOR};"
        )
        frame.mousePressEvent = lambda event: self.article_clique.emit(article)

        row = QHBoxLayout(frame)
        row.setContentsMargins(15, 12, 15, 12)

        icone = QLabel("🔔")
        icone.setFixedSize(50, 50)
        icone.setAlignment(Qt.AlignCenter)
        icone.setStyleSheet("background-color: #0a0a30; font-size: 22px; border-radius: 4px;")
        row.addWidget(icone)

        lbl = QLabel(f"'{article.nom}' correspond à vos critères !".upper())
        lbl.setStyleSheet(label_white(11) + " letter-spacing: 1px;")
        lbl.setWordWrap(True)
        row.addWidget(lbl)

        return frame

    def _charger_abonnements(self):
        while self.abo_layout.count():
            w = self.abo_layout.takeAt(0).widget()
            if w:
                w.setParent(None)

        mes_obs = [o for o in self.plateforme._observateurs
                   if o.acheteur.id == self.utilisateur.id]

        if not mes_obs:
            vide = QLabel("Aucun abonnement actif.\nUtilise les filtres pour t'abonner.")
            vide.setStyleSheet(label_dim(13))
            vide.setWordWrap(True)
            self.abo_layout.addWidget(vide)
            return

        for obs in mes_obs:
            self.abo_layout.addWidget(self._carte_abonnement(obs))

    def _carte_abonnement(self, observateur):
        frame = QFrame()
        frame.setStyleSheet(
            f"background-color: {MUTED_COLOR}; border-radius: 6px; border-left: 3px solid {PINK_COLOR};"
        )

        col = QVBoxLayout(frame)
        col.setContentsMargins(15, 12, 15, 12)
        col.setSpacing(6)

        criteres_txt = "  |  ".join(
            f"{k.upper()}: {v}" for k, v in observateur.criteres.items()
        )
        lbl = QLabel(criteres_txt)
        lbl.setStyleSheet(label_white(11) + " letter-spacing: 1px;")
        lbl.setWordWrap(True)
        col.addWidget(lbl)

        btn_deso = QPushButton("SE DÉSABONNER")
        btn_deso.setStyleSheet(f"""
            QPushButton {{
                color: {PINK_COLOR}; background: transparent;
                border: 1px solid {PINK_COLOR}; border-radius: 8px;
                padding: 3px 10px; font-size: 9px; font-weight: bold; letter-spacing: 1px;
            }}
            QPushButton:hover {{ background-color: {PINK_COLOR}; color: {BG_COLOR}; }}
        """)
        btn_deso.setFixedWidth(140)
        btn_deso.clicked.connect(lambda: self._desabonner(observateur))
        col.addWidget(btn_deso, alignment=Qt.AlignLeft)

        return frame

    def _desabonner(self, observateur):
        self.plateforme.desabonner(observateur)
        self._charger_abonnements()

    def showEvent(self, event):
        super().showEvent(event)
        self._charger_notifications()
        self._charger_abonnements()
