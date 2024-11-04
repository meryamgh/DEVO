import trimesh

import trimesh

# Charger le fichier STL
mesh = trimesh.load("C:/Users/merya/Desktop/DEVO/devisto3D/mur.stl")

# Sauvegarder en OBJ
mesh.export("C:/Users/merya/Desktop/DEVO/devisto3D/mur.obj")
print("Conversion en OBJ terminée !")
