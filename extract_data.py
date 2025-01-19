import requests
import json
import time
import os


base_url = "https://api-bc.batiactu.com/api/bcdf/"
headers = {
    'Accept': 'application/json, text/plain, */*',
  'Authorization': 'Bearer your_token',    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
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

def save_data_to_json(json_file, data):
    with open(json_file, 'a', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        f.write(",\n")  

# Fonction principale pour démarrer la récupération et initialiser le fichier JSON
def main():
    json_file = 'all_items_48659.json'
    
  
    if not os.path.exists(json_file):
        with open(json_file, 'w', encoding='utf-8') as f:
            f.write("[\n")
    
   # parents = get_first_data()
  #  print(parents)
    parents = [48646,48629,141175,48659]
    get_sub_data(48659,json_file)
    with open(json_file, 'a', encoding='utf-8') as f:
        f.write("\n]")  
    print("Données enregistrées avec succès dans 'all_items_48646.json'")

if __name__ == "__main__":
    main()