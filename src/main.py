import undetected_chromedriver as uc
import pyautogui
import time
from cursor import FakeCursor


# Initialisation du navigateur avec undetected‑chromedriver
options = uc.ChromeOptions()
options.add_argument("--start-maximized")
driver = uc.Chrome(options=options)
driver.get("https://google.com")
time.sleep(2)  # Attendre le chargement complet de la page

# Création de l'instance du FakeCursor (singleton)
cursor = FakeCursor()

# Définir des positions (exemple : déplacer la souris de (100, 100) à (780, 766))
start_position = (100, 100)
end_position = (780, 766)

# Simulation d'un mouvement naturel de la souris
cursor.move_random(start_position, end_position)

# Simulation d'un clic à la position actuelle de la souris
cursor.click()

# Fermeture du navigateur
input("Press Enter to close the browser...")

driver.quit()
