# Dictionnaire de chemins et phrases correspondantes
chemins_phrases = {
    "fenêtre": {
        "oscillo_battante": {
            "bois": "Vous avez sélectionné une fenêtre oscillo_battantee en bois.",
            "PVC": "Vous avez sélectionné une fenêtre oscillo_battantee en PVC.",
            "aluminium": "Vous avez sélectionné une fenêtre oscillo_battantee en aluminium."
        },
        "coulissante": {
            "bois": "Vous avez sélectionné une fenêtre coulissante en bois.",
            "PVC": "Vous avez sélectionné une fenêtre coulissante en PVC.",
            "aluminium": "Vous avez sélectionné une fenêtre coulissante en aluminium."
        }
    },
    "porte": {
        "battante": {
            "bois": "Vous avez sélectionné une porte battante en bois.",
            "PVC": "Vous avez sélectionné une porte battante en PVC.",
            "acier": "Vous avez sélectionné une porte battante en acier."
        },
        "coulissante": {
            "bois": "Vous avez sélectionné une porte coulissante en bois.",
            "PVC": "Vous avez sélectionné une porte coulissante en PVC.",
            "aluminium": "Vous avez sélectionné une porte coulissante en aluminium."
        }
    }
}

# Fonction pour récupérer la phrase en fonction du chemin sélectionné
def afficher_phrase(type_element, type_ouverture, materiau):
    # Vérification de l'existence du chemin dans le dictionnaire
    phrase = chemins_phrases.get(type_element, {}).get(type_ouverture, {}).get(materiau)
    if phrase:
        print(phrase)
    else:
        print("Chemin non valide ou non trouvé dans la configuration.")

# Exemple d'utilisation
afficher_phrase("fenêtre", "oscillo_battante", "bois")  # Cela affichera la phrase correspondante
