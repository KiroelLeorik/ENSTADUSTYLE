from PyQt5.QtWidgets import QApplication
from ui.login_window import LoginWindow
import sys
from models.plateforme import Plateforme

def init_plateforme() -> Plateforme:
    """Initialise et charge la plateforme depuis la BDD."""
    p = Plateforme()
    p.charger_depuis_bdd()
    return p

if __name__ == '__main__':
    p = init_plateforme()
    app = QApplication(sys.argv)
    window = LoginWindow(p)
    window.show()
    sys.exit(app.exec_())