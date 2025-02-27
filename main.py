import time
import random
import math
import dotenv
import os
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from moveMouse import random_mouse_move
from utils import login


dotenv.load_dotenv()
# Configuration d'empreinte digitale réaliste
USER_AGENT_REAL = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/115.0.0.0 Safari/537.36"
)
VIEWPORT_SIZE = {"width": random.randint(900, 1100), "height": random.randint(800, 900)}
LOCALE = "fr-FR"
TIMEZONE_ID = "Europe/Paris"
PROXY_SERVER = None  # Exemple : "http://username:password@proxyserver.com:port"

def main():
    """
    Main function to launch the browser, navigate to Facebook, and perform automated actions.

    Parameters:
    None

    Returns:
    None
    """
    with sync_playwright() as p:
        launch_args = [
            "--incognito",
            "--disable-background-networking",
            "--disable-sync",
            "--disable-translate",
            "--no-first-run",
            "--no-default-browser-check",
        ]
        browser_options = {"headless": False, "args": launch_args}
        if PROXY_SERVER:
            browser_options["proxy"] = {"server": PROXY_SERVER}
        
        browser = p.chromium.launch(**browser_options)
        
        context = browser.new_context(
            user_agent=USER_AGENT_REAL,
            viewport=VIEWPORT_SIZE,
            locale=LOCALE,
            timezone_id=TIMEZONE_ID,
        )
        
        # Injection d'init script pour masquer certains indicateurs d'automatisation
        context.add_init_script("""
            (() => {
                // Masquer le flag webdriver
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                window.chrome = { runtime: {} };
                Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
                Object.defineProperty(navigator, 'languages', { get: () => ['fr-FR', 'en-US', 'en'] });
                Object.defineProperty(navigator, 'vendor', { get: () => "Google Inc." });
                delete window._phantom;
                delete window.callPhantom;
                
                // Initialiser la position de la souris
                window.lastMousePosition = {x: 0, y: 0};
                // Mettre à jour la position à chaque mouvement
                document.addEventListener('mousemove', e => {
                    window.lastMousePosition = {x: e.clientX, y: e.clientY};
                });

                // Masquer les propriétés spécifiques à Playwright
                Object.defineProperty(navigator, 'maxTouchPoints', { get: () => 1 });
                Object.defineProperty(navigator.connection, 'rtt', { get: () => 50 });
                Object.defineProperty(navigator.connection, 'downlink', { get: () => 10 });
            })();
        """)


        
        page = context.new_page()
        
        # Appliquer les techniques stealth
        stealth_sync(page)
        
        # Accéder à Facebook en français
        page.goto("https://www.facebook.com/?locale=fr_FR", timeout=60000)

        # Injection du curseur personnalisé dans le DOM
        page.evaluate('''() => {
            if (!document.getElementById("custom-cursor")) {
                const cursor = document.createElement("div");
                cursor.id = "custom-cursor";
                cursor.style.position = "fixed";
                cursor.style.width = "15px";
                cursor.style.height = "15px";
                cursor.style.background = "red";
                cursor.style.borderRadius = "50%";
                cursor.style.zIndex = "10000";
                cursor.style.pointerEvents = "none";
                cursor.style.transition = "left 0.05s linear, top 0.05s linear";
                document.body.appendChild(cursor);
            }
        }''')

        login(page)

        input("Appuyez sur Entrée pour fermer le navigateur...")
        browser.close()


if __name__ == "__main__":
    main()
