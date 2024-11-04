import os
import FreeCAD
import Part

# Chemin vers le fichier STEP (à modifier selon votre fichier)
input_step_file = "mur.step"  # Remplacez par le chemin de votre fichier STEP
output_stl_file = "mur.stl"   # Remplacez par le chemin de sortie pour le fichier OBJ

# Vérification de l'existence du fichier STEP
if not os.path.exists(input_step_file):
    print("Le fichier STEP spécifié n'existe pas.")
    exit()

# Charger le fichier STEP dans FreeCAD
doc = FreeCAD.newDocument("conversion")
shape = Part.Shape()
shape.read(input_step_file)
part_obj = doc.addObject("Part::Feature", "MyShape")
part_obj.Shape = shape

# Exporter en STL
try:
    Part.export([part_obj], output_stl_file)
    print(f"Fichier exporté en STL : {output_stl_file}")
except Exception as e:
    print(f"Erreur lors de l'exportation en STL : {e}")

# Fermer le document FreeCAD
FreeCAD.closeDocument(doc.Name)