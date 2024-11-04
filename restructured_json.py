# import requests
# import json
# import time

# # Set the base URL and headers for the requests
# base_url = "https://api-bc.batiactu.com/api/bcdf/"
# headers = {
#     'Accept': 'application/json, text/plain, */*',
#   'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjdjMTNhZmZlM2Q2ODFkMjgxYjdiYzg4MWUxZTY5MDZmOWQ3N2QzMzMwYTU1ZmY1MDJhNGJhODhjZjc0MzVhNjY4ZTRjOGEyOTAwZjQ0MTI0In0.eyJhdWQiOiIxMCIsImp0aSI6IjdjMTNhZmZlM2Q2ODFkMjgxYjdiYzg4MWUxZTY5MDZmOWQ3N2QzMzMwYTU1ZmY1MDJhNGJhODhjZjc0MzVhNjY4ZTRjOGEyOTAwZjQ0MTI0IiwiaWF0IjoxNzMwMjM1NTU5LCJuYmYiOjE3MzAyMzU1NTksImV4cCI6MTczMTk2MzU1OSwic3ViIjoiMTI5NzUiLCJzY29wZXMiOltdfQ.MNnAF7LeA-1jX4nGzbcCDvQllsW2HMb8REyVyx4Qt3UCfkcqAIdoAORMUyh-ePZHiMDonuZGqKRAhkPgtDiu7zJospCCIktwkLt0bP7FrTuZrOQNr-xdRRl4lwmbf71PWH0u1i1EouOgui0OHvgPMBBvM8gHpvE5kvjccBXeOrLUtveYpzl9VYWMNfoZzF8mt0vpwo29OM1NikV8-DKZyHrf9xbeIq3zRlKY_e-v_XwS8lRaYqm7EM6USJv1B1weyHJZ1sLr4W_92-fMGbXmGn7c3sXWoDg1l9-KrdmtRiacj87OntX1ReHIRItkMXJL9qaxq4Q0NPtVYdkXcretkhumg9THPiyrc1oepyE0-5y_JYaCM13yT9lTKdyHSYu_j4q_NappoJk7PIgC0rFF2ce4VALyloAB68wZDbwg9lobqEsGQ6ZlK3R23Hvu9wax41_Vgz2PF3ibChoznZ4-xC8cZEbFr31Iq8FGQT48DxendPgIkCmcEqrpyV_zWlp-0Tb-NvdSNcLpU9jCNieeVQ5dWIAC7W_F_ox0wLYZBElZa5cwKoUva7AjMn3yRaCUXnIg42e9W_tWQkAtpDE3AVq7wj3k2kzFq2LO9FXHooNtb5XYwUH49WKRW9bSWVz3TU2BSPT4YykMtAyQkCnlx9kpr_xUSiTBy2ZySEfTMpY',    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
#     'Content-Type': 'application/json',
# }

# payload = json.dumps({
#     "thm": "15.8400000000",
#     "coefChMO": 2,
#     "coefFGMO": 1.57,
#     "coefRegion": "1.0000000000",
#     "marge": "15.0000000000",
#     "marge_mo": "15.0000000000",
#     "marge_four": "15.0000000000",
#     "coefFGF": "1.0500000000",
#     "coefDifficulte": "1.0000000000",
#     "coefRemise": "1.0000000000",
#     "coef1": "1.0000000000",
#     "mov": "58.5148235294"
# })

# # Recursive function to fetch categories and subcategories
# def fetch_categories(category_id=None, retries=3, delay=1):
#     url = "https://api-bc.batiactu.com/api/bcdf/getFamilleRacine" if category_id is None else f"https://api-bc.batiactu.com/api/bcdf/getFamille/{category_id}"

#     for attempt in range(retries):
#         try:
#             response = requests.get(url, headers=headers)
#             response.raise_for_status()
#             categories_data = response.json()

#             # Access the list of categories from the 'liste' key
#             categories = categories_data.get('liste')
            
#             if not isinstance(categories, list):
#                 print("No further subcategories. Fetching final data for ID:", category_id)
#                 return fetch_final_data(category_id)  # Call final POST request when no subcategories

#             break  # Exit the retry loop if the request is successful
#         except requests.exceptions.RequestException as e:
#             if response.status_code == 429:
#                 print(f"Rate limit exceeded for ID {category_id}. Retrying in {delay} seconds...")
#                 time.sleep(delay)  # Wait before retrying
#                 delay *= 2  # Exponential backoff
#             else:
#                 print(f"Failed to fetch categories for ID {category_id}: {e}")
#                 return None

#     else:
#         print(f"Max retries exceeded for ID {category_id}.")
#         return None

#     # For each category, fetch its subcategories recursively
#     for category in categories:
#         if isinstance(category, dict):  # Ensure each item is a dictionary
#             subcategory_id = category.get('id')
#             print(f"Fetching subcategories for category ID: {subcategory_id}")
#             subcategories = fetch_categories(subcategory_id)
            
#             if subcategories is not None:
#                 category['subcategories'] = subcategories  # Add subcategories to the category data
#         else:
#             print(f"Unexpected item format: {category} (not a dictionary)")

#     return categories

# # Function to perform the final POST request
# def fetch_final_data(category_id):
#     if category_id is None:
#         print("No valid category ID for final data.")
#         return None

#     url = f"https://api-bc.batiactu.com/api/bcdf/getOuvrages/{category_id}"

#     try:
#         response = requests.post(url, headers=headers, data=payload)
#         response.raise_for_status()
#         final_data = response.json()
#         print(f"Final data fetched for category ID {category_id}")
#         return {"final_data": final_data}  # Embed final data in a dictionary for better structure
#     except requests.exceptions.RequestException as e:
#         print(f"Failed to fetch final data for category ID {category_id}: {e}")
#         return None

# # Main function to start the data collection and save to JSON
# def main():
#     print("Starting data collection...")
#     data = fetch_categories()

#     # Save data to JSON file if collection was successful
#     if data:
#         with open('api_data.json', 'w', encoding='utf-8') as f:
#             json.dump(data, f, ensure_ascii=False, indent=4)
#         print("Data collection complete. Saved to 'api_data.json'.")
#     else:
#         print("Data collection failed or returned no data.")

# if __name__ == "__main__":
#     main()

#all_items_69486
#restructured_data



import json

# Charger le JSON original
with open("all_items_69486_comp.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Créer un dictionnaire pour stocker chaque catégorie par son ID
categories = {}
for entry in data:
    categories[entry["category_id"]] = entry

# Suivi des catégories déjà intégrées pour éviter les doublons
processed_categories = set()

# Fonction pour créer la structure hiérarchique avec informations des parents
def build_hierarchy(category_id, parent_id=None, parent_libelle=None):
    if category_id in processed_categories:
        return None  # Évite les doublons

    category = categories.get(category_id, {}).copy()  # Récupère la catégorie actuelle
    processed_categories.add(category_id)  # Marque cette catégorie comme traitée

    # Ajouter les informations du parent directement au niveau de la catégorie
    if parent_id is not None:
        category["id_parent"] = parent_id
    if parent_libelle is not None:
        category["libelle_parent"] = parent_libelle

    # Si c'est un niveau final, retourner la catégorie
    if "final_data" in category:
        return category

    # Si ce n'est pas un niveau final, traiter les sous-catégories
    children = []
    if "data" in category and "liste" in category["data"]:
        for sub in category["data"]["liste"]:
            sub_id = sub.get("id")
            if sub_id in categories:
                # Passer l'ID et le libellé actuels comme parent pour les sous-catégories
                child = build_hierarchy(sub_id, category_id, sub.get("libelle"))
                if child:
                    children.append(child)

    # Mise à jour de la structure de données pour inclure les enfants hiérarchisés
    category["children"] = children
    category.pop("data", None)  # Supprimer "data" car "children" le remplace
    return category

# Localiser le(s) niveau(x) supérieur(s) qui n'ont pas de parent dans les données
top_level_categories = [
    build_hierarchy(category_id) for category_id, entry in categories.items()
    if "id_parent" not in entry or entry["id_parent"] not in categories
]

# Filtrer les éléments None (résultat des doublons évités) de la hiérarchie finale
top_level_categories = [item for item in top_level_categories if item]

# Sauvegarder le JSON restructuré dans un fichier
with open("restructured_data_test.json", "w", encoding="utf-8") as f:
    json.dump(top_level_categories, f, ensure_ascii=False, indent=4)

print("JSON restructuré enregistré dans 'restructured_data.json'")
