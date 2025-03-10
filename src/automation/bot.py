# Description: Fichier principal du bot d'automatisation
# Version: 1.0

from automation.scraper import extract_post, set_filter_recent, scroll_and_extract
from automation.navigation import redirect_to_group
from utils.cookies import has_saved_cookies, load_cookies
from automation.login import login
import time
from utils.cursor import FakeCursor


cursor = FakeCursor()


def run_bot(driver, facebook_url, facebook_group_url, email, password):
    """Orchestration du bot"""
    if has_saved_cookies():
        print("🟢 Chargement des cookies existants...")
        driver.get(facebook_url)
        load_cookies(driver)
        time.sleep(2)
        driver.refresh()
    else:
        print("🔑 Aucun cookie trouvé. Connexion requise.")
        driver.get(facebook_url)
        login(driver, email, password)

    redirect_to_group(driver, facebook_group_url)
    time.sleep(3)
    set_filter_recent(driver, cursor)
    time.sleep(3)
    scroll_and_extract(driver, cursor)

    input("Press Enter to close the browser...")
    driver.quit()
