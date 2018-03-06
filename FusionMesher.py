# Importing sample Fusion Command
# Could import multiple Command definitions here
from .MesherCommand import MesherInterferenceCommand, MesherClearCommand, MesherInfoCommand
from .Demo2Command import Demo2Command
from .DemoPaletteCommand import DemoPaletteShowCommand, DemoPaletteSendCommand

commands = []
command_definitions = []

# Define parameters for 1st command
cmd = {
    'cmd_name': 'Mesh to Brep Interference',
    'cmd_description': 'Calculate if a mesh has nodes within or on the boundary of 1 or more solid bodies',
    'cmd_id': 'cmdID_mesher_interference',
    'cmd_resources': './resources',
    'workspace': 'FusionSolidEnvironment',
    'command_promoted': True,
    'toolbar_panel_id': 'Mesher',
    'class': MesherInterferenceCommand
}
command_definitions.append(cmd)

# Define parameters for 1st command
cmd = {
    'cmd_name': 'Results Clear',
    'cmd_description': 'Deletes Graphics Groups',
    'cmd_id': 'cmdID_mesher_clear',
    'cmd_resources': './resources',
    'workspace': 'FusionSolidEnvironment',
    'toolbar_panel_id': 'Mesher',
    'class': MesherClearCommand
}
command_definitions.append(cmd)

# Define parameters for 1st command
cmd = {
    'cmd_name': 'Mesh Info',
    'cmd_description': 'Basic info about a mesh',
    'cmd_id': 'cmdID_mesher_info',
    'cmd_resources': './resources',
    'workspace': 'FusionSolidEnvironment',
    'toolbar_panel_id': 'Mesher',
    'class': MesherInfoCommand
}
command_definitions.append(cmd)

# # Define parameters for 2nd command
# cmd = {
#     'cmd_name': 'Fusion Demo Command 2',
#     'cmd_description': 'Fusion Demo Command 2 Description',
#     'cmd_id': 'cmdID_demo2',
#     'cmd_resources': './resources',
#     'workspace': 'FusionSolidEnvironment',
#     'toolbar_panel_id': 'SolidScriptsAddinsPanel',
#     'command_visible': True,
#     'command_promoted': True,
#     'class': Demo2Command
# }
# command_definitions.append(cmd)
#
# # Define parameters for 2nd command
# cmd = {
#     'cmd_name': 'Fusion Palette Demo Command',
#     'cmd_description': 'Fusion Demo Palette Description',
#     'cmd_id': 'cmdID_palette_demo',
#     'cmd_resources': './resources',
#     'workspace': 'FusionSolidEnvironment',
#     'toolbar_panel_id': 'SolidScriptsAddinsPanel',
#     'command_visible': True,
#     'command_promoted': False,
#     'palette_id': 'demo_palette_id',
#     'palette_name': 'Demo Palette Name',
#     'palette_html_file_url': 'demo.html',
#     'palette_is_visible': True,
#     'palette_show_close_button': True,
#     'palette_is_resizable': True,
#     'palette_width': 500,
#     'palette_height': 600,
#     'class': DemoPaletteShowCommand
# }
# command_definitions.append(cmd)
#
# # Define parameters for 2nd command
# cmd = {
#     'cmd_name': 'Fusion Palette Send Command',
#     'cmd_description': 'Send info to Fusion 360 Palette',
#     'cmd_id': 'cmdID_palette_send_demo',
#     'cmd_resources': './resources',
#     'workspace': 'FusionSolidEnvironment',
#     'toolbar_panel_id': 'SolidScriptsAddinsPanel',
#     'command_visible': True,
#     'command_promoted': False,
#     'palette_id': 'demo_palette_id',
#     'class': DemoPaletteSendCommand
# }
# command_definitions.append(cmd)

# Set to True to display various useful messages when debugging your app
debug = False

# Don't change anything below here:
for cmd_def in command_definitions:
    command = cmd_def['class'](cmd_def, debug)
    commands.append(command)


def run(context):
    for run_command in commands:
        run_command.on_run()


def stop(context):
    for stop_command in commands:
        stop_command.on_stop()
