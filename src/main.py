# Description: Bot qui permet de scrapper les publications d'un groupe Facebook
# Version: 1.0

import os
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from automation.bot import run_bot


def main():
    # Charger les variables d'environnement
    load_dotenv()
    EMAIL = os.getenv("LOGIN")
    PASSWORD = os.getenv("PASSWORD")
    FB_WEBSITE_URL = os.getenv("FACEBOOK_URL")
    FB_GROUP_URL = os.getenv("FACEBOOK_GROUP_LINK")

    # Initialisation du navigateur
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = uc.Chrome(driver_executable_path=ChromeDriverManager().install(), options=options)

    COOKIES_FILE = ".cookies.pkl"

    # Lancement du bot
    run_bot(driver, FB_WEBSITE_URL, FB_GROUP_URL, EMAIL, PASSWORD)


if __name__ == "__main__":
    main()
