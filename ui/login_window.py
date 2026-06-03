from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                              QLineEdit, QPushButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class LoginWindow(QWidget):
    def __init__(self, plateforme):
        super().__init__()
        self.plateforme = plateforme
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("ENST'AS DU STYLE")
        self.setFixedSize(400, 500)
        self.setStyleSheet("background-color: #0d0d1a;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        # Titre
        titre = QLabel("ENST'AS\nDU STYLE")
        titre.setAlignment(Qt.AlignCenter)
        titre.setStyleSheet("color: #00bfff; font-size: 32px; font-weight: bold;")
        layout.addWidget(titre)

        # Champ pseudo
        self.input_pseudo = QLineEdit()
        self.input_pseudo.setPlaceholderText("Pseudo")
        self.input_pseudo.setStyleSheet("""
            background-color: #1a1a2e;
            color: white;
            border: 1px solid #00bfff;
            border-radius: 8px;
            padding: 10px;
            font-size: 14px;
        """)
        layout.addWidget(self.input_pseudo)

        # Champ mot de passe
        self.input_mdp = QLineEdit()
        self.input_mdp.setPlaceholderText("Mot de passe")
        self.input_mdp.setEchoMode(QLineEdit.Password)
        self.input_mdp.setStyleSheet(self.input_pseudo.styleSheet())
        layout.addWidget(self.input_mdp)

        # Bouton connexion
        btn_login = QPushButton("SE CONNECTER")
        btn_login.setStyleSheet("""
            background-color: #00bfff;
            color: #0d0d1a;
            border-radius: 8px;
            padding: 12px;
            font-size: 14px;
            font-weight: bold;
        """)
        btn_login.clicked.connect(self.se_connecter)
        layout.addWidget(btn_login)

        # Message d'erreur
        self.label_erreur = QLabel("")
        self.label_erreur.setAlignment(Qt.AlignCenter)
        self.label_erreur.setStyleSheet("color: red; font-size: 12px;")
        layout.addWidget(self.label_erreur)

        self.setLayout(layout)

    def se_connecter(self):
        pseudo = self.input_pseudo.text()
        mdp = self.input_mdp.text()
        user = self.plateforme.authentifier_utilisateur(pseudo, mdp)
        if user:
            from ui.main_window import MainWindow
            self.main = MainWindow(self.plateforme, user)
            self.main.show()
            self.close()
        else:
            self.label_erreur.setText("Pseudo ou mot de passe incorrect.")

