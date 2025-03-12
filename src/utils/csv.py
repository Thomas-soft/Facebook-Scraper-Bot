# Description: Module pour la gestion des fichiers CSV.
# Version: 1.0

import csv
import os
import time
import ast
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def load_scraped_keys(csv_file="posts.csv"):
    """
    Charge depuis le CSV existant les clés (ici : (Auteur, Texte)) des posts déjà scrappés.
    """
    keys = set()
    if os.path.exists(csv_file):
        with open(csv_file, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # On utilise Auteur et Texte pour constituer une clé unique
                key = (row.get("Auteur", "").strip(), row.get("Texte", "").strip())
                keys.add(key)
    return keys


def save_posts_to_csv(posts, csv_file="posts.csv"):
    """
    Sauvegarde la liste des posts dans un fichier CSV.
    Les colonnes sont : Auteur, Texte, Images, Videos, Liens externes, Date, Scrapped at.
    """
    fieldnames = ["Auteur", "Texte", "Images", "Videos", "Liens externes", "Date", "Scrapped at"]
    file_exists = os.path.isfile(csv_file)

    with open(csv_file, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        for post in posts:
            row = {}
            row["Auteur"] = post.get("Auteur", "")
            row["Texte"] = post.get("Texte", "")
            # Pour Images
            images = post.get("Images", "")
            if isinstance(images, list):
                row["Images"] = ", ".join(images)
            else:
                row["Images"] = images
            # Pour Videos : conversion de "Vidéos" vers "Videos"
            videos = post.get("Vidéos", "")
            if isinstance(videos, list):
                row["Videos"] = ", ".join(videos)
            else:
                row["Videos"] = videos
            # Pour Liens externes
            links = post.get("Liens externes", "")
            if isinstance(links, list):
                row["Liens externes"] = ", ".join(links)
            else:
                row["Liens externes"] = links
            row["Date"] = post.get("Date", "")
            row["Scrapped at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow(row)
    print(f"✅ {len(posts)} post(s) sauvegardé(s) dans '{csv_file}'.")
