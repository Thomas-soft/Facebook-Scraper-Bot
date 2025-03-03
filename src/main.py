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
        print("Ouverture du menu des post...")
        most_relevant_xpath = "//span[contains(text(), 'Most relevant')]"
        find_element_and_click(most_relevant_xpath)
        time.sleep(random.uniform(0.5, 1))
        
        # Cliquer sur "Show recent post first"
        print("Sélection de 'Show recent post first'...")
        recent_post_xpath = "//span[contains(text(), 'Show recent post first')]"
        find_element_and_click(recent_post_xpath)
    except Exception as e:
        print(f"Erreur lors du changement d'ordre des post : {e}")


def extract_post(driver, max_post=5):
    """Extrait plusieurs post à partir de la div contenant role='feed'."""
    try:
        print("🔍 Recherche de la section 'feed'...")

        # Attendre que la div role="feed" apparaisse
        feed = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='feed']"))
        )

        # Récupérer **toutes** les div qui suivent immédiatement après cette div "feed"
        post = feed.find_elements(By.XPATH, "./div")

        if not post:
            print("❌ Aucun post trouvé.")
            return []

        print(f"📌 {len(post)} post détectés. Extraction des {min(len(post), max_post)} premiers.")

        extracted_post = []

        for post in post[1:max_post]:  # Limiter le nombre de post à extraire
            post_info = {}

            # 🔹 Extraction de l'auteur
            try:
                post_info["Auteur"] = post.find_element(By.XPATH, ".//h2 | .//span/strong").text
            except:
                post_info["Auteur"] = "Inconnu"

            # 🔹 Recherche de la div avec data-ad-rendering-role="story_message"
            try:
                message_div = post.find_element(By.XPATH, ".//div[@data-ad-rendering-role='story_message']")
                text_content = message_div.text.strip()
                if text_content:
                    post_info["Texte"] = text_content
                else:
                    post_info["Texte"] = "Aucun texte détecté"
            except:
                post_info["Texte"] = "Aucun texte détecté"

            # 4️⃣ Images du post (en filtrant les emojis)
            try:
                images = post.find_elements(By.XPATH, ".//img")

                # Filtrer les images : prendre celles dont la largeur/hauteur est > 100 pixels et qui ne sont pas des emojis
                image_urls = [
                    img.get_attribute("src") for img in images
                    if img.get_attribute("src")
                    and int(img.get_attribute("width") or 0) > 100  # Largeur > 100
                    and int(img.get_attribute("height") or 0) > 100  # Hauteur > 100
                    and "emoji" not in img.get_attribute("src")  # Exclure les emojis
                ]

                post_info["Images"] = image_urls if image_urls else "Aucune image"
            except:
                post_info["Images"] = "Erreur lors de l'extraction"

            # 5️⃣ Vidéos du post
            try:
                videos = post.find_elements(By.XPATH, ".//video")
                video_urls = [video.get_attribute("src") for video in videos if video.get_attribute("src")]
                post_info["Vidéos"] = video_urls if video_urls else "Aucune vidéo"
            except:
                post_info["Vidéos"] = "Erreur lors de l'extraction"

            # 6️⃣ Liens externes
            try:
                links = post.find_elements(By.XPATH, ".//a")
                external_links = [
                    link.get_attribute("href")
                    for link in links
                    if link.get_attribute("href") and "facebook.com" not in link.get_attribute("href")
                ]
                post_info["Liens externes"] = external_links if external_links else "Aucun lien externe"
            except:
                post_info["Liens externes"] = "Erreur lors de l'extraction"

            # 🔹 Extraction de la date
            try:
                post_info["Date"] = post.find_element(By.XPATH, ".//abbr | .//span[contains(@class, 'timestamp')]").text
            except:
                post_info["Date"] = "Non disponible"

            extracted_post.append(post_info)

        # 📌 Affichage des post extraits
        for i, post in enumerate(extracted_post, 1):
            print(f"\n✅ **Post {i} extrait :**")
            for key, value in post.items():
                print(f"{key}: {value}")

        return extracted_post

    except Exception as e:
        print(f"⚠️ Erreur lors de l'extraction des post : {e}")
        return []


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
time.sleep(random.uniform(4, 7))
extract_post(driver, 5)

input("Press Enter to close the browser...")
driver.quit()
