import sqlite3
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
con = sqlite3.connect(os.path.join(BASE_DIR, "../marche.db"))


def get_connection():
