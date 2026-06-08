"""----------- Author : LARDILLIER Léo / GREGOIRE Louna -------------"""

import os, shutil
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QFrame, QGridLayout, QScrollArea,
                              QDialog, QLineEdit, QTextEdit, QComboBox,
                              QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt, pyqtSignal
from ui.styles import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PHOTOS_DIR = os.path.join(BASE_DIR, "assets", "photos")


def _pix_absolu(chemin, largeur, hauteur):
    """Charge un pixmap depuis un chemin relatif au projet, retourne None si absent."""
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


class EditArticleDialog(QDialog):
    """Dialogue d'édition d'un article existant."""

    def __init__(self, article, parent=None):
        super().__init__(parent)
        self.article = article
        self.nouvelle_photo = None
        self.setWindowTitle("Modifier l'article")
        self.setFixedSize(460, 640)
        self.setStyleSheet(f"background-color: {BG_COLOR};")
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(10)

        titre = QLabel("MODIFIER L'ARTICLE")
        titre.setStyleSheet(label_accent(16) + " letter-spacing: 3px;")
        layout.addWidget(titre)

        # Aperçu photo
        photo_row = QHBoxLayout()
        photo_row.setSpacing(15)

        self.photo_label = QLabel()
        self.photo_label.setFixedSize(120, 120)
        self.photo_label.setAlignment(Qt.AlignCenter)
        self._maj_photo_preview()
        photo_row.addWidget(self.photo_label)

        btn_photo = QPushButton("Changer la photo")
        btn_photo.setStyleSheet(f"""
            QPushButton {{
                color: {ACCENT_COLOR}; background: transparent;
                border: 1px solid {ACCENT_COLOR}; border-radius: 8px;
                padding: 6px 12px; font-size: 11px; font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {ACCENT_COLOR}; color: {BG_COLOR}; }}
        """)
        btn_photo.clicked.connect(self._choisir_photo)
        photo_row.addWidget(btn_photo, alignment=Qt.AlignVCenter)
        photo_row.addStretch()
        layout.addLayout(photo_row)

        inp = input_dashed_style()

        self.input_nom = QLineEdit(self.article.nom or "")
        self.input_nom.setPlaceholderText("TITRE")
        self.input_nom.setStyleSheet(inp)
        layout.addWidget(self.input_nom)

        self.input_desc = QTextEdit(self.article.description or "")
        self.input_desc.setPlaceholderText("DESCRIPTION")
        self.input_desc.setMaximumHeight(70)
        self.input_desc.setStyleSheet(inp)
        layout.addWidget(self.input_desc)

        prix_row = QHBoxLayout()
        self.input_prix = QLineEdit(str(self.article.prix_vendeur))
        self.input_prix.setPlaceholderText("PRIX (€)")
        self.input_prix.setStyleSheet(inp)
        self.input_prix_min = QLineEdit(str(self.article.prix_min))
        self.input_prix_min.setPlaceholderText("PRIX MIN (€)")
        self.input_prix_min.setStyleSheet(inp)
        prix_row.addWidget(self.input_prix)
        prix_row.addWidget(self.input_prix_min)
        layout.addLayout(prix_row)

        self.combo_etat = QComboBox()
        self.combo_etat.addItems(["neuf", "tres_bon", "bon", "correct", "mauvais"])
        self.combo_etat.setCurrentText(self.article.etat or "bon")
        self.combo_etat.setStyleSheet(inp)
        layout.addWidget(self.combo_etat)

        champs = [
            ("SOUS-CATÉGORIE", "sous_categorie"),
            ("GENRE", "genre"),
            ("TAILLE", "taille"),
            ("COULEUR", "couleur"),
            ("MARQUE", "marque"),
            ("MATIÈRE", "matiere"),
        ]
        self.inputs = {}
        for placeholder, cle in champs:
            field = QLineEdit(getattr(self.article, cle, "") or "")
            field.setPlaceholderText(placeholder)
            field.setStyleSheet(inp)
            self.inputs[cle] = field
            layout.addWidget(field)

        self.label_erreur = QLabel("")
        self.label_erreur.setStyleSheet("color: #ff4444; font-size: 11px;")
        layout.addWidget(self.label_erreur)

        btn_row = QHBoxLayout()
        btn_annuler = QPushButton("ANNULER")
        btn_annuler.setStyleSheet(btn_accent_style())
        btn_annuler.clicked.connect(self.reject)
        btn_sauvegarder = QPushButton("SAUVEGARDER")
        btn_sauvegarder.setStyleSheet(btn_accent_style())
        btn_sauvegarder.clicked.connect(self._sauvegarder)
        btn_row.addWidget(btn_annuler)
        btn_row.addWidget(btn_sauvegarder)
        layout.addLayout(btn_row)

    def _maj_photo_preview(self):
        chemin = self.nouvelle_photo or getattr(self.article, 'photo', None)
        pix = _pix_absolu(chemin, 120, 120)
        if pix:
            self.photo_label.setPixmap(pix)
            self.photo_label.setText("")
            self.photo_label.setStyleSheet("border-radius: 4px;")
        else:
            self.photo_label.setText("📷")
            self.photo_label.setStyleSheet(photo_placeholder_style() + " font-size: 30px;")

    def _choisir_photo(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Choisir une photo", "", "Images (*.png *.jpg *.jpeg *.webp)"
        )
        if not path:
            return
        os.makedirs(PHOTOS_DIR, exist_ok=True)
        filename = os.path.basename(path)
        dest = os.path.join(PHOTOS_DIR, filename)
        shutil.copy2(path, dest)
        self.nouvelle_photo = f"assets/photos/{filename}"
        from PyQt5.QtGui import QPixmap
        from PyQt5.QtCore import Qt
        pix = QPixmap(dest).scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        if not pix.isNull():
            self.photo_label.setPixmap(pix)
            self.photo_label.setText("")
            self.photo_label.setStyleSheet("border-radius: 4px;")

    def _sauvegarder(self):
        nom = self.input_nom.text().strip()
        if not nom:
            self.label_erreur.setText("Le titre est obligatoire.")
            return
        try:
            prix = float(self.input_prix.text())
            prix_min = float(self.input_prix_min.text())
        except ValueError:
            self.label_erreur.setText("Les prix doivent être des nombres.")
            return

        self.article.nom = nom
        self.article.description = self.input_desc.toPlainText()
        self.article.prix_vendeur = prix
        self.article.prix_min = prix_min
        self.article.etat = self.combo_etat.currentText()
        for cle, field in self.inputs.items():
            setattr(self.article, cle, field.text().strip() or None)
        if self.nouvelle_photo:
            self.article.photo = self.nouvelle_photo

        from db.db import update_article
        update_article(self.article.id, self.article.nom, self.article.description,
                       self.article.prix_vendeur, self.article.prix_min, self.article.etat,
                       self.article.sous_categorie, self.article.genre, self.article.taille,
                       self.article.couleur, self.article.marque, self.article.matiere,
                       self.article.photo)
        self.accept()


class EditProfilDialog(QDialog):
    """Dialogue d'édition du profil utilisateur."""

    def __init__(self, utilisateur, parent=None):
        super().__init__(parent)
        self.utilisateur = utilisateur
        self.setWindowTitle("Modifier le profil")
        self.setFixedSize(380, 420)
        self.setStyleSheet(f"background-color: {BG_COLOR};")
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(14)

        titre = QLabel("MODIFIER LE PROFIL")
        titre.setStyleSheet(label_accent(16) + " letter-spacing: 3px;")
        layout.addWidget(titre)

        # Photo de profil
        self.avatar_label = QLabel()
        self.avatar_label.setFixedSize(100, 100)
        self.avatar_label.setAlignment(Qt.AlignCenter)
        self._maj_avatar_dialog()
        layout.addWidget(self.avatar_label, alignment=Qt.AlignCenter)

        btn_photo = QPushButton("Changer la photo")
        btn_photo.setStyleSheet(f"color: {ACCENT_COLOR}; background: transparent; border: none; font-size: 11px;")
        btn_photo.clicked.connect(self._choisir_photo)
        layout.addWidget(btn_photo, alignment=Qt.AlignCenter)

        inp = input_dashed_style()

        self.input_pseudo = QLineEdit(self.utilisateur.pseudo)
        self.input_pseudo.setPlaceholderText("PSEUDO")
        self.input_pseudo.setStyleSheet(inp)
        layout.addWidget(self.input_pseudo)

        self.input_mail = QLineEdit(self.utilisateur.mail)
        self.input_mail.setPlaceholderText("MAIL")
        self.input_mail.setStyleSheet(inp)
        layout.addWidget(self.input_mail)

        self.input_localisation = QLineEdit(self.utilisateur.localisation or "")
        self.input_localisation.setPlaceholderText("LOCALISATION")
        self.input_localisation.setStyleSheet(inp)
        layout.addWidget(self.input_localisation)

        sep = QLabel("— CHANGER LE MOT DE PASSE —")
        sep.setStyleSheet(label_dim(10) + " letter-spacing: 2px;")
        sep.setAlignment(Qt.AlignCenter)
        layout.addWidget(sep)

        self.input_ancien_mdp = QLineEdit()
        self.input_ancien_mdp.setPlaceholderText("ANCIEN MOT DE PASSE")
        self.input_ancien_mdp.setEchoMode(QLineEdit.Password)
        self.input_ancien_mdp.setStyleSheet(inp)
        layout.addWidget(self.input_ancien_mdp)

        self.input_nouveau_mdp = QLineEdit()
        self.input_nouveau_mdp.setPlaceholderText("NOUVEAU MOT DE PASSE (6 car. min.)")
        self.input_nouveau_mdp.setEchoMode(QLineEdit.Password)
        self.input_nouveau_mdp.setStyleSheet(inp)
        layout.addWidget(self.input_nouveau_mdp)

        self.label_erreur = QLabel("")
        self.label_erreur.setStyleSheet("color: #ff4444; font-size: 11px;")
        self.label_erreur.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_erreur)

        btn_row = QHBoxLayout()
        btn_annuler = QPushButton("ANNULER")
        btn_annuler.setStyleSheet(btn_accent_style())
        btn_annuler.clicked.connect(self.reject)

        btn_sauvegarder = QPushButton("SAUVEGARDER")
        btn_sauvegarder.setStyleSheet(btn_accent_style())
        btn_sauvegarder.clicked.connect(self._sauvegarder)

        btn_row.addWidget(btn_annuler)
        btn_row.addWidget(btn_sauvegarder)
        layout.addLayout(btn_row)

    def _maj_avatar_dialog(self):
        pix = _pix_absolu(getattr(self.utilisateur, 'photo', None), 100, 100)
        if pix:
            self.avatar_label.setPixmap(pix)
            self.avatar_label.setText("")
            self.avatar_label.setStyleSheet("border-radius: 50px;")
        else:
            self.avatar_label.setText("👤")
            self.avatar_label.setStyleSheet(
                f"background-color: {PINK_COLOR}; border-radius: 50px; font-size: 45px;"
            )

    def _choisir_photo(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Choisir une photo de profil", "", "Images (*.png *.jpg *.jpeg *.webp)"
        )
        if not path:
            return
        os.makedirs(PHOTOS_DIR, exist_ok=True)
        filename = os.path.basename(path)
        dest = os.path.join(PHOTOS_DIR, filename)
        shutil.copy2(path, dest)
        chemin = f"assets/photos/{filename}"
        self.utilisateur.photo = chemin
        from db.db import update_utilisateur_photo
        update_utilisateur_photo(self.utilisateur.id, chemin)
        from PyQt5.QtGui import QPixmap
        from PyQt5.QtCore import Qt
        pix = QPixmap(dest).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        if not pix.isNull():
            self.avatar_label.setPixmap(pix)
            self.avatar_label.setText("")
            self.avatar_label.setStyleSheet("border-radius: 50px;")

    def _sauvegarder(self):
        pseudo = self.input_pseudo.text().strip() or None
        mail = self.input_mail.text().strip() or None
        localisation = self.input_localisation.text().strip() or None
        ancien_mdp = self.input_ancien_mdp.text()
        nouveau_mdp = self.input_nouveau_mdp.text()

        if nouveau_mdp:
            ok = self.utilisateur.set_mot_de_passe(ancien_mdp, nouveau_mdp)
            if not ok:
                self.label_erreur.setText("Ancien mot de passe incorrect.")
                return

        self.utilisateur.modifier_profil(pseudo, mail, localisation)
        self.accept()


class ProfilPage(QWidget):
    """Page profil de l'utilisateur connecté."""

    article_clique = pyqtSignal(object)

    def __init__(self, plateforme, utilisateur):
        super().__init__()
        self.plateforme = plateforme
        self.utilisateur = utilisateur
        self.setStyleSheet(f"background-color: {BG_COLOR};")
        self._init_ui()

    def _init_ui(self):
        self.layout_principal = QHBoxLayout(self)
        self.layout_principal.setContentsMargins(40, 30, 40, 30)
        self.layout_principal.setSpacing(50)

        # --- GAUCHE ---
        left = QVBoxLayout()
        left.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        left.setSpacing(14)

        self.avatar = QLabel()
        self.avatar.setFixedSize(180, 180)
        self.avatar.setAlignment(Qt.AlignCenter)
        self._maj_avatar()
        left.addWidget(self.avatar, alignment=Qt.AlignCenter)

        self.label_pseudo = QLabel(f"@{self.utilisateur.pseudo.upper()}")
        self.label_pseudo.setStyleSheet(label_accent(18))
        self.label_pseudo.setAlignment(Qt.AlignCenter)
        left.addWidget(self.label_pseudo)

        stats = QHBoxLayout()
        stats.setAlignment(Qt.AlignCenter)
        stats.setSpacing(30)
        from db.db import get_nb_abonnes, get_nb_abonnements
        abonnes = get_nb_abonnes(self.utilisateur.id)
        abonnements = get_nb_abonnements(self.utilisateur.id)
        for valeur, libelle in [(abonnes, "ABONNÉS"), (abonnements, "ABONNEMENTS")]:
            col = QVBoxLayout()
            col.setAlignment(Qt.AlignCenter)
            v = QLabel(str(valeur))
            v.setStyleSheet(label_white(18) + " font-weight: bold;")
            v.setAlignment(Qt.AlignCenter)
            l = QLabel(libelle)
            l.setStyleSheet(label_dim(9) + " letter-spacing: 2px;")
            l.setAlignment(Qt.AlignCenter)
            col.addWidget(v)
            col.addWidget(l)
            stats.addLayout(col)
        left.addLayout(stats)

        for texte, slot in [("MODIFIER LE PROFIL", self._ouvrir_edition_profil),
                             ("PORTE MONNAIE", None),
                             ("MES ANNONCES", None)]:
            btn = self._btn_texte(texte)
            if slot:
                btn.clicked.connect(slot)
            left.addWidget(btn)

        left.addStretch()
        self.layout_principal.addLayout(left)

        # --- DROITE ---
        right = QVBoxLayout()
        right.setAlignment(Qt.AlignTop)
        right.setSpacing(10)

        btn_params = self._btn_texte("DECONNEXION")
        btn_params.clicked.connect(self._ouvrir_parametres)
        right.addWidget(btn_params, alignment=Qt.AlignRight)

        btn_eval = self._btn_texte("MES EVALUATIONS")
        right.addWidget(btn_eval, alignment=Qt.AlignRight)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border: none; background: transparent;")
        self.scroll.setMaximumHeight(380)

        self.container = QWidget()
        self.container.setStyleSheet("background: transparent;")
        self.grid = QGridLayout(self.container)
        self.grid.setSpacing(10)
        self.grid.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.scroll.setWidget(self.container)

        right.addWidget(self.scroll)
        right.addStretch()
        self.layout_principal.addLayout(right)

        self._afficher_annonces()

    def _maj_avatar(self):
        pix = _pix_absolu(getattr(self.utilisateur, 'photo', None), 180, 180)
        if pix:
            self.avatar.setPixmap(pix)
            self.avatar.setText("")
            self.avatar.setStyleSheet("border-radius: 90px;")
        else:
            self.avatar.clear()
            self.avatar.setText("👤")
            self.avatar.setStyleSheet(
                f"background-color: {PINK_COLOR}; border-radius: 90px; font-size: 75px;"
            )

    def showEvent(self, event):
        super().showEvent(event)
        self._afficher_annonces()

    def _afficher_annonces(self):
        for i in reversed(range(self.grid.count())):
            w = self.grid.itemAt(i).widget()
            if w:
                w.setParent(None)

        vendeur = self.plateforme.en_tant_que_vendeur(self.utilisateur)
        vendus, en_vente = vendeur.mes_articles()
        tous = en_vente + vendus

        for i, article in enumerate(tous[:9]):
            frame = QFrame()
            frame.setFixedSize(170, 245)
            frame.setStyleSheet(f"background-color: {MUTED_COLOR}; border-radius: 4px;")
            fl = QVBoxLayout(frame)
            fl.setContentsMargins(0, 0, 0, 8)
            fl.setSpacing(4)

            photo_lbl = QLabel()
            photo_lbl.setFixedSize(170, 120)
            photo_lbl.setAlignment(Qt.AlignCenter)
            pix = _pix_absolu(getattr(article, 'photo', None), 170, 120)
            if pix:
                photo_lbl.setPixmap(pix)
            else:
                photo_lbl.setText("📷")
                photo_lbl.setStyleSheet(photo_placeholder_style() + " font-size: 28px;")
            fl.addWidget(photo_lbl)

            lbl = QLabel(article.nom.upper()[:22])
            lbl.setStyleSheet(label_accent(9) + " letter-spacing: 1px;")
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setWordWrap(True)

            statut = QLabel("VENDU" if article.vendu else "EN VENTE")
            statut.setStyleSheet(
                f"color: {'#ff4444' if article.vendu else '#44ff88'}; font-size: 9px; letter-spacing: 1px;"
            )
            statut.setAlignment(Qt.AlignCenter)

            fl.addWidget(lbl)
            fl.addWidget(statut)

            if not article.vendu:
                frame.setCursor(Qt.PointingHandCursor)
                frame.mousePressEvent = lambda e, a=article: self.article_clique.emit(a)

                btn_style_rouge = f"""
                    QPushButton {{
                        color: #ff4444; background: transparent;
                        border: 1px solid #ff4444; border-radius: 8px;
                        padding: 2px 8px; font-size: 8px; font-weight: bold; letter-spacing: 1px;
                    }}
                    QPushButton:hover {{ background-color: #ff4444; color: {BG_COLOR}; }}
                """
                btn_style_bleu = f"""
                    QPushButton {{
                        color: {ACCENT_COLOR}; background: transparent;
                        border: 1px solid {ACCENT_COLOR}; border-radius: 8px;
                        padding: 2px 8px; font-size: 8px; font-weight: bold; letter-spacing: 1px;
                    }}
                    QPushButton:hover {{ background-color: {ACCENT_COLOR}; color: {BG_COLOR}; }}
                """

                btns = QHBoxLayout()
                btns.setSpacing(6)
                btns.setContentsMargins(8, 0, 8, 0)

                btn_editer = QPushButton("ÉDITER")
                btn_editer.setStyleSheet(btn_style_bleu)
                btn_editer.clicked.connect(lambda checked, a=article: self._editer_article(a))

                btn_retirer = QPushButton("RETIRER")
                btn_retirer.setStyleSheet(btn_style_rouge)
                btn_retirer.clicked.connect(lambda checked, a=article, v=vendeur: self._retirer_article(a, v))

                btns.addWidget(btn_editer)
                btns.addWidget(btn_retirer)
                fl.addLayout(btns)

            fl.addStretch()
            self.grid.addWidget(frame, i // 3, i % 3)

    def _editer_article(self, article):
        dialog = EditArticleDialog(article, self)
        if dialog.exec_() == QDialog.Accepted:
            self._afficher_annonces()

    def _retirer_article(self, article, vendeur):
        rep = QMessageBox.question(
            self, "Retirer l'article",
            f"Retirer '{article.nom}' de la vente ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if rep == QMessageBox.Yes:
            vendeur.retirer_article(article)
            if article in self.plateforme.articles:
                self.plateforme.articles.remove(article)
            self._afficher_annonces()

    def _btn_texte(self, texte):
        btn = QPushButton(texte)
        btn.setStyleSheet(f"""
            QPushButton {{
                color: {WHITE}; background: transparent; border: none;
                font-size: 13px; font-weight: bold; letter-spacing: 2px;
                padding: 6px 0;
            }}
            QPushButton:hover {{ color: {ACCENT_COLOR}; }}
        """)
        return btn

    def _ouvrir_edition_profil(self):
        dialog = EditProfilDialog(self.utilisateur, self)
        if dialog.exec_() == QDialog.Accepted:
            self.label_pseudo.setText(f"@{self.utilisateur.pseudo.upper()}")
            self._maj_avatar()
            QMessageBox.information(self, "Profil", "Profil mis à jour avec succès !")

    def _ouvrir_parametres(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Déconnexion")
        msg.setText(f"Connecté en tant que @{self.utilisateur.pseudo}")
        msg.setStyleSheet(f"""
            QMessageBox {{ background-color: {BG_COLOR}; }}
            QMessageBox QLabel {{ color: {WHITE}; font-size: 13px; }}
            QMessageBox QPushButton {{
                color: {WHITE};
                background-color: {MUTED_COLOR};
                border: 1px solid {ACCENT_COLOR};
                border-radius: 4px;
                padding: 6px 14px;
                font-weight: bold;
            }}
            QMessageBox QPushButton:hover {{ color: {ACCENT_COLOR}; }}
        """)
        btn_deco = msg.addButton("Se déconnecter", QMessageBox.ActionRole)
        msg.addButton("Annuler", QMessageBox.RejectRole)
        msg.exec_()

        if msg.clickedButton() == btn_deco:
            self.plateforme.deconnecter_utilisateur()
            from ui.login_window import LoginWindow
            self.login = LoginWindow(self.plateforme)
            self.login.show()
            self.window().close()
