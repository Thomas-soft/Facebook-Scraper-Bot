import math
import random
import time


def human_scroll(page):
    """
    Simulates a smooth and progressive scroll like a human.

    Parameters:
    page (playwright.sync_api.Page): The page object to perform the scroll on.

    Returns:
    None
    """
    # Simuler l'appui sur "PageDown" de manière répétée
    for _ in range(2):
        page.keyboard.press("PageDown")
        time.sleep(random.uniform(0.5, 2))  # Pause aléatoire entre 0.5 et 2 secondes


def ease_out_back(t, overshoot=1.70158):
    """
    Easing function of type easeOutBack with overshoot parameter.
    Provides a slight overshoot before stabilizing.

    Parameters:
    t (float): The time parameter, typically between 0 and 1.
    overshoot (float): The overshoot parameter, default is 1.70158.

    Returns:
    float: The eased value.
    """
    c1 = overshoot
    c3 = c1 + 1
    return 1 + c3 * ((t - 1) ** 3) + c1 * ((t - 1) ** 2)


def quadratic_bezier(p0, p1, p2, t):
    """
    Calculates the point on a quadratic Bezier curve for a parameter t.

    Parameters:
    p0 (tuple): The start point of the curve (x, y).
    p1 (tuple): The control point of the curve (x, y).
    p2 (tuple): The end point of the curve (x, y).
    t (float): The parameter, typically between 0 and 1.

    Returns:
    tuple: The point on the Bezier curve (x, y).
    """
    x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
    y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
    return (x, y)


def random_mouse_move(page, start, end):
    """
    Moves the mouse in a very natural and different way each time it is called.

    Parameters:
    page (playwright.sync_api.Page): The page object to perform the mouse move on.
    start (tuple): The starting position of the mouse (x, y).
    end (tuple): The ending position of the mouse (x, y).

    Returns:
    None
    """
    # Randomisation du nombre d'étapes et du délai de base
    steps = random.randint(55, 65)
    base_delay = random.uniform(0.010, 0.015)
    
    x1, y1 = start
    x2, y2 = end
    
    # Calcul du point médian et de la distance
    mid = ((x1 + x2) / 2, (y1 + y2) / 2)
    dx = x2 - x1
    dy = y2 - y1
    distance = math.hypot(dx, dy)
    
    # Calcul du vecteur perpendiculaire normalisé
    if distance != 0:
        perp = (-dy / distance, dx / distance)
    else:
        perp = (0, 0)
        
    # Choix d'un offset aléatoire entre 5% et 15% de la distance
    offset = distance * random.uniform(0.05, 0.75)
    # Inverser aléatoirement la direction de l'offset
    if random.choice([True, False]):
        offset = -offset
    control = (mid[0] + perp[0] * offset, mid[1] + perp[1] * offset)
    
    # Randomisation du paramètre d'overshoot
    overshoot = random.uniform(0.6, 0.8)
    
    for i in range(1, steps + 1):
        t = i / steps
        # Appliquer l'easing avec overshoot pour un mouvement plus naturel
        eased_t = ease_out_back(t, overshoot=overshoot)
        # Calcul du point sur la courbe de Bézier
        bx, by = quadratic_bezier(start, control, end, eased_t)
        
        # Ajouter un jitter dégressif : amplitude aléatoire entre 3 et 7 pixels, maximale au milieu
        jitter_amplitude = random.uniform(0.5, 2) * math.sin(math.pi * t)
        bx += random.uniform(-jitter_amplitude, jitter_amplitude)
        by += random.uniform(-jitter_amplitude, jitter_amplitude)
        
        page.mouse.move(bx, by)
        time.sleep(base_delay * random.uniform(0.9, 1.1))

        # Mettre à jour la position du curseur personnalisé
        page.evaluate(f'''() => {{
            const cursor = document.getElementById("custom-cursor");
            if(cursor){{
                cursor.style.left = "{bx}px";
                cursor.style.top = "{by}px";
            }}
        }}''')