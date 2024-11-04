from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Vec
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.BRep import BRep_Builder
from OCC.Core.TopoDS import TopoDS_Compound
from OCC.Core.StlAPI import StlAPI_Writer
from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.Display.SimpleGui import init_display

# Initialiser l'affichage
display, start_display, add_menu, add_function_to_menu = init_display()

# Paramètres pour la chaise
seat_width = 40    # Largeur du siège
seat_depth = 40    # Profondeur du siège
seat_thickness = 2 # Épaisseur du siège

back_height = 30   # Hauteur du dossier
back_thickness = 2 # Épaisseur du dossier

leg_height = 35    # Hauteur des pieds
leg_thickness = 2  # Épaisseur des pieds

# Créer le siège
seat = BRepPrimAPI_MakeBox(seat_width, seat_depth, seat_thickness).Shape()
seat_translation = gp_Trsf()
seat_translation.SetTranslation(gp_Vec(0, 0, leg_height))
seat_transformed = BRepBuilderAPI_Transform(seat, seat_translation).Shape()
display.DisplayShape(seat_transformed, update=True)

# Créer le dossier de la chaise
backrest = BRepPrimAPI_MakeBox(seat_width, back_thickness, back_height).Shape()
back_translation = gp_Trsf()
back_translation.SetTranslation(gp_Vec(0, seat_depth - back_thickness, leg_height + seat_thickness))
back_transformed = BRepBuilderAPI_Transform(backrest, back_translation).Shape()
display.DisplayShape(back_transformed, update=True)

# Créer les quatre pieds de la chaise
leg1 = BRepPrimAPI_MakeBox(leg_thickness, leg_thickness, leg_height).Shape()
leg2 = BRepPrimAPI_MakeBox(leg_thickness, leg_thickness, leg_height).Shape()
leg3 = BRepPrimAPI_MakeBox(leg_thickness, leg_thickness, leg_height).Shape()
leg4 = BRepPrimAPI_MakeBox(leg_thickness, leg_thickness, leg_height).Shape()

# Positionner chaque pied
leg_positions = [
    gp_Vec(0, 0, 0),
    gp_Vec(seat_width - leg_thickness, 0, 0),
    gp_Vec(0, seat_depth - leg_thickness, 0),
    gp_Vec(seat_width - leg_thickness, seat_depth - leg_thickness, 0),
]

# Créer un compound pour regrouper toutes les pièces de la chaise
compound = TopoDS_Compound()
builder = BRep_Builder()
builder.MakeCompound(compound)

# Transformer et afficher chaque pied
for leg, position in zip([leg1, leg2, leg3, leg4], leg_positions):
    leg_translation = gp_Trsf()
    leg_translation.SetTranslation(position)
    leg_transformed = BRepBuilderAPI_Transform(leg, leg_translation).Shape()
    display.DisplayShape(leg_transformed, update=True)
    builder.Add(compound, leg_transformed)

# Ajouter le siège et le dossier au compound
builder.Add(compound, seat_transformed)
builder.Add(compound, back_transformed)

# Fonction pour exporter en STL
def export_stl(shape, filename="chair.stl"):
    writer = StlAPI_Writer()
    writer.Write(shape, filename)
    print(f"Fichier STL enregistré sous {filename}")

# Fonction pour exporter en STEP
def export_step(shape, filename="chair.step"):
    step_writer = STEPControl_Writer()
    step_writer.Transfer(shape, STEPControl_AsIs)
    step_writer.Write(filename)
    print(f"Fichier STEP enregistré sous {filename}")

# Exporter la chaise en STL et STEP
export_stl(compound, "chair.stl")
export_step(compound, "chair.step")

# Lancer l'affichage
start_display()
