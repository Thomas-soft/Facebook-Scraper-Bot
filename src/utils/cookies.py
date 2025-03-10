# Description: Module pour gérer les cookies du navigateur
# Version: 1.0

import os
import pickle
from utils.cursor import FakeCursor


COOKIES_FILE = ".cookies.pkl"


def save_cookies(driver):
    """Sauvegarde les cookies actuels dans un fichier"""
    with open(COOKIES_FILE, "wb") as file:
        pickle.dump(driver.get_cookies(), file)
    print("✅ Cookies sauvegardés.")


def load_cookies(driver):
    """Charge les cookies depuis un fichier et les applique au navigateur"""
    if os.path.exists(COOKIES_FILE):
        with open(COOKIES_FILE, "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        print("✅ Cookies chargés.")


def has_saved_cookies():
    """Vérifie si des cookies existent"""
    return os.path.exists(COOKIES_FILE)
