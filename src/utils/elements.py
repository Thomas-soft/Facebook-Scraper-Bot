# Description: Fonctions utilitaires pour manipuler des éléments sur une page web.
# Version: 1.0

import random
import time
import pyautogui
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def wait_for_element(driver, xpath, timeout=10):
    """Attend qu'un élément soit présent avant de continuer."""
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))


def get_element_screen_position(driver, element):
    """Retourne la position d'un élément par rapport à l'écran."""
    x_page, y_page = element.location['x'], element.location['y']
    window_x = driver.execute_script("return window.screenX;")
    window_y = driver.execute_script("return window.screenY;")
    scroll_x = driver.execute_script("return window.scrollX;")
    scroll_y = driver.execute_script("return window.scrollY;")

    # Hauteur des barres Chrome
    outer_height = driver.execute_script("return window.outerHeight;")
    inner_height = driver.execute_script("return window.innerHeight;")
    chrome_bar_height = outer_height - inner_height  # Barre d'onglets + barre de titre

    x_screen = window_x + x_page - scroll_x
    y_screen = window_y + y_page - scroll_y + chrome_bar_height

    return x_screen, y_screen


def find_element_and_click(driver, xpath):
    """Trouve un élément via son XPath et clique dessus avec pyautogui"""
    element = wait_for_element(driver, xpath)

    if element:
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
    else:
        print(f"⚠️ Élément non trouvé : {xpath}")
        return None
