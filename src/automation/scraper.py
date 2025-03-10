# Description: Fonctions pour extraire des posts Facebook.
# Version: 1.1

import random
import time
import pyautogui
from selenium.webdriver.common.by import By
from utils.elements import get_element_screen_position
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def is_element_visible(driver, element, margin=100):
    """Vérifie si un élément est visible à l'écran en tenant compte d'une marge (par défaut 100px)."""
    screen_height = driver.execute_script("return window.innerHeight;")
    scroll_position = driver.execute_script("return window.scrollY;")
    element_y = element.location['y']
    return scroll_position <= element_y <= scroll_position + screen_height - margin


def click_see_more_buttons(driver, cursor):
    """Clique sur tous les boutons 'See more' visibles en utilisant le fake cursor.
       Pour ces boutons, on utilise une marge réduite afin de cliquer même s'ils se trouvent
       en bas de l'écran."""
    try:
        # Récupérer tous les boutons "See more"
        buttons = driver.find_elements(By.XPATH, "//div[text()='See more']")
        print(f"🔍 {len(buttons)} boutons 'See more' détectés.")
        for button in buttons:
            # Pour les boutons "See more", on vérifie la visibilité avec margin=0
            if is_element_visible(driver, button, margin=0):
                try:
                    # Récupérer la position à l'écran du bouton
                    x, y = get_element_screen_position(driver, button)
                    # Déplacer le curseur vers la position cible
                    cursor.move_random(end=(x + 5, y + 2))
                    # Effectuer un clic avec le fake cursor
                    cursor.click()
                    print("🔘 Clic sur 'See more'")
                    time.sleep(random.uniform(0.2, 0.5))  # Pause pour le chargement du contenu étendu
                except Exception as e:
                    print(f"⚠️ Erreur lors du clic sur 'See more' : {e}")
    except Exception as e:
        print(f"⚠️ Erreur lors de la récupération des boutons 'See more' : {e}")


def click_author(driver, post_info, cursor):
    """
    Clique sur l'élément auteur d'un post en utilisant le clic du milieu via le fake cursor.
    
    :param driver: instance Selenium du navigateur
    :param post_info: dictionnaire contenant les infos du post (doit contenir "Auteur_element")
    :param cursor: instance de FakeCursor
    """
    try:
        auteur_element = post_info.get("Auteur_element")
        if auteur_element is not None:
            # Récupérer la position de l'élément auteur
            x, y = get_element_screen_position(driver, auteur_element)
            # Déplacer le curseur vers l'élément
            cursor.move_random(end=(x + 5, y + 2))
            # Effectuer un clic du milieu
            cursor.middle_click()
            print("🔘 Middle click sur l'auteur :", post_info.get("Auteur"))
        else:
            print("⚠️ Aucune référence à l'élément auteur n'a été trouvée pour ce post.")
    except Exception as e:
        print(f"⚠️ Erreur lors du clic sur l'auteur : {e}")


def extract_post(driver, max_post=20):
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

        nb_post = len(post)
        print(f"📌 {nb_post - 4} post détectés. Extraction...")

        extracted_post = []

        for post in post[1:nb_post - 3]:  # Limiter le nombre de post à extraire
            post_info = {}

            # 🔹 Extraction de l'auteur
            try:
                auteur_element = post.find_element(By.XPATH, ".//h2 | .//span/strong")
                post_info["Auteur"] = auteur_element.text
                post_info["Auteur_element"] = auteur_element
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

        # # 📌 Affichage des post extraits
        # for i, post in enumerate(extracted_post, 1):
        #     print(f"\n✅ **Post {i} extrait :**")
        #     for key, value in post.items():
        #         print(f"{key}: {value}")

        return extracted_post

    except Exception as e:
        print(f"⚠️ Erreur lors de l'extraction des post : {e}")
        return []


def scroll_and_extract(driver, cursor, scroll_amount=-2, pause_time=0.1, max_iterations=20):
    """
    Défile la page en utilisant pyautogui.scroll(), clique sur "See more" pour étendre les descriptions longues,
    et extrait uniquement les posts visibles (vérifiés via is_element_visible sur l'élément auteur).
    Pour chaque nouveau post, effectue un clic du milieu sur l'auteur (une seule fois par auteur).
    """
    posts = []
    seen_keys = set()       # Pour mémoriser les posts déjà affichés
    clicked_authors = set() # Pour éviter de cliquer plusieurs fois sur le même auteur
    printed_count = 0       # Compteur pour la numérotation continue des posts affichés

    for i in range(max_iterations):
        # Utilisation de pyautogui pour défiler la page
        pyautogui.scroll(scroll_amount)
        time.sleep(pause_time)
        print(f"🔄 Itération {i+1} : défilement de la page avec pyautogui.scroll({scroll_amount})...")
        
        # Clique sur tous les boutons "See more" avant l'extraction
        click_see_more_buttons(driver, cursor)
        
        # Extraction de tous les posts (même ceux hors écran)
        extracted = extract_post(driver)
        
        # On ne conserve que les posts dont l'élément auteur est visible
        visible_posts = []
        for post in extracted:
            auteur_element = post.get("Auteur_element")
            if auteur_element and is_element_visible(driver, auteur_element):
                visible_posts.append(post)
            else:
                print("Post ignoré car son auteur n'est pas visible à l'écran.")
        
        new_posts = []
        for post in visible_posts:
            key = (post.get("Auteur"), post.get("Date"), post.get("Texte"))
            if key not in seen_keys:
                seen_keys.add(key)
                posts.append(post)
                new_posts.append(post)
        
        # Pour chaque nouveau post, cliquer sur l'auteur si ce n'est pas déjà fait
        if new_posts:
            for j, post in enumerate(new_posts, start=printed_count+1):
                auteur = post.get("Auteur")
                if auteur and auteur not in clicked_authors:
                    click_author(driver, post, cursor)
                    clicked_authors.add(auteur)
                else:
                    print(f"Auteur '{auteur}' déjà cliqué ou introuvable, passage au suivant.")
            printed_count += len(new_posts)
        else:
            print("Aucun nouveau post visible détecté à cette itération.")
        
        # On arrête l'extraction après un certain nombre de posts extraits
        if printed_count >= 50:
            break

    print(f"📝 Total posts extraits et traités : {printed_count}")
    print("🔚 Fin de l'extraction.")
    print("Récapitulatif des posts extraits :")
    for i, post in enumerate(posts, 1):
        print(f"\n✅ **Post {i} extrait :**")
        for key, value in post.items():
            print(f"{key}: {value}")
    return posts


def set_filter_recent(driver, cursor):
    """Définit le filtre des posts à 'Les plus récents'."""
    # Clic sur le bouton 'Les plus récents'
    cursor.move_random(
        None,
        (
            random.randint(10, pyautogui.size()[0] - 10),
            random.randint(200, 250)
        )
    )
    try:
        filter_button = driver.find_element(By.XPATH, "//span[text()='Most relevant']")
        if filter_button is None:
            print("⚠️ 'Most relevant' non trouvé.")
            return
        else:
            print("✅ 'Most relevant' trouvé.")
        if is_element_visible(driver, filter_button):
            x, y = get_element_screen_position(driver, filter_button)
            cursor.move_random(None, (x + 5, y + 2))
            cursor.click()
            print("🔘 Clic sur 'Most relevant'")
        else:
            while not is_element_visible(driver, filter_button):
                pyautogui.scroll(-1)
                time.sleep(random.uniform(0.01, 0.1))
            x, y = get_element_screen_position(driver, filter_button)
            cursor.move_random(None, (x + 5, y + 2))
            cursor.click()
        recent_button = driver.find_element(By.XPATH, "//span[text()='Recent activity']")
        if recent_button is None:
            print("⚠️ 'Recent activity' non trouvé.")
            return
        else:
            print("✅ 'Recent activity' trouvé.")
        if is_element_visible(driver, recent_button):
            x, y = get_element_screen_position(driver, recent_button)
            cursor.move_random(None, (x + 5, y + 2))
            cursor.click()
            print("🔘 Clic sur 'Recent activity'")
        else:
            while not is_element_visible(driver, recent_button):
                pyautogui.scroll(-1)
                time.sleep(random.uniform(0.01, 0.1))
            x, y = get_element_screen_position(driver, recent_button)
            cursor.move_random(None, (x + 5, y + 2))
            cursor.click()
        time.sleep(0.6)
    except Exception as e:
        print(f"⚠️ Erreur lors du clic sur 'Most relevant' : {e}")
