import os
import random
import time
from moveMouse import random_mouse_move


def login(page):
    # Laisser un peu de temps pour que l'utilisateur (ou le script) génère un mouvement
    time.sleep(random.randint(3, 5))
    
    # Récupérer la position actuelle de la souris depuis la page
    pos = page.evaluate("() => window.lastMousePosition")
    # Si aucune position n'a été mise à jour, utiliser un fallback
    if not pos or (pos["x"] == 0 and pos["y"] == 0):
        start_pos = (100, 100)
    else:
        start_pos = (pos["x"], pos["y"])
    print(f"Position initiale de la souris récupérée : {start_pos}")
    
    # Simuler un comportement humain
    # 1. Cliquer sur le champ email
    email_input = page.wait_for_selector("#email")
    email_box = email_input.bounding_box()
    if email_box:
        email_center = (
            email_box["x"] + email_box["width"] / 2 + random.randint(-10, 10),
            email_box["y"] + email_box["height"] / 2 + random.randint(-10, 10)
        )
        random_mouse_move(page, start_pos, email_center)
        page.mouse.click(*email_center)
        page.keyboard.type(os.getenv("LOGIN"), delay=random.randint(110, 250))
        start_pos = email_center  # mise à jour
    else:
        print("Champ email introuvable.")
    
    time.sleep(random.randint(1, 3))
    
    # 2. Cliquer sur le champ password
    password_input = page.wait_for_selector("#pass")
    password_box = password_input.bounding_box()
    if password_box:
        password_center = (
            password_box["x"] + password_box["width"] / 2 + random.randint(-10, 10),
            password_box["y"] + password_box["height"] / 2 + random.randint(-10, 10)
        )
        random_mouse_move(page, start_pos, password_center)
        page.mouse.click(*password_center)
        page.keyboard.type(os.getenv("PASSWORD"), delay=random.randint(110, 250))
    else:
        print("Champ password introuvable.")

    time.sleep(random.randint(1, 3))

    # 3. Cliquer sur le bouton "Se connecter"
    # Ici, nous utilisons le sélecteur "button[name='login']"
    login_button = page.wait_for_selector("button[name='login']")
    login_box = login_button.bounding_box()
    if login_box:
        login_center = (
            login_box["x"] + login_box["width"] / 2,
            login_box["y"] + login_box["height"] / 2
        )
        random_mouse_move(page, start_pos, login_center)
        page.mouse.click(*login_center)
        print("Bouton 'Se connecter' cliqué.")
    else:
        print("Bouton 'Se connecter' introuvable.")

    # time.sleep(random.randint(5, 7))

    # # 4. Naviguer vers le groupe Facebook que vous avez rejoint
    # # Remplacez <GROUP_ID> par l'identifiant ou l'URL de votre groupe
    # GROUP_URL = "https://www.facebook.com/groups/websiteflippingcommunity/"
    # page.goto(GROUP_URL, timeout=60000)
    # print(f"Navigation vers le groupe : {GROUP_URL}")