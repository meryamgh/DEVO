import FreeCAD
import Import
import Mesh
import sys
import os

def convert_step_to_obj(step_filename, obj_filename):
    # Vérifier si le fichier STEP existe
    if not os.path.isfile(step_filename):
        print(f"Erreur : le fichier STEP '{step_filename}' n'existe pas.")
        return
    
    # Charger le fichier STEP dans un document FreeCAD
    Import.open(step_filename)
    doc = FreeCAD.ActiveDocument
    
    # Vérifier si le document contient des objets
    if doc is None or len(doc.Objects) == 0:
        print("Erreur : le fichier STEP n'a pas été chargé ou est vide.")
        return

    # Convertir chaque objet STEP en OBJ
    Mesh.export(doc.Objects, obj_filename)
    print(f"Fichier OBJ sauvegardé sous {obj_filename}")

# Vérifier les arguments en ligne de commande
if len(sys.argv) >= 3:
    step_filename = sys.argv[1]
    obj_filename = sys.argv[2]
    convert_step_to_obj(step_filename, obj_filename)
else:
    print("Utilisation : freecadcmd obj.py <fichier.step> <fichier.obj>")
