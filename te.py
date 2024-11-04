# from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
# from OCC.Core.gp import gp_Pnt
# from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
# from OCC.Core.BOPAlgo import BOPAlgo_Splitter
# from OCC.Display.SimpleGui import init_display
# from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs
# from OCC.Core.StlAPI import StlAPI_Writer

# # Initialize the display
# display, start_display, add_menu, add_function_to_menu = init_display()

# # Dimensions
# board_width = 900  # mm
# board_length = 2400  # mm
# board_thickness = 12.5  # mm, typical thickness for outdoor cement boards

# plenum_height_min = 150  # mm
# plenum_height_max = 240  # mm

# # CD60 Metal Frame Dimensions
# frame_width = 60  # mm
# frame_height = 30  # mm
# frame_spacing = 300  # mm

# # Function to create a box at a given position
# def create_box(x, y, z, dx, dy, dz):
#     return BRepPrimAPI_MakeBox(gp_Pnt(x, y, z), dx, dy, dz).Shape()

# # Create Concrete Slab
# concrete_slab_thickness = 200  # mm, assumed thickness for visualization
# concrete_slab = create_box(-1000, -1000, 0, 5000, 5000, concrete_slab_thickness)

# # Create Metal Frame Grid
# frames = []
# z_frame = concrete_slab_thickness + plenum_height_min  # Starting height for the frame
# for i in range(0, int(board_length / frame_spacing) + 1):
#     frame = create_box(0, i * frame_spacing, z_frame, frame_width, frame_spacing, frame_height)
#     frames.append(frame)

# # Fuse all frames into a single shape
# splitter = BOPAlgo_Splitter()
# splitter.AddArgument(concrete_slab)
# for frame in frames:
#     splitter.AddArgument(frame)
# splitter.Perform()
# fused_frame = splitter.Shape()

# # Add Cement Boards
# cement_boards = []
# y_position = 0
# while y_position < board_length:
#     cement_board = create_box(0, y_position, z_frame + frame_height, board_width, frame_spacing, board_thickness)
#     cement_boards.append(cement_board)
#     y_position += board_length

# # Save fused shape as STEP file
# step_writer = STEPControl_Writer()
# step_writer.Transfer(fused_frame, STEPControl_AsIs)
# step_writer.Write("fused_frame.step")  # Change file path as needed

# # Save fused shape as STL file
# stl_writer = StlAPI_Writer()
# stl_writer.Write(fused_frame, "fused_frame.stl")  # Change file path as needed

# # Display Elements
# display.DisplayShape(fused_frame, update=True)
# for cement_board in cement_boards:
#     display.DisplayShape(cement_board, update=True)

# # Start Display
# start_display()
from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCC.Display.SimpleGui import init_display
from OCC.Core.StlAPI import StlAPI_Writer
from OCC.Core.IGESControl import IGESControl_Writer
from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.Core.Interface import Interface_Static_SetCVal

# Initialisation de l'affichage
display, start_display, add_menu, add_function_to_menu = init_display()

# Dimensions du mur
mur_largeur = 4.0  # Largeur du mur en mètres
mur_hauteur = 3.0  # Hauteur du mur en mètres
mur_epaisseur = 0.45  # Epaisseur moyenne du mur en mètres

# Dimensions de l'ouverture
ouverture_largeur = 1.20  # Largeur de l'ouverture en mètres
ouverture_hauteur = 1.45  # Hauteur de l'ouverture en mètres
ouverture_profondeur = mur_epaisseur  # Profondeur de l'ouverture pour percer tout le mur

# Création du mur
mur = BRepPrimAPI_MakeBox(gp_Pnt(0, 0, 0), mur_largeur, mur_epaisseur, mur_hauteur).Shape()

# Création de l'ouverture (découpe)
ouverture = BRepPrimAPI_MakeBox(
    gp_Pnt((mur_largeur - ouverture_largeur) / 2, 0, 1.0),  # Centrée en X et à 1 mètre de hauteur
    ouverture_largeur,
    ouverture_profondeur,
    ouverture_hauteur
).Shape()

# Découpe de l'ouverture dans le mur
mur_avec_ouverture = BRepAlgoAPI_Cut(mur, ouverture).Shape()
 
base_name = "mur_avec_ouverture"

# Exporter en STL
stl_writer = StlAPI_Writer()
stl_writer.Write(mur_avec_ouverture, f"{base_name}.stl")
print(f"Exporté en STL : {base_name}.stl")

# Exporter en STEP
step_writer = STEPControl_Writer()
Interface_Static_SetCVal("write.step.schema", "AP203")  # Ou AP214 selon votre besoin
step_writer.Transfer(mur_avec_ouverture, STEPControl_AsIs)
step_writer.Write(f"{base_name}.step")
print(f"Exporté en STEP : {base_name}.step")

# Exporter en IGES
iges_writer = IGESControl_Writer()
iges_writer.AddShape(mur_avec_ouverture)
iges_writer.Write(f"{base_name}.iges")
print(f"Exporté en IGES : {base_name}.iges")

# Affichage du résultat
display.DisplayShape(mur_avec_ouverture, update=True)
start_display()
