"""----------- Author : LARDILLIER Léo -------------"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                              QLineEdit, QPushButton, QCheckBox)
from PyQt5.QtCore import Qt


STYLE_BG = "background-color: #0d0d1a;"
STYLE_TITRE = "color: #00bfff; font-size: 32px; font-weight: bold;"
STYLE_INPUT = """
    background-color: #1a1a2e;
    color: white;
    border: 1px solid #00bfff;
    border-radius: 8px;
    padding: 10px;
    font-size: 14px;
"""
STYLE_BTN_MAIN = """
    background-color: #00bfff;
    color: #0d0d1a;
    border-radius: 8px;
    padding: 12px;
    font-size: 14px;
    font-weight: bold;
"""
STYLE_BTN_LINK = """
    QPushButton {
        background: transparent;
        color: #4466ff;
        border: none;
        font-size: 12px;
        text-decoration: underline;
    }
    QPushButton:hover { color: #6688ff; }
"""
STYLE_ERREUR = "color: red; font-size: 12px;"


class LoginWindow(QWidget):
    def __init__(self, plateforme):
        super().__init__()
        self.plateforme = plateforme
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle("ENST'AS DU STYLE")
        self.setFixedSize(400, 500)
        self.setStyleSheet(STYLE_BG)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        titre = QLabel("ENST'AS\nDU STYLE")
        titre.setAlignment(Qt.AlignCenter)
        titre.setStyleSheet(STYLE_TITRE)
        layout.addWidget(titre)

        self.input_pseudo = QLineEdit()
        self.input_pseudo.setPlaceholderText("Pseudo")
        self.input_pseudo.setStyleSheet(STYLE_INPUT)
        layout.addWidget(self.input_pseudo)

        self.input_mdp = QLineEdit()
        self.input_mdp.setPlaceholderText("Mot de passe")
        self.input_mdp.setEchoMode(QLineEdit.Password)
        self.input_mdp.setStyleSheet(STYLE_INPUT)
        layout.addWidget(self.input_mdp)

        btn_login = QPushButton("SE CONNECTER")
        btn_login.setStyleSheet(STYLE_BTN_MAIN)
        btn_login.clicked.connect(self._se_connecter)
        layout.addWidget(btn_login)

        self.label_erreur = QLabel("")
        self.label_erreur.setAlignment(Qt.AlignCenter)
        self.label_erreur.setStyleSheet(STYLE_ERREUR)
        layout.addWidget(self.label_erreur)

        btn_inscription = QPushButton("Pas encore de compte ? Créer un compte")
        btn_inscription.setStyleSheet(STYLE_BTN_LINK)
        btn_inscription.clicked.connect(self._ouvrir_inscription)
        layout.addWidget(btn_inscription)

        self.setLayout(layout)

    def _se_connecter(self):
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

    def _ouvrir_inscription(self):
        self.register = RegisterWindow(self.plateforme, self)
        self.register.show()


class RegisterWindow(QWidget):
    def __init__(self, plateforme, login_window):
        super().__init__()
        self.plateforme = plateforme
        self.login_window = login_window
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle("ENST'AS DU STYLE — Inscription")
        self.setFixedSize(400, 620)
        self.setStyleSheet(STYLE_BG)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(14)

        titre = QLabel("CRÉER UN COMPTE")
        titre.setAlignment(Qt.AlignCenter)
        titre.setStyleSheet("color: #00bfff; font-size: 22px; font-weight: bold;")
        layout.addWidget(titre)

        self.input_pseudo = QLineEdit()
        self.input_pseudo.setPlaceholderText("Pseudo *")
        self.input_pseudo.setStyleSheet(STYLE_INPUT)
        layout.addWidget(self.input_pseudo)

        self.input_nom = QLineEdit()
        self.input_nom.setPlaceholderText("Nom *")
        self.input_nom.setStyleSheet(STYLE_INPUT)
        layout.addWidget(self.input_nom)

        self.input_prenom = QLineEdit()
        self.input_prenom.setPlaceholderText("Prénom *")
        self.input_prenom.setStyleSheet(STYLE_INPUT)
        layout.addWidget(self.input_prenom)

        self.input_mail = QLineEdit()
        self.input_mail.setPlaceholderText("Adresse e-mail *")
        self.input_mail.setStyleSheet(STYLE_INPUT)
        layout.addWidget(self.input_mail)

        self.input_mdp = QLineEdit()
        self.input_mdp.setPlaceholderText("Mot de passe * (6 car. min.)")
        self.input_mdp.setEchoMode(QLineEdit.Password)
        self.input_mdp.setStyleSheet(STYLE_INPUT)
        layout.addWidget(self.input_mdp)

        self.input_localisation = QLineEdit()
        self.input_localisation.setPlaceholderText("Localisation (optionnel)")
        self.input_localisation.setStyleSheet(STYLE_INPUT)
        layout.addWidget(self.input_localisation)

        self.check_pro = QCheckBox("Compte vendeur professionnel")
        self.check_pro.setStyleSheet("color: white; font-size: 13px;")
        layout.addWidget(self.check_pro)

        btn_creer = QPushButton("CRÉER LE COMPTE")
        btn_creer.setStyleSheet(STYLE_BTN_MAIN)
        btn_creer.clicked.connect(self._creer_compte)
        layout.addWidget(btn_creer)

        self.label_erreur = QLabel("")
        self.label_erreur.setAlignment(Qt.AlignCenter)
        self.label_erreur.setStyleSheet(STYLE_ERREUR)
        layout.addWidget(self.label_erreur)

        btn_retour = QPushButton("← Retour à la connexion")
        btn_retour.setStyleSheet(STYLE_BTN_LINK)
        btn_retour.clicked.connect(self.close)
        layout.addWidget(btn_retour)

        self.setLayout(layout)

    def _creer_compte(self):
        pseudo = self.input_pseudo.text().strip()
        nom = self.input_nom.text().strip()
        prenom = self.input_prenom.text().strip()
        mail = self.input_mail.text().strip()
        mdp = self.input_mdp.text()
        localisation = self.input_localisation.text().strip() or None
        est_pro = self.check_pro.isChecked()

        if not all([pseudo, nom, prenom, mail, mdp]):
            self.label_erreur.setText("Veuillez remplir tous les champs obligatoires (*).")
            return
        if len(mdp) < 6:
            self.label_erreur.setText("Le mot de passe doit contenir au moins 6 caractères.")
            return

        ok = self.plateforme.creer_utilisateur(pseudo, nom, prenom, mail, mdp, est_pro, 0, localisation)
        if not ok:
            self.label_erreur.setText("Ce pseudo est déjà utilisé.")
            return

        user = self.plateforme.authentifier_utilisateur(pseudo, mdp)
        from ui.main_window import MainWindow
        self.main = MainWindow(self.plateforme, user)
        self.main.show()
        self.login_window.close()
        self.close()
