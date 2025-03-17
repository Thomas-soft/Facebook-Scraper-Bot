# Description: Fonctions pour extraire des posts Facebook.
# Version: 1.1

import random
import time
import pyautogui
from selenium.webdriver.common.by import By
from utils.elements import get_element_screen_position
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from utils.csv import load_scraped_keys, save_posts_to_csv
from ia.analyse_post import is_website_selling
import platform
# from utils.elements import wait_for_element  # Make sure to import your wait_for_element function


def is_element_visible(driver, element, margin=250):
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
        # print(f"🔍 {len(buttons)} boutons 'See more' détectés.")
        for button in buttons:
            if is_element_visible(driver, button, margin=0):
                try:
                    x, y = get_element_screen_position(driver, button)
                    cursor.move_random(end=(x + 5, y + 2))
                    cursor.click()
                    print("🔘 Clic sur 'See more'")
                    # Petite pause pour que le contenu se charge
                    time.sleep(random.uniform(0.5, 1))
                except Exception as e:
                    print(f"⚠️ Erreur lors du clic sur 'See more' : {e}")
    except Exception as e:
        print(f"⚠️ Erreur lors de la récupération des boutons 'See more' : {e}")

# def click_author(driver, post_info, cursor):
#     """
#     Clique sur l'élément auteur d'un post en utilisant le clic du milieu via le fake cursor.
#     """
#     try:
#         auteur_element = post_info.get("Auteur_element")
#         if auteur_element is not None:
#             x, y = get_element_screen_position(driver, auteur_element)
#             cursor.move_random(end=(x + 5, y + 2))
#             cursor.middle_click()
#             print("🔘 Middle click sur l'auteur :", post_info.get("Auteur"))
#         else:
#             print("⚠️ Aucune référence à l'élément auteur n'a été trouvée pour ce post.")
#     except Exception as e:
#         print(f"⚠️ Erreur lors du clic sur l'auteur : {e}")


def wait_for_element(driver, xpath, timeout=10):
    """
    Waits for an element to be present in the DOM based on the given XPath.
    Returns the element if found, or None if not found within the timeout.
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element
    except Exception as e:
        print(f"⚠️ Wait for element failed for XPath '{xpath}': {e}")
        return None

def click_author(driver, post_info, cursor):
    """
    Clicks the author element of a post using a middle click via the fake cursor.
    Then, in the newly opened tab, the script:
      - Waits for and clicks the "Message" button (a div with aria-label="Message" or role="button")
      - Waits for and clicks the text input area (a div with role="textbox")
      - Types "Hi" using pyautogui
      - Closes the tab using the keyboard shortcut (ctrl+w or cmd+w)
    If the "Message" button (or text input) is not found, the tab is closed and control returns to the original tab.
    
    :param driver: Selenium WebDriver instance
    :param post_info: dictionary containing post info (must include "Auteur_element")
    :param cursor: FakeCursor instance for handling mouse movements/clicks
    """
    try:
        auteur_element = post_info.get("Auteur_element")
        if not auteur_element:
            print("⚠️ No reference to the author element was found for this post.")
            return

        # Retrieve the screen position of the author element and perform a middle click via the fake cursor
        x, y = get_element_screen_position(driver, auteur_element)
        cursor.move_random(end=(x + 5, y + 2))
        cursor.middle_click()
        print("🔘 Middle click on author:", post_info.get("Auteur"))

        # Save the original window handle
        original_window = driver.current_window_handle
        time.sleep(1)  # Wait for the new tab to open

        # Identify the new tab
        new_window = None
        for handle in driver.window_handles:
            if handle != original_window:
                new_window = handle
                break

        if not new_window:
            print("⚠️ No new tab found after clicking the author element.")
            return

        # Switch to the new tab
        driver.switch_to.window(new_window)
        print("🔄 Switched to author's tab")
        time.sleep(1)

        # --- Step 1: Click the "Message" button ---
        print("🔍 Looking for the 'Message' button...")
        msg_xpath = "//div[contains(., 'Message') and (@aria-label='Message' or @role='button')]"
        message_button = wait_for_element(driver, msg_xpath, timeout=10)
        if not message_button:
            print("⚠️ 'Message' button not found; closing the tab.")
            if platform.system() == "Darwin":
                pyautogui.hotkey("command", "w")
            else:
                pyautogui.hotkey("ctrl", "w")
            time.sleep(0.5)
            driver.switch_to.window(original_window)
            return
        else:
            x_btn, y_btn = get_element_screen_position(driver, message_button)
            cursor.move_random(end=(x_btn + 5, y_btn + 2))
            cursor.click()
            print("📩 'Message' button clicked")
        time.sleep(1)

        # --- Step 2: Click on the text input area ---
        print("🔍 Looking for the text input area...")
        input_xpath = "//div[@role='textbox']"
        message_input = wait_for_element(driver, input_xpath, timeout=10)
        if not message_input:
            print("⚠️ Text input not found; closing the tab.")
            if platform.system() == "Darwin":
                pyautogui.hotkey("command", "w")
            else:
                pyautogui.hotkey("ctrl", "w")
            time.sleep(0.5)
            driver.switch_to.window(original_window)
            return
        else:
            x_input, y_input = get_element_screen_position(driver, message_input)
            cursor.move_random(end=(x_input + 5, y_input + 2))
            cursor.click()
            print("📝 Text input clicked")
        time.sleep(1)

        # --- Step 3: Type "Hi" using pyautogui ---
        pyautogui.write("Hi", interval=0.1)
        print("⌨️ Typed 'Hi'")
        time.sleep(1)

        # --- Step 4: Close the tab using keyboard shortcut ---
        if platform.system() == "Darwin":
            pyautogui.hotkey("command", "w")
        else:
            pyautogui.hotkey("ctrl", "w")
        print("🗑 Closed author's tab using keyboard shortcut")
        time.sleep(0.5)
        driver.switch_to.window(original_window)
    except Exception as e:
        print(f"⚠️ Error during processing the author click: {e}")


def extract_post(driver):
    """Extrait plusieurs posts à partir de la div contenant role='feed'."""
    try:
        # print("🔍 Recherche de la section 'feed'...")
        feed = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='feed']"))
        )
        posts = feed.find_elements(By.XPATH, "./div")
        if not posts:
            print("❌ Aucun post trouvé.")
            return []
        nb_post = len(posts)
        print(f"📌 {nb_post - 4} post détectés. Extraction...")
        extracted_post = []
        for post in posts[1:nb_post - 3]:
            post_info = {}
            # Extraction de l'auteur
            try:
                auteur_element = post.find_element(By.XPATH, ".//h2 | .//span/strong")
                post_info["Auteur"] = auteur_element.text
                post_info["Auteur_element"] = auteur_element
            except:
                post_info["Auteur"] = "Inconnu"
            # Extraction du texte (on retire "See more" s'il est présent)
            try:
                message_div = post.find_element(By.XPATH, ".//div[@data-ad-rendering-role='story_message']")
                text_content = message_div.text.strip()
                if text_content:
                    # Suppression de "See more" du texte
                    post_info["Texte"] = text_content.replace("See more", "").strip()
                else:
                    post_info["Texte"] = "Aucun texte détecté"
            except:
                post_info["Texte"] = "Aucun texte détecté"
            # Extraction des images
            try:
                images = post.find_elements(By.XPATH, ".//img")
                image_urls = [
                    img.get_attribute("src") for img in images
                    if img.get_attribute("src")
                    and int(img.get_attribute("width") or 0) > 100
                    and int(img.get_attribute("height") or 0) > 100
                    and "emoji" not in img.get_attribute("src")
                ]
                post_info["Images"] = image_urls if image_urls else "Aucune image"
            except:
                post_info["Images"] = "Erreur lors de l'extraction"
            # Extraction des vidéos
            try:
                videos = post.find_elements(By.XPATH, ".//video")
                video_urls = [video.get_attribute("src") for video in videos if video.get_attribute("src")]
                post_info["Vidéos"] = video_urls if video_urls else "Aucune vidéo"
            except:
                post_info["Vidéos"] = "Erreur lors de l'extraction"
            # Extraction des liens externes
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
            # Extraction de la date
            try:
                post_info["Date"] = post.find_element(By.XPATH, ".//abbr | .//span[contains(@class, 'timestamp')]").text
            except:
                post_info["Date"] = "Non disponible"
            extracted_post.append(post_info)
        return extracted_post
    except Exception as e:
        print(f"⚠️ Erreur lors de l'extraction des post : {e}")
        return []

def scroll_and_extract(driver, cursor, csv_file="posts.csv", scroll_amount=-2, pause_time=0.1, max_iterations=5):
    """
    Défile la page, clique sur "See more" et extrait les posts visibles.
    L'extraction s'arrête dès que 'max_iterations' auteurs uniques ont été collectés.
    """
    posts = []
    seen_keys = set()
    seen_authors = set()
    first_run = not os.path.exists(csv_file)
    target_authors = max_iterations
    existing_keys = load_scraped_keys(csv_file)
    duplicate_counter = 0

    while True:
        pyautogui.scroll(scroll_amount)
        time.sleep(pause_time)
        click_see_more_buttons(driver, cursor)
        # Attendre un délai supplémentaire pour que le contenu complet soit chargé
        time.sleep(0.2)
        extracted = extract_post(driver)
        visible_posts = []
        for post in extracted:
            auteur_element = post.get("Auteur_element")
            if auteur_element and is_element_visible(driver, auteur_element):
                visible_posts.append(post)
            else:
                pass
                # print("Post ignoré car son auteur n'est pas visible à l'écran.")

        for post in visible_posts:
            auteur_text = post.get("Auteur", "").strip()
            texte_text = " ".join(post.get("Texte", "").split())
            key = (auteur_text, texte_text)
            if key in existing_keys or key in seen_keys or (auteur_text in seen_authors):
                duplicate_counter += 1
                # print("🔄 Post déjà scrappé ou auteur déjà traité :", key)
            else:
                duplicate_counter = 0
                seen_keys.add(key)
                posts.append(post)
                existing_keys.add(key)
                print("🆕 Nouveau post ajouté :", key)
                seen_author_num = len(seen_authors) + 1
                print(f"🔘 Auteur n°{seen_author_num} : {auteur_text}")
                seen_authors.add(auteur_text)
                if is_website_selling(driver, post.get("Texte", ""), post.get("Images", [])) == True:
                    print("🚀 Clic sur l'auteur...")
                    click_author(driver, post, cursor)
                else:
                    print("⚠️ Le post n'est pas une annonce de vente.")
            if len(seen_authors) >= target_authors:
                print(f"✅ Nombre d'auteurs cibles atteint ({target_authors}).")
                return posts
        if not first_run and duplicate_counter >= 3:
            print("⚠️ 3 posts consécutifs déjà scrapés rencontrés. Arrêt de l'extraction.")
            return posts
    return posts

def set_filter_recent(driver, cursor):
    """Définit le filtre des posts à 'Les plus récents'."""
    cursor.move_random(
        None,
        (
            random.randint(10, pyautogui.size()[0] - 10),
            random.randint(200, pyautogui.size()[1] - 10)
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