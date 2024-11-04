import requests
import json
import time
import os

# Set the base URL and headers for the requests
base_url = "https://api-bc.batiactu.com/api/bcdf/"
headers = {
    'Accept': 'application/json, text/plain, */*',
  'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjdjMTNhZmZlM2Q2ODFkMjgxYjdiYzg4MWUxZTY5MDZmOWQ3N2QzMzMwYTU1ZmY1MDJhNGJhODhjZjc0MzVhNjY4ZTRjOGEyOTAwZjQ0MTI0In0.eyJhdWQiOiIxMCIsImp0aSI6IjdjMTNhZmZlM2Q2ODFkMjgxYjdiYzg4MWUxZTY5MDZmOWQ3N2QzMzMwYTU1ZmY1MDJhNGJhODhjZjc0MzVhNjY4ZTRjOGEyOTAwZjQ0MTI0IiwiaWF0IjoxNzMwMjM1NTU5LCJuYmYiOjE3MzAyMzU1NTksImV4cCI6MTczMTk2MzU1OSwic3ViIjoiMTI5NzUiLCJzY29wZXMiOltdfQ.MNnAF7LeA-1jX4nGzbcCDvQllsW2HMb8REyVyx4Qt3UCfkcqAIdoAORMUyh-ePZHiMDonuZGqKRAhkPgtDiu7zJospCCIktwkLt0bP7FrTuZrOQNr-xdRRl4lwmbf71PWH0u1i1EouOgui0OHvgPMBBvM8gHpvE5kvjccBXeOrLUtveYpzl9VYWMNfoZzF8mt0vpwo29OM1NikV8-DKZyHrf9xbeIq3zRlKY_e-v_XwS8lRaYqm7EM6USJv1B1weyHJZ1sLr4W_92-fMGbXmGn7c3sXWoDg1l9-KrdmtRiacj87OntX1ReHIRItkMXJL9qaxq4Q0NPtVYdkXcretkhumg9THPiyrc1oepyE0-5y_JYaCM13yT9lTKdyHSYu_j4q_NappoJk7PIgC0rFF2ce4VALyloAB68wZDbwg9lobqEsGQ6ZlK3R23Hvu9wax41_Vgz2PF3ibChoznZ4-xC8cZEbFr31Iq8FGQT48DxendPgIkCmcEqrpyV_zWlp-0Tb-NvdSNcLpU9jCNieeVQ5dWIAC7W_F_ox0wLYZBElZa5cwKoUva7AjMn3yRaCUXnIg42e9W_tWQkAtpDE3AVq7wj3k2kzFq2LO9FXHooNtb5XYwUH49WKRW9bSWVz3TU2BSPT4YykMtAyQkCnlx9kpr_xUSiTBy2ZySEfTMpY',    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'Content-Type': 'application/json',
}

payload = json.dumps({
    "thm": "15.8400000000",
    "coefChMO": 2,
    "coefFGMO": 1.57,
    "coefRegion": "1.0000000000",
    "marge": "15.0000000000",
    "marge_mo": "15.0000000000",
    "marge_four": "15.0000000000",
    "coefFGF": "1.0500000000",
    "coefDifficulte": "1.0000000000",
    "coefRemise": "1.0000000000",
    "coef1": "1.0000000000",
    "mov": "58.5148235294"
})


def get_first_data():
    url = "https://api-bc.batiactu.com/api/bcdf/getFamilleRacine" 
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    categories_data = response.json()
    categories = categories_data.get('liste')
    return categories


def get_sub_data(id_parent, json_file, visited_ids=None, retries=150, delay=1):
    if visited_ids is None:
        visited_ids = set()

    if id_parent in visited_ids:
        print(f"ID {id_parent} déjà visité, arrêt de la récursion pour éviter la boucle infinie.")
        return

    visited_ids.add(id_parent)
    url = f"{base_url}getFamille/{id_parent}"

    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            categories_data = response.json()
            categories = categories_data.get('liste')

            if categories == []:
                final_data = get_last_sub_data(id_parent)
                if final_data:
                    save_data_to_json(json_file, final_data)
                return
            save_data_to_json(json_file, {"category_id": id_parent, "data": categories_data})

            for category in categories:
                print(f"Fetching sub-data for ID {category['id']}")
                get_sub_data(category['id'], json_file, visited_ids)

            break
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                print(f"Trop de requêtes. Nouvelle tentative dans {delay} secondes...")
                time.sleep(delay)
                delay *= 2
            else:
                print(f"Échec de la récupération des catégories pour l'ID {id_parent} : {e}")
                return

# Fonction pour obtenir les données finales et sauvegarder chaque fois qu'elles sont récupérées
def get_last_sub_data(id_smallest_parent):
    url = f"{base_url}getOuvrages/{id_smallest_parent}"
    retries, delay = 150, 1

    for attempt in range(retries):
        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()
            final_data = response.json().get('liste')
            print(f"Données finales récupérées pour la catégorie ID {id_smallest_parent}")
            return {"category_id": id_smallest_parent, "final_data": final_data}
        except requests.exceptions.RequestException as e:
            if response.status_code == 429:
                print(f"Trop de requêtes. Nouvelle tentative dans {delay} secondes...")
                time.sleep(delay)
                delay *= 2
            else:
                print(f"Échec de la récupération des données finales pour l'ID {id_smallest_parent} : {e}")
                return None
    print(f"Nombre maximal de tentatives atteint pour l'ID {id_smallest_parent}.")
    return None

# Fonction pour enregistrer chaque entrée finale dans le fichier JSON
def save_data_to_json(json_file, data):
    with open(json_file, 'a', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        f.write(",\n")  # Ajouter une virgule après chaque objet pour garder un format JSON de liste

# Fonction principale pour démarrer la récupération et initialiser le fichier JSON
def main():
    json_file = 'all_items_48659.json'
    
    # Si le fichier n'existe pas, créer une liste JSON vide pour les données
    if not os.path.exists(json_file):
        with open(json_file, 'w', encoding='utf-8') as f:
            f.write("[\n")
    
   # parents = get_first_data()
  #  print(parents)
    parents = [48646,48629,141175,48659]
   # for parent in parents :
    #    get_sub_data(parent, json_file)
    # for parent in parents:
    #     get_sub_data(parent['id'], json_file)
    get_sub_data(48659,json_file)
    with open(json_file, 'a', encoding='utf-8') as f:
        f.write("\n]")  
    print("Données enregistrées avec succès dans 'all_items_48646.json'")

if __name__ == "__main__":
    main()



# def get_sub_data(id_parent, list_categories,  retries=150, delay=1):
#     url = f"https://api-bc.batiactu.com/api/bcdf/getFamille/{id_parent}"
#     for attempt in range(retries):
#         try:

#             response = requests.get(url, headers=headers)
#             response.raise_for_status()
#             categories_data = response.json()
#             categories = categories_data.get('liste')
#             if categories==[]:
#                 list_categories.extend(get_last_sub_data(id_parent))
#                 return list_categories
#             list_categories.extend(categories)
#             ids = [item['id'] for item in categories]
#             for i in ids:
#                 print(i)
#                 get_sub_data(i, list_categories)
#             break
#         except requests.exceptions.HTTPError as e:
#             if response.status_code == 429:
#                 print(f"Rate limit exceeded. Retrying in {delay} seconds...")
#                 time.sleep(delay) 
#                 delay *= 2  
#             else:
#                 print(f"Failed to fetch categories for ID {id_parent}: {e}")
#                 return None

#     else:
#         print(f"Max retries exceeded for ID {id_parent}.")
#         return None
#     return list_categories
    

# def get_last_sub_data(id_smallest_parent):
#     retries=150
#     delay=1
#     url = f"https://api-bc.batiactu.com/api/bcdf/getOuvrages/{id_smallest_parent}"
    
#     for attempt in range(retries):
#         try:
#             response = requests.post(url, headers=headers, data=payload)
#             response.raise_for_status()
#             final_data = response.json()
#             categories = final_data.get('liste')
#             print(f"Final data fetched for category ID {id_smallest_parent}")
#             return {"final_data": categories}  # Return the fetched data if successful

#         except requests.exceptions.RequestException as e:
#             if response.status_code == 429:
#                 print(f"Rate limit exceeded. Retrying in {delay} seconds...")
#                 time.sleep(delay)  # Wait before retrying
#                 delay *= 2  # Increase delay for exponential backoff
#             else:
#                 print(f"Failed to fetch final data for category ID {id_smallest_parent}: {e}")
#                 return None

#     print(f"Max retries exceeded for category ID {id_smallest_parent}.")
#     return None  # Return None if all retries fail


# def main():
#     all_items = []
#     parents = get_first_data()
#     ids = [item['id'] for item in parents]
#     # for i in ids:
#     #     list_categories = []
#     #     print(i)
#     #     all_items.append(get_sub_data(i, list_categories))
#    # print(get_sub_data(69486,all_items))
#     result = get_sub_data(69486,all_items)
#     if result:
#         with open('all_items_69486.json', 'w', encoding='utf-8') as f:
#             json.dump(result, f, ensure_ascii=False, indent=4)
#         print("Data successfully saved to 'all_items.json'")
#     else:
#         print("Failed to retrieve data.")
#     return ""

# if __name__ == "__main__":
#     main()