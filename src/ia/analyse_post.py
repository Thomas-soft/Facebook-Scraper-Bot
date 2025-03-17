# Description: This file contains the function to analyse a post
# Version: 1.0

import os
import requests
import time
import traceback
import base64
import pyautogui
import platform
import dotenv

# Charger les variables d'environnement à partir du fichier .env
dotenv.load_dotenv()


def is_website_selling(driver, text, images):

    # S'assurer que 'images' est une liste
    if not isinstance(images, list):
        images = []

    # Limites à respecter
    MAX_IMAGES = 5
    MAX_FILE_SIZE = 30 * 1024 * 1024  # 30 MB en octets

    image_b64_list = []
    original_window = driver.current_window_handle
    new_tabs = []
    count = 0

    # Traitement des images (max 5)
    for image_url in images:
        if count >= MAX_IMAGES:
            print("Limite de 5 images atteinte.")
            break
        print(f"\n--- Traitement de l'image {count+1}/{MAX_IMAGES}: {image_url} ---")
        try:
            # Ouvrir un nouvel onglet pour charger l'image
            driver.switch_to.new_window('tab')
            new_tabs.append(driver.current_window_handle)
            driver.get(image_url)
            time.sleep(1)  # Pause pour le chargement de l'image

            try:
                img_elem = driver.find_element("tag name", "img")
                image_data = img_elem.screenshot_as_png
                print("Capture d'écran de l'élément <img> prise.")
            except Exception as e:
                print("Échec de capture d'écran de l'élément <img>, capture complète de l'onglet...")
                image_data = driver.get_screenshot_as_png()

            file_size = len(image_data)
            print(f"Taille de l'image: {file_size / (1024*1024):.2f} MB")
            if file_size > MAX_FILE_SIZE:
                print("Image trop volumineuse (plus de 30MB), ignorée.")
            else:
                image_b64 = base64.b64encode(image_data).decode('utf-8')
                image_b64_list.append(image_b64)
                count += 1
        except Exception as e:
            print(f"Erreur lors du téléchargement de l'image {image_url}: {e}")
            traceback.print_exc()
        # finally:
            # driver.switch_to.window(original_window)

    # Déterminer la touche système pour fermer un onglet
    system_key = "command" if platform.system() == "Darwin" else "ctrl"

    # Fermeture de tous les onglets d'images ouverts en simulant la combinaison key+w
    print("\nFermeture de tous les onglets d'images ouverts...")
    for tab_handle in new_tabs:
        try:
            driver.switch_to.window(tab_handle)
            pyautogui.hotkey(system_key, 'w')
            print(f"Onglet {tab_handle} fermé avec {system_key}+w.")
            time.sleep(0.5)  # Pause pour s'assurer de la fermeture
        except Exception as e:
            print(f"Erreur lors de la fermeture de l'onglet {tab_handle}: {e}")
            traceback.print_exc()
    driver.switch_to.window(original_window)

    # Construction du payload JSON pour LM Studio
    # Ici, le texte est placé dans "content" et, s'il y a au moins une image, la première est envoyée dans le champ "image".
    LM_STUDIO_ENDPOINT = "http://localhost:1234/v1/chat/completions"
    user_message = text  # Contenu textuel uniquement
    print("LE texte est : ", user_message)

    # Construction du message utilisateur avec un champ image si disponible
    message_user = {"role": "user", "content": user_message}
    if image_b64_list:
        message_user["image"] = image_b64_list[0]

    payload = {
        "model": "mathstral-7b-v0.1",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an advanced AI assistant with deep expertise in analyzing textual content to identify whether a post is "
                    "offering (or requesting) the sale or purchase of a website, blog, e-commerce store, domain, or any other form of "
                    "online presence.\n\n"
                    
                    "Your task is to carefully interpret the entire text of the post and determine if it suggests a website sale/purchase—even "
                    "if the language is stylized, abbreviated, or indirectly references a transaction.\n\n"
                    
                    "Here are some guidelines and examples:\n\n"
                    
                    "1. **Contextual Clues Beyond Keywords**\n"
                    "- Do not rely on a simple list of keywords. Instead, look for phrases, hints, or context that imply a transaction.\n"
                    "- Posts may mention monetization (e.g., 'AdSense', 'pin verified', 'income', 'earnings', 'monetized site', 'traffic stats'), "
                    "which can be a strong sign of a website being sold.\n"
                    "- References to 'selling' or 'buying' a domain, 'passing the site to someone', or 'site flipping' should also be considered.\n\n"
                    
                    "2. **Synonyms & Partial Phrases**\n"
                    "- A post might not say 'for sale' directly. It could say 'I’m letting go of my domain', 'AdSense available for sell', "
                    "'looking for a buyer', or 'ready to hand over the site'.\n"
                    "- Phrases like 'WordPress site', 'e-commerce store', 'blog', 'domain', 'hosting', 'pin verified', 'niche', 'traffic', "
                    "'revenue', 'aged domain', or 'established site' might indicate an online property for sale.\n\n"
                    
                    "3. **Sales Channels or Groups**\n"
                    "- If the post comes from a known 'website flipping' or 'domain marketplace' context, even subtle references (e.g., 'DM for price', "
                    "'best offer', 'open to bids', 'ready for takeover') may imply a sale.\n\n"
                    
                    "4. **False Positives**\n"
                    "- If the text only discusses a website or domain but does not imply any intent to sell or buy, it is not considered an offer. "
                    "For example, 'I just launched my blog' or 'Tips to grow AdSense revenue' is not necessarily a sale offer.\n\n"
                    
                    "5. **Required Output**\n"
                    "- If you determine the post **is** offering or requesting the sale/purchase of a website (in any form), respond **only** "
                    "with the following JSON (no explanation):\n"
                    "  {\"result\": true}\n\n"
                    "- If you determine the post is **not** an offer/request to buy or sell a website, respond with the following JSON and provide "
                    "a brief reason:\n"
                    "  {\"result\": false, \"reason\": \"short explanation\"}\n\n"
                    
                    "6. **Use Your Reasoning**\n"
                    "- Go beyond superficial keyword detection. If multiple signals point to a sale (e.g., references to 'selling', 'AdSense account', "
                    "'pin verified', 'WordPress site', 'domain', 'e-commerce', 'inbox for price', 'for sale', 'website flipping', 'monetized site', "
                    "'serious buyers only'), infer that the post is an offer.\n"
                    "- If the text is ambiguous, lean on context clues. For instance, 'WordPress site for sale' or 'Adsense with website for sell' "
                    "should be treated as an offer, even if it’s not perfectly phrased.\n\n"
                    
                    "Remember:\n"
                    "- **If it’s a sale/purchase offer** → {\"result\": true}\n"
                    "- **Otherwise** → {\"result\": false, \"reason\": \"brief explanation\"}\n\n"
                    
                    "Now, read the user's post carefully and decide if it is an offer to buy or sell a website. Then provide your final answer in the "
                    "exact JSON format requested, without additional commentary."
                )
            },
            # Insert your user message here, for example:
            # {"role": "user", "content": "Your post text..."}
        ],
        "temperature": 0.2,
        "max_tokens": 50,
        "stream": False
    }





    headers = {"Content-Type": "application/json"}
    try:
        print("\nEnvoi de la requête POST à LM Studio...")
        response = requests.post(LM_STUDIO_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()
        response_json = response.json()
        assistant_message = response_json["choices"][0]["message"]["content"]
        print("Réponse de l'IA :", assistant_message)
        is_selling = True if assistant_message.lower() == "{\"result\": true}" else False
    except Exception as e:
        print("Erreur lors de l'appel à LM Studio :", e)
        traceback.print_exc()
        is_selling = False

    return is_selling

