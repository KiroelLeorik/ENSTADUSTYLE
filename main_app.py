"""----------- Author : LARDILLIER Léo -------------

Point d'entrée du programme ENST'AS DU STYLE.
Lance l'interface graphique PyQt5.
"""

import sys
from PyQt5.QtWidgets import QApplication
from models.plateforme import Plateforme


def init_plateforme() -> Plateforme:
    """Initialise et charge la plateforme depuis la BDD."""
    p = Plateforme()
    p.charger_depuis_bdd()
    return p


if __name__ == "__main__":
    p = init_plateforme()

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Fenêtre de login
    from ui.login_window import LoginWindow
    login = LoginWindow(p)
    login.show()

    sys.exit(app.exec_())
