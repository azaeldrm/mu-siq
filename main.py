import pygame
from GUI import mainGUI

# if __name__ == "__main__":

#     # # Initialize main GUI
#     # MAIN = screenGUI()
#     # MAIN.init_gui()

#     # Extract image file location from command line
#     camera_dir = './resources/camera/'
#     scan_dir = './resources/scanned/'
#     img_name = sys.argv[1:][0]

#     # Process image through warping algorithm to straighten image taken at an angle
#     scan_confirm = scan_img(img_name, scan_dir, camera_dir)

#     if scan_confirm:
        
#         # Execute extractMIDI function to analyze music sheet image and extract an array of notes.
#         # notes_array = extractMIDI(scan_dir+img_name)

#         # Using commented-out nested array for testing purposes.
#         notes_array = [['e3 4 1'], ['d3 4 1'], ['c3 4 1'], ['d3 4 1'], ['e3 4 1'], ['e3 4 1'], ['e3 2 1'], ['d3 4 1'], ['d3 4 1'], ['d3 2 1'], ['e3 4 1'], ['g3 4 1'],
#             ['g3 2 1'], ['e3 4 1'], ['d3 4 1'], ['c3 4 1'], ['d3 4 1'], ['e3 4 1'], ['e3 4 1'], ['e3 2 1'], ['d3 4 1'], ['d3 4 1'], ['e3 4 1'], ['d3 4 1'], ['c3 1 1']]

#         # Initialize GUI and MOTOR objects with the notes displaying and motor awaiting commands
#         MOTOR = motorCONTROL()
#         GUI = musicGUI(notes_array)
        
#         MOTOR.init_control()
#         GUI.init_gui()
        

#         while GUI.state:
#             # Add flow of information between GUI and MOTOR
#             if GUI.trigger == 1:
#                 MOTOR.hit()
#             elif GUI.trigger == -1:
#                 MOTOR.change_pitch(GUI.noteActive)      

#         # Run parallel thread of note display and motor function down below

if __name__ == "__main__":

    pygame.init()
    mainGUI()
    