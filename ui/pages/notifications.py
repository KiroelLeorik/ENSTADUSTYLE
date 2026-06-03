"""----------- Author : LARDILLIER Léo / GREGOIRE Louna -------------"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QFrame, QScrollArea)
from PyQt5.QtCore import Qt, pyqtSignal
from ui.styles import *


class NotificationsPage(QWidget):
    """Page affichant les notifications de l'utilisateur (Observer pattern)."""

    article_clique = pyqtSignal(object)

    def __init__(self, plateforme):
        super().__init__()
        self.plateforme = plateforme
        self.setStyleSheet(f"background-color: {BG_COLOR};")
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(15)

        titre = QLabel("NOTIFICATIONS")
        titre.setStyleSheet(label_accent(28) + " letter-spacing: 3px;")
        layout.addWidget(titre)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: transparent;")

        self.container = QWidget()
        self.container.setStyleSheet("background: transparent;")
        self.notif_layout = QVBoxLayout(self.container)
        self.notif_layout.setSpacing(12)
        self.notif_layout.setAlignment(Qt.AlignTop)

        scroll.setWidget(self.container)
        layout.addWidget(scroll)

    def _charger(self):
        while self.notif_layout.count():
            w = self.notif_layout.takeAt(0).widget()
            if w:
                w.setParent(None)
        notifs = getattr(self.plateforme, "notifications", [])
        for article in reversed(notifs):
            self.notif_layout.addWidget(self._creer_carte(article))

    def _creer_carte(self, article):
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
        icone.setStyleSheet(f"background-color: #0a0a30; font-size: 22px; border-radius: 4px;")
        row.addWidget(icone)

        lbl = QLabel(f"'{article.nom}' correspond à vos critères !".upper())
        lbl.setStyleSheet(label_white(11) + " letter-spacing: 1px;")
        lbl.setWordWrap(True)
        row.addWidget(lbl)

        return frame

    def showEvent(self, event):
        super().showEvent(event)
        self._charger()
