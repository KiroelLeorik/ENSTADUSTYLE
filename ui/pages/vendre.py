"""----------- Author : LARDILLIER Léo / GREGOIRE Louna -------------"""

import os, shutil
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QLineEdit, QTextEdit, QComboBox,
                              QFrame, QGridLayout, QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt
from ui.styles import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PHOTOS_DIR = os.path.join(BASE_DIR, "assets", "photos")


class VendrePage(QWidget):
    """Formulaire de mise en vente d'un article."""

    def __init__(self, plateforme, utilisateur):
        super().__init__()
        self.plateforme = plateforme
        self.utilisateur = utilisateur
        self.photo_path = None
        self.setStyleSheet(f"background-color: {BG_COLOR};")
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(15)

        titre = QLabel("VENDRE")
        titre.setStyleSheet(label_accent(28) + " letter-spacing: 3px;")
        layout.addWidget(titre)

        body = QHBoxLayout()
        body.setSpacing(30)
        body.setAlignment(Qt.AlignTop)

        # --- PHOTO gauche ---
        photo_col = QVBoxLayout()
        photo_col.setSpacing(8)

        photo_main = QFrame()
        photo_main.setFixedSize(180, 190)
        photo_main.setStyleSheet(f"background-color: {MUTED_COLOR}; border-radius: 4px;")
        pm_layout = QVBoxLayout(photo_main)
        pm_layout.setContentsMargins(0, 0, 0, 0)
        self.photo_label = QLabel("📷")
        self.photo_label.setAlignment(Qt.AlignCenter)
        self.photo_label.setStyleSheet("font-size: 60px; background: transparent;")
        self.photo_label.setFixedSize(180, 190)
        pm_layout.addWidget(self.photo_label)
        photo_col.addWidget(photo_main)

        btn_choisir = QPushButton("+ Ajouter une photo")
        btn_choisir.setFixedSize(180, 45)
        btn_choisir.setStyleSheet(f"""
            QPushButton {{
                background-color: {MUTED_COLOR}; color: {WHITE};
                border: none; font-size: 13px; border-radius: 4px;
            }}
            QPushButton:hover {{ background-color: {ACCENT_COLOR}; color: {BG_COLOR}; }}
        """)
        btn_choisir.clicked.connect(self._choisir_photo)
        photo_col.addWidget(btn_choisir)

        body.addLayout(photo_col)

        # --- FORMULAIRE droite ---
        form = QVBoxLayout()
        form.setSpacing(10)
        form.setAlignment(Qt.AlignTop)

        inp_style = input_dashed_style()

        self.input_titre = QLineEdit()
        self.input_titre.setPlaceholderText("TITRE:")
        self.input_titre.setStyleSheet(inp_style)
        form.addWidget(self.input_titre)

        self.input_desc = QTextEdit()
        self.input_desc.setPlaceholderText("DESCRIPTION: Ajoute les informations utiles...")
        self.input_desc.setMaximumHeight(75)
        self.input_desc.setStyleSheet(inp_style)
        form.addWidget(self.input_desc)

        prix_row = QHBoxLayout()
        self.input_prix = QLineEdit()
        self.input_prix.setPlaceholderText("PRIX (€):")
        self.input_prix.setStyleSheet(inp_style)

        self.input_prix_min = QLineEdit()
        self.input_prix_min.setPlaceholderText("PRIX MIN (€):")
        self.input_prix_min.setStyleSheet(inp_style)

        prix_row.addWidget(self.input_prix)
        prix_row.addWidget(self.input_prix_min)
        form.addLayout(prix_row)

        body.addLayout(form)
        layout.addLayout(body)

        # --- CHAMPS DÉTAIL en grille ---
        grid = QGridLayout()
        grid.setSpacing(15)

        self.inputs = {}
        champs = [
            ("TAILLE:", "taille"), ("MATIÈRE:", "matiere"), ("MARQUE:", "marque"),
            ("GENRE:", "genre"), ("COULEUR:", "couleur"),
        ]
        for i, (placeholder, clé) in enumerate(champs):
            inp = QLineEdit()
            inp.setPlaceholderText(placeholder)
            inp.setStyleSheet(input_dashed_style())
            self.inputs[clé] = inp
            grid.addWidget(inp, i // 3, i % 3)

        self.combo_etat = QComboBox()
        self.combo_etat.addItems(["neuf", "tres_bon", "bon", "correct", "mauvais"])
        self.combo_etat.setStyleSheet(input_dashed_style())
        grid.addWidget(self.combo_etat, 1, 2)

        self.input_sous_cat = QLineEdit()
        self.input_sous_cat.setPlaceholderText("SOUS-CATÉGORIE:")
        self.input_sous_cat.setStyleSheet(input_dashed_style())
        grid.addWidget(self.input_sous_cat, 2, 0)

        layout.addLayout(grid)

        # Bouton VENDRE
        btn_vendre = QPushButton("VENDRE")
        btn_vendre.setStyleSheet(btn_accent_style())
        btn_vendre.setFixedWidth(160)
        btn_vendre.clicked.connect(self._publier)
        layout.addWidget(btn_vendre, alignment=Qt.AlignRight)

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
        self.photo_path = f"assets/photos/{filename}"
        from PyQt5.QtGui import QPixmap
        from PyQt5.QtCore import Qt
        pix = QPixmap(dest).scaled(180, 190, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        if not pix.isNull():
            self.photo_label.setPixmap(pix)
            self.photo_label.setText("")
            self.photo_label.setStyleSheet("")

    def _publier(self):
        from models.article import Vetement
        nom = self.input_titre.text().strip()
        if not nom:
            QMessageBox.warning(self, "Erreur", "Le titre est obligatoire.")
            return
        try:
            prix = float(self.input_prix.text() or "0")
            prix_min_txt = self.input_prix_min.text()
            prix_min = float(prix_min_txt) if prix_min_txt else prix * 0.7
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Le prix doit être un nombre.")
            return

        article = Vetement(
            id=None,
            nom=nom,
            description=self.input_desc.toPlainText(),
            categorie="Vêtements",
            prix_vendeur=prix,
            prix_min=prix_min,
            etat=self.combo_etat.currentText(),
            id_vendeur=self.utilisateur.id,
            date_publication=None,
            photo=self.photo_path,
            vendu=0,
            sous_categorie=self.input_sous_cat.text(),
            genre=self.inputs["genre"].text(),
            taille=self.inputs["taille"].text(),
            couleur=self.inputs["couleur"].text(),
            marque=self.inputs["marque"].text(),
            matiere=self.inputs["matiere"].text(),
        )

        try:
            vendeur = self.plateforme.en_tant_que_vendeur(self.utilisateur)
            vendeur.mettre_en_vente(article)
            self.plateforme.ajouter_article(article)
            QMessageBox.information(self, "Succès", f"'{article.nom}' mis en vente avec succès !")
            self._vider()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))

    def _vider(self):
        self.input_titre.clear()
        self.input_desc.clear()
        self.input_prix.clear()
        self.input_prix_min.clear()
        self.input_sous_cat.clear()
        for inp in self.inputs.values():
            inp.clear()
        self.photo_path = None
        self.photo_label.clear()
        self.photo_label.setText("📷")
        self.photo_label.setStyleSheet("font-size: 60px; background: transparent;")
