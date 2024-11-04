import FreeCAD
import Part
import Mesh
import MeshPart  # Import MeshPart for mesh conversion

def convert_step_to_stl(input_step, output_stl):
    doc = FreeCAD.newDocument()
    shape = Part.Shape()
    shape.read(input_step)

    # Convert to Mesh
    mesh_obj = doc.addObject("Mesh::Feature", "Mesh")
    mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.1, AngularDeflection=0.1, Relative=False)
    mesh_obj.Mesh = mesh

    # Export to STL
    Mesh.export([mesh_obj], output_stl)
    print(f"Converted {input_step} to {output_stl}")

def convert_step_to_gltf(input_step, output_gltf):
    doc = FreeCAD.newDocument()
    shape = Part.Shape()
    shape.read(input_step)

    # Convert to Mesh
    mesh_obj = doc.addObject("Mesh::Feature", "Mesh")
    mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.1, AngularDeflection=0.1, Relative=False)
    mesh_obj.Mesh = mesh

    # Export to GLTF
    Mesh.export([mesh_obj], output_gltf)
    print(f"Converted {input_step} to {output_gltf}")

# Define paths
input_step = "chair.step"  # Replace with your actual STEP file path
output_stl = "c.stl"   # Replace with your desired STL output path
#output_gltf = "gltfm.gltf" # Replace with your desired GLTF output path

# Uncomment one of the following lines depending on your desired output format:
convert_step_to_stl(input_step, output_stl)
#convert_step_to_gltf(input_step, output_gltf)
