"""
fake_cursor.py

Module pour simuler le mouvement naturel d'un curseur réel via PyAutoGUI.
Le mouvement est généré à l'aide d'une courbe de Bézier quadratique, d'une fonction d'easing (easeOutBack)
et d'un léger jitter pour imiter l'imprécision humaine.

La classe FakeCursor est implémentée en singleton et lève une exception si l'on tente de l'instancier une seconde fois.
"""

import pyautogui
import math
import random
import time

class FakeCursor:
    _instance = None

    def __new__(cls):
        if cls._instance is not None:
            raise Exception("FakeCursor instance already exists. Only one instance is allowed.")
        instance = super(FakeCursor, cls).__new__(cls)
        cls._instance = instance
        return instance

    def __init__(self):
        # Initialisation uniquement lors de la première instanciation
        if hasattr(self, "_initialized") and self._initialized:
            return
        # Désactive le mécanisme failsafe de PyAutoGUI (optionnel)
        pyautogui.FAILSAFE = False
        # On récupère la position actuelle de la souris
        self.__current_position = pyautogui.position()
        self._initialized = True

    def __move_cursor(self, x, y):
        """
        Déplace le curseur réel vers la position (x, y) via PyAutoGUI
        et met à jour la position interne.
        """
        pyautogui.moveTo(x, y)
        self.__current_position = (x, y)

    def __ease_out_back(self, t, overshoot=1.70158):
        """
        Fonction d'easing easeOutBack qui produit un léger dépassement avant de se stabiliser.
        
        :param t: Paramètre de temps (entre 0 et 1)
        :param overshoot: Paramètre d'overshoot
        :return: Valeur ajustée de t
        """
        c1 = overshoot
        c3 = c1 + 1
        return 1 + c3 * ((t - 1) ** 3) + c1 * ((t - 1) ** 2)

    def __quadratic_bezier(self, p0, p1, p2, t):
        """
        Calcule le point sur une courbe de Bézier quadratique pour un paramètre t.
        
        :param p0: Point de départ (tuple x, y)
        :param p1: Point de contrôle (tuple x, y)
        :param p2: Point d'arrivée (tuple x, y)
        :param t: Paramètre de la courbe (entre 0 et 1)
        :return: Tuple (x, y) du point calculé
        """
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        return (x, y)

    def move_random(self, start=None, end=None):
        """
        Simule un mouvement de souris naturel entre deux positions.
        
        Utilise :
        - Une courbe de Bézier quadratique pour lisser la trajectoire.
        - La fonction d'easing easeOutBack pour générer un léger dépassement.
        - Un jitter dégressif pour imiter l'imprécision humaine.
        
        :param start: Tuple (x, y) de la position de départ. Par défaut, la position actuelle.
        :param end: Tuple (x, y) de la position d'arrivée. Doit être spécifié.
        """
        if start is None:
            start = self.__current_position  # Utiliser la position actuelle si aucun point de départ n'est fourni

        if end is None:
            raise ValueError("L'argument 'end' est requis pour déplacer le curseur.")

        steps = random.randint(55, 65)
        base_delay = random.uniform(0.010, 0.015)

        x1, y1 = start
        x2, y2 = end

        mid = ((x1 + x2) / 2, (y1 + y2) / 2)
        dx = x2 - x1
        dy = y2 - y1
        distance = math.hypot(dx, dy)

        if distance != 0:
            perp = (-dy / distance, dx / distance)
        else:
            perp = (0, 0)

        offset = distance * random.uniform(0.01, 0.75)
        if random.choice([True, False]):
            offset = -offset

        control = (mid[0] + perp[0] * offset, mid[1] + perp[1] * offset)
        overshoot = random.uniform(0.2, 0.4)

        for i in range(1, steps + 1):
            t_param = i / steps
            eased_t = self.__ease_out_back(t_param, overshoot=overshoot)
            bx, by = self.__quadratic_bezier(start, control, end, eased_t)
            jitter_amplitude = random.uniform(0.5, 2) * math.sin(math.pi * t_param)
            bx += random.uniform(-jitter_amplitude, jitter_amplitude)
            by += random.uniform(-jitter_amplitude, jitter_amplitude)
            self.__move_cursor(bx, by)
            time.sleep(base_delay * random.uniform(0.9, 1.1))

    def click(self):
        """
        Simule un clic de souris réel en effectuant successivement un mouseDown puis un mouseUp.
        Un délai court est ajouté entre les deux actions pour imiter un clic humain.
        """
        if self.__current_position is None:
            raise Exception("Position inconnue pour cliquer. Déplacez d'abord le curseur.")
        x, y = self.__current_position
        # Déplacement explicite (facultatif) pour s'assurer que la souris est bien à la bonne position
        pyautogui.moveTo(x, y)
        pyautogui.mouseDown()
        time.sleep(random.uniform(0.05, 0.1))
        pyautogui.mouseUp()
