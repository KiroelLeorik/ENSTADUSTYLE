"""----------- Author : LARDILLIER Léo / GREGOIRE Louna -------------
Constantes de style pour l'interface ENST'AS DU STYLE.
"""

# Couleurs
BG_COLOR = "#04041a"
SIDEBAR_COLOR = "#02020e"
CARD_COLOR = "#080820"
MUTED_COLOR = "#0d0d30"
ACCENT_COLOR = "#4466ff"
ACCENT_HOVER = "#6688ff"
PINK_COLOR = "#ff55aa"
WHITE = "#ffffff"
DIM_COLOR = "#4444aa"
BORDER_COLOR = "#1a1a44"
GOLD_COLOR = "#ffcc00"


def btn_accent_style():
    return f"""
        QPushButton {{
            color: {ACCENT_COLOR};
            background: transparent;
            border: 2px solid {ACCENT_COLOR};
            border-radius: 15px;
            padding: 8px 20px;
            font-weight: bold;
            letter-spacing: 2px;
            font-size: 12px;
        }}
        QPushButton:hover {{
            background-color: {ACCENT_COLOR};
            color: {BG_COLOR};
        }}
    """


def label_accent(size=14):
    return f"color: {ACCENT_COLOR}; font-size: {size}px; font-weight: bold; letter-spacing: 2px;"


def label_white(size=12):
    return f"color: {WHITE}; font-size: {size}px;"


def label_dim(size=11):
    return f"color: {DIM_COLOR}; font-size: {size}px;"


def input_dashed_style():
    return f"""
        QLineEdit, QTextEdit, QComboBox {{
            background-color: transparent;
            color: {WHITE};
            border: none;
            border-bottom: 1px dashed {ACCENT_COLOR};
            font-size: 12px;
            letter-spacing: 2px;
            padding: 5px;
        }}
        QComboBox::drop-down {{ border: none; }}
        QComboBox QAbstractItemView {{
            background-color: {MUTED_COLOR};
            color: {WHITE};
            border: 1px solid {ACCENT_COLOR};
        }}
    """


def nav_btn_style():
    return f"""
        QPushButton {{
            color: {ACCENT_COLOR};
            background: transparent;
            border: none;
            font-size: 28px;
            font-weight: bold;
            padding: 5px 10px;
        }}
        QPushButton:hover {{ color: {WHITE}; }}
        QPushButton:disabled {{ color: {DIM_COLOR}; }}
    """


def sidebar_btn_style():
    return f"""
        QPushButton {{
            color: {ACCENT_COLOR};
            background: transparent;
            border: none;
            font-size: 16px;
            padding: 12px 5px;
            text-align: left;
            letter-spacing: 1px;
        }}
        QPushButton:hover {{ color: {WHITE}; }}
    """


def icon_btn_style():
    return f"""
        QPushButton {{
            color: {ACCENT_COLOR};
            background: transparent;
            border: none;
            font-size: 22px;
            font-weight: bold;
        }}
        QPushButton:hover {{ color: {WHITE}; }}
    """


def photo_placeholder_style():
    return f"background-color: #0a0a30; color: {DIM_COLOR}; font-size: 40px; border-radius: 4px;"
