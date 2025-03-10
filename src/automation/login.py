# Description: Module de connexion à Facebook
# Version: 1.0

import random
import time
from utils.elements import find_element_and_click
from utils.elements import wait_for_element
from utils.cookies import save_cookies


def login(driver, email, password):
    """Effectue la connexion si nécessaire"""
    for field_xpath, value in [("//input[@id='email']", email), ("//input[@id='pass']", password)]:
        field = wait_for_element(driver, field_xpath)
        if field:
            field.clear()
            field.send_keys(value)
            time.sleep(random.uniform(0.5, 1.5))
    
    find_element_and_click(driver, "//button[@name='login']")
    time.sleep(random.uniform(2, 5))
    save_cookies(driver)
