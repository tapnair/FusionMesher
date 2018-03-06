import adsk.core
import adsk.fusion
import traceback

from .Fusion360Utilities.Fusion360Utilities import AppObjects
from .Fusion360Utilities.Fusion360CommandBase import Fusion360CommandBase


def mesh_brep_interference(mesh_body: adsk.fusion.MeshBody, brep_bodies: adsk.fusion.BRepBodies):

    nodes = mesh_body.mesh.nodeCoordinates

    contained_nodes = []
    boundary_nodes = []

    for brep_body in brep_bodies:
        for node in nodes:
            result = brep_body.pointContainment(node)
            if result == adsk.fusion.PointContainment.PointInsidePointContainment:
                contained_nodes.append(node)
            elif result == adsk.fusion.PointContainment.PointOnPointContainment:
                boundary_nodes.append(node)

    return contained_nodes, boundary_nodes


def draw_points(nodes, image_file, graphics_group):


    vec_coords = []
    for node in nodes:
        vec_coords.extend([node.x, node.y, node.z])

    coordinates = adsk.fusion.CustomGraphicsCoordinates.create(vec_coords)

    cg_points = graphics_group.addPointSet(coordinates, [],
                                           adsk.fusion.CustomGraphicsPointTypes.UserDefinedCustomGraphicsPointType,
                                           image_file)

    return cg_points


# Class for a Fusion 360 Command
# Place your program logic here
# Delete the line that says "pass" for any method you want to use
class MesherInterferenceCommand(Fusion360CommandBase):
    # Run whenever a user makes any change to a value or selection in the addin UI
    # Commands in here will be run through the Fusion processor and changes will be reflected in  Fusion graphics area
    def on_preview(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        pass

    # Run after the command is finished.
    # Can be used to launch another command automatically or do other clean up.
    def on_destroy(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, reason, input_values):
        pass

    # Run when any input is changed.
    # Can be used to check a value and then update the add-in UI accordingly
    def on_input_changed(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, changed_input, input_values):
        pass

    # Run when the user presses OK
    # This is typically where your main program logic would go
    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):

        # Get the values from the user input
        # the_value = input_values['value_input']
        # the_boolean = input_values['bool_input']
        # the_string = input_values['string_input']

        brep_bodies = input_values['brep_input']
        mesh_bodies = input_values['mesh_input']

        # Selections are returned as a list so lets get the first one and its name
        mesh_body = mesh_bodies[0]

        # Get a reference to all relevant application objects in a dictionary
        ao = AppObjects()

        contained_nodes, boundary_nodes = mesh_brep_interference(mesh_body, brep_bodies)

        ao = AppObjects()

        root_comp = ao.root_comp
        graphics_group = root_comp.customGraphicsGroups.add()

        boundary_graphics = draw_points(boundary_nodes, './resources/green_dot.png', graphics_group)
        contained_graphics = draw_points(contained_nodes, './resources/red_dot.png', graphics_group)

        for body in brep_bodies:
            body.opacity = .2
        message = ''
        message += 'Interference Check Results:\n'
        message += '  Nodes Contained in Solids: ' + str(len(contained_nodes)) + '  (Red)\n'
        message += '  Nodes Contained in Boundary: ' + str(len(boundary_nodes)) + '  (Green)'

        ao.ui.messageBox(message)

        for body in brep_bodies:
            body.opacity = 1.0

    # Run when the user selects your command icon from the Fusion 360 UI
    # Typically used to create and display a command dialog box
    # The following is a basic sample of a dialog UI
    def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):

        # Create a default value using a string
        default_value = adsk.core.ValueInput.createByString('1.0 in')
        ao = AppObjects()

        # Create a few inputs in the UI
        # inputs.addValueInput('value_input', '***Sample***Value', ao.units_manager.defaultLengthUnits, default_value)
        # inputs.addBoolValueInput('bool_input', '***Sample***Checked', True)
        # inputs.addStringValueInput('string_input', '***Sample***String Value', 'Default value')
        brep_input = inputs.addSelectionInput('brep_input', 'Select Solid Body(s)', 'Select Something')
        brep_input.addSelectionFilter('SolidBodies')
        brep_input.setSelectionLimits(1, 0)
        mesh_input = inputs.addSelectionInput('mesh_input', 'Select Mesh Body', 'Select Something')
        mesh_input.addSelectionFilter('MeshBodies')
        mesh_input.setSelectionLimits(1, 1)

class MesherClearCommand(Fusion360CommandBase):
    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        ao = AppObjects()

        root_comp = ao.root_comp

        custom_graphics_groups = root_comp.customGraphicsGroups
        for group in custom_graphics_groups:
            group.deleteMe()


class MesherInfoCommand(Fusion360CommandBase):

    def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):

        mesh_input = inputs.addSelectionInput('mesh_input', 'Select Mesh Body', 'Select Something')
        mesh_input.addSelectionFilter('MeshBodies')
        mesh_input.setSelectionLimits(1, 1)

    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        ao = AppObjects()

        mesh_bodies = input_values['mesh_input']
        mesh_body = mesh_bodies[0]
        mesh = adsk.fusion.PolygonMesh.cast(mesh_body.mesh)

        message = 'The selected Mesh Contains:\n'

        message += '  Nodes: ' + str(mesh.nodeCount) + '\n'
        message += '  Triangles: ' + str(mesh.triangleCount) + '\n'
        message += '  Quads: ' + str(mesh.quadCount) + '\n'
        message += '  Polygons: ' + str(mesh.polygonCount) + '\n'

        ao.ui.messageBox(message)