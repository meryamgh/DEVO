# Mapping entre les types de travaux et les équipements nécessaires
equipements_travaux = {
    "terrassement": ["pelle mécanique", "bulldozer", "camion benne"],
    "construction de fondations": ["bétonnière", "pelleteuse", "vibrateur à béton"],
    "maçonnerie": ["bétonnière", "échafaudage", "grue", "marteau", "scie"],
    "plomberie": ["clé à molette", "soudeuse", "tuyaux", "raccords"],
    "électricité": ["multimètre", "pince coupante", "câbles", "tournevis"],
    "finition intérieure": ["ponceuse", "rouleaux de peinture", "échelle", "perceuse"]
}

# Exemple d'utilisation : récupérer les équipements pour un projet de terrassement
type_de_travail = "terrassement"
equipements_necessaires = equipements_travaux.get(type_de_travail, [])

print(f"Pour le travail de {type_de_travail}, les équipements nécessaires sont : {', '.join(equipements_necessaires)}")



