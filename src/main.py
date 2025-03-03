import undetected_chromedriver as uc
from dotenv import load_dotenv
import pyautogui
import random
import time
import os
import pickle
from cursor import FakeCursor
from utils import type_like_human
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Charger les variables d'environnement depuis .env
load_dotenv()
EMAIL = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")
FB_WEBSITE_URL = os.getenv("FACEBOOK_URL")
FB_GROUP_URL = os.getenv("FACEBOOK_GROUP_LINK")

# Initialisation du navigateur avec undetected‑chromedriver
options = uc.ChromeOptions()
options.add_argument("--start-maximized")
driver = uc.Chrome(options=options)

COOKIES_FILE = ".cookies.pkl"


def save_cookies():
    """Sauvegarde les cookies actuels dans un fichier"""
    with open(COOKIES_FILE, "wb") as file:
        pickle.dump(driver.get_cookies(), file)
    print("✅ Cookies sauvegardés.")


def load_cookies():
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


def wait_for_element(xpath, timeout=10):
    """Attend qu'un élément soit présent avant de continuer."""
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))


def find_element_and_click(xpath):
    element = wait_for_element(xpath)
    rect = element.rect
    window_rect = driver.get_window_rect()
    window_x, window_y = window_rect["x"], window_rect["y"]
    viewport_height = driver.execute_script("return window.innerHeight;")
    toolbar_height = window_rect["height"] - viewport_height
    target_x = window_x + rect["x"] + rect["width"] // 2
    target_y = window_y + toolbar_height + rect["y"] + rect["height"] // 2
    pyautogui.moveTo(target_x, target_y, duration=random.uniform(0.3, 0.7))
    pyautogui.click()
    return element


def decline_cookies():
    try:
        decline_button_xpath = '//span[contains(text(), "Decline optional cookies")]/parent::*'
        print("Recherche du bouton 'Decline optional cookies'...")
        find_element_and_click(decline_button_xpath)
        time.sleep(random.uniform(1, 2))
    except Exception as e:
        print(f"Erreur lors du refus des cookies : {e}")


def login():
    """Effectue la connexion si nécessaire"""
    for field_xpath, value in [("//input[@id='email']", EMAIL), ("//input[@id='pass']", PASSWORD)]:
        field = find_element_and_click(field_xpath)
        if field.get_attribute("value"):
            field.clear()
        time.sleep(random.uniform(0.5, 1.5))
        type_like_human(value)
    find_element_and_click("//button[@name='login']")
    time.sleep(random.uniform(2, 5))
    save_cookies()  # Sauvegarde les cookies après connexion réussie


def redirect_to_group():
    print(f"Redirection vers le groupe Facebook : {FB_GROUP_URL}")
    driver.get(FB_GROUP_URL)


def change_post_order():
    try:
        # Cliquer sur "Most relevant"
        print("Ouverture du menu des posts...")
        most_relevant_xpath = "//span[contains(text(), 'Most relevant')]"
        find_element_and_click(most_relevant_xpath)
        time.sleep(random.uniform(0.5, 1))
        
        # Cliquer sur "Show recent posts first"
        print("Sélection de 'Show recent posts first'...")
        recent_posts_xpath = "//span[contains(text(), 'Show recent posts first')]"
        find_element_and_click(recent_posts_xpath)
    except Exception as e:
        print(f"Erreur lors du changement d'ordre des posts : {e}")


def extract_first_post():
    """Extrait le maximum d'informations du premier post affiché."""
    try:
        print("Recherche du premier post...")

        # Trouver tous les posts en utilisant l'attribut aria-posinset
        posts = driver.find_elements(By.CSS_SELECTOR, "div[aria-posinset]")

        if not posts:
            print("Aucun post trouvé.")
            return

        first_post = posts[0]  # Sélectionne le premier post affiché
        post_info = {}

        # Extraction de l'auteur
        try:
            post_info["Auteur"] = first_post.find_element(By.XPATH, ".//h2 | .//span/strong").text
        except:
            post_info["Auteur"] = "Inconnu"

        # Extraction de la date
        try:
            post_info["Date"] = first_post.find_element(By.XPATH, ".//abbr | .//span[contains(@class, 'timestamp')]").text
        except:
            post_info["Date"] = "Non disponible"

        # Extraction du texte du post
        try:
            post_info["Texte"] = first_post.find_element(By.XPATH, ".//div[contains(@data-ad-preview, 'message')]").text
        except:
            post_info["Texte"] = "Aucun texte détecté"

        # Extraction des images du post
        post_info["Images"] = []
        try:
            images = first_post.find_elements(By.TAG_NAME, "img")
            for img in images:
                img_src = img.get_attribute("src")
                if img_src and "emoji" not in img_src:
                    post_info["Images"].append(img_src)
        except:
            pass

        # Extraction des liens externes
        post_info["Liens"] = []
        try:
            links = first_post.find_elements(By.TAG_NAME, "a")
            for link in links:
                href = link.get_attribute("href")
                if href and "facebook.com" not in href:
                    post_info["Liens"].append(href)
        except:
            pass

        # Affichage des informations du post
        print("\n✅ **Informations du post extrait :**")
        for key, value in post_info.items():
            if isinstance(value, list):
                print(f"{key}:")
                for item in value:
                    print(f"  - {item}")
            else:
                print(f"{key}: {value}")

    except Exception as e:
        print(f"Erreur lors de l'extraction du premier post : {e}")


# ✅ Vérifie si des cookies existent
if has_saved_cookies():
    print("🟢 Chargement des cookies existants...")
    driver.get(FB_WEBSITE_URL)
    load_cookies()
    time.sleep(2)
    driver.refresh()  # Rafraîchit la page pour activer les cookies
else:
    print("🔑 Aucun cookie trouvé. Connexion requise.")
    driver.get(FB_WEBSITE_URL)
    time.sleep(random.uniform(1, 3))
    decline_cookies()
    time.sleep(random.uniform(1, 3))
    login()

# ✅ Une fois connecté, continuer normalement
time.sleep(random.uniform(2, 5))
redirect_to_group()
# time.sleep(random.uniform(1, 3))
# change_post_order()
time.sleep(random.uniform(5, 10))
extract_first_post()

input("Press Enter to close the browser...")
driver.quit()
