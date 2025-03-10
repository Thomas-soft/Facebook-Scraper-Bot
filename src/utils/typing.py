# Description: Module pour simuler la frappe d'un humain
# Version: 1.0

import pyautogui
import random
import time


def type_like_human(text):
    for char in text:
        pyautogui.write(char)
        time.sleep(random.uniform(0.05, 0.1))  # Pause aléatoire entre 50ms et 200ms
