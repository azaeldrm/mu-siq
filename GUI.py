import pygame
from queue import Queue
from time import sleep
from note_decoder import note_decoder
from scanIMG import scan_img
from threading import Thread
from CONTROL import motorCONTROL
from extractMIDI import extractNotes


class GUI:
    def __init__(self):
        self.state = False
        self.font = pygame.font.Font('freesansbold.ttf', 20)

    def quitScreen(self):
        self.state = False


    def init_thread(self,q,func,args=None):
        if args == None:
            q.put(func())
        elif isinstance(args,list):
            q.put(func(*args))
        else:
            q.put(func(args))
        return q.get()


    def motorCommand(self,q,message):
        q.put(message)


    def moveToNewScreen(self,newScreen,args=None):
        self.state = False
        if args == None:
            newScreen()
        elif isinstance(args,list):
            newScreen(*args)
        else:
            newScreen(args)


    def createText(self, text, color):
        textSurface = self.font.render(text,True,color)
        return textSurface, textSurface.get_rect()


    def createButton(self, screen, msg, pos_x, pos_y, length, height, i_color, a_color, action = None, args = None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        global buttonDown

        if pos_x < mouse[0] < pos_x + length and pos_y < mouse[1] < pos_y + height:
            pygame.draw.rect(screen, i_color, (pos_x, pos_y, length, height))
            if click[0] == 1 and not buttonDown and action != None:
                if args == None:
                    action()
                elif isinstance(args,list):
                    action(*args)
                else:
                    action(args)
                buttonDown = True

            elif click[0] == 0:
                buttonDown = False

        else:
            pygame.draw.rect(screen, a_color, (pos_x, pos_y, length, height))

        textSurf, textRect = self.createText(msg,(240,240,240))
        textRect.center = (pos_x+round(length/2),pos_y+round(height/2))
        screen.blit(textSurf, textRect)


class mainGUI(GUI):
    def __init__(self):
        GUI.__init__(self)
        self.init_gui()

    def init_gui(self):
        # Declaring variables
        print('mainGUI initialized.')
        BLACK = (0,0,0)
        WHITE = (240,240,240)
        RED_B = (200,20,20)
        RED_D = (160,0,0)
        sizeX = 800
        sizeY = 500
        buttonX = 160
        buttonY = 80
        scan_button_pos_x = round(sizeX/2)-round(buttonX/2)-200
        scan_button_pos_y = round(sizeY/2)-round(buttonY/2)+120
        quit_button_pos_x = round(sizeX/2)-round(buttonX/2)+200
        quit_button_pos_y = round(sizeY/2)-round(buttonY/2)+120
        screen = pygame.display.set_mode((sizeX, sizeY))
        pygame.display.set_caption("Pentagram GUI")

        # Displaying name of project
        titleSurf, titleRect = self.createText("μ-SIC, the Autonomous Musical Instrument",(0,0,0))
        titleRect.center = (round(sizeX/2),100)

        # The loop will carry on until the user exit the game (e.g. clicks the close button).
        self.state = True

        # The clock will be used to control how fast the screen updates
        clock = pygame.time.Clock()

        # -------- Main Program Loop -----------
        while self.state:
            # Main event loop (main screen)
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    self.state = False  # Flag that we are done so we exit this loop

            # Creating variables
            screen.fill(WHITE)

            # Draw GUI title and pentagram logo
            screen.blit(titleSurf, titleRect)
            for _ in range(5):
                pygame.draw.line(screen, BLACK, [round(sizeX/2)-160,130+(_+1)*10], [round(sizeX/2)+160,130+(_+1)*10], 1)

            # Draw buttons
            self.createButton(screen,"SCAN",scan_button_pos_x,scan_button_pos_y,buttonX,buttonY,RED_B,RED_D,self.moveToNewScreen,scanGUI)
            self.createButton(screen,"QUIT",quit_button_pos_x,quit_button_pos_y,buttonX,buttonY,RED_B,RED_D,self.quitScreen)

            # Refresh the game
            pygame.display.flip()

            # Limit to 60 frames per second
            clock.tick(60)

        # Once we have exited the main program loop we can stop the game engine:
        print('Exiting mainGUI')
        pygame.quit()
        quit()


class scanGUI(GUI):
    def __init__(self):
        GUI.__init__(self)
        self.init_gui()

    def init_gui(self):
        # Declaring variables
        print('scanGUI initialized.')
        BLACK = (0,0,0)
        WHITE = (240,240,240)
        RED_B = (200,20,20)
        RED_D = (160,0,0)
        sizeX = 800
        sizeY = 500
        buttonX = 160
        buttonY = 80
        scan_button_pos_x = round(sizeX/2)-round(buttonX/2)-200
        scan_button_pos_y = round(sizeY/2)-round(buttonY/2)+120
        quit_button_pos_x = round(sizeX/2)-round(buttonX/2)+200
        quit_button_pos_y = round(sizeY/2)-round(buttonY/2)+120
        screen = pygame.display.set_mode((sizeX, sizeY))
        pygame.display.set_caption("Scan GUI")
        camera_dir = './resources/camera/'
        scanned_dir = './resources/scanned/'
        image_dir = 'musicsheet4.jpg'

        # Taking picture and scanning it
        scan_img(image_dir,camera_dir,scanned_dir)
        image = pygame.image.load(scanned_dir + image_dir)
        image = pygame.transform.scale(image, (400, 400))


        # Displaying name of project
        titleSurf, titleRect = self.createText("Scanned results",(0,0,0))
        titleRect.center = (round(sizeX/2),50)

        # The loop will carry on until the user exit the game (e.g. clicks the close button).
        self.state = True

        # The clock will be used to control how fast the screen updates
        clock = pygame.time.Clock()

        # -------- Main Program Loop -----------
        while self.state:
            # Main event loop (main screen)
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    self.state = False  # Flag that we are done so we exit this loop

            # Creating variables
            screen.fill(WHITE)

            # Draw text
            screen.blit(titleSurf, titleRect)
            screen.blit(image, (round(sizeX/2)-round(400/2),100))

            # Define notes_array test array
            # notes_array = [['e3 4 1'], ['d3 4 1'], ['c3 4 1'], ['d3 4 1'], ['e3 4 1'], ['e3 4 1'], ['e3 2 1'], ['d3 4 1'], ['d3 4 1'], ['d3 2 1'], ['e3 4 1'], ['e3 4 1'],
            # ['e3 2 1'], ['e3 4 1'], ['d3 4 1'], ['c3 4 1'], ['d3 4 1'], ['e3 4 1'], ['e3 4 1'], ['e3 2 1'], ['d3 4 1'], ['d3 4 1'], ['e3 4 1'], ['d3 4 1'], ['c3 1 1']]

            # Draw buttons
            # self.createButton(screen,"YES",scan_button_pos_x,scan_button_pos_y,buttonX,buttonY,RED_B,RED_D,self.moveToNewScreen,[musicGUI,[notes_array]])
            self.createButton(screen,"YES",scan_button_pos_x,scan_button_pos_y,buttonX,buttonY,RED_B,RED_D,self.moveToNewScreen,extractGUI)
            self.createButton(screen,"NO",quit_button_pos_x,quit_button_pos_y,buttonX,buttonY,RED_B,RED_D,self.moveToNewScreen,mainGUI)

            # Refresh the game
            pygame.display.flip()

            # Limit to 60 frames per second
            clock.tick(60)

        # Once we have exited the main program loop we can stop the game engine:
        pygame.quit()
        quit()


class extractGUI(GUI, Thread):
    def __init__(self):
        self.state = False
        self.extracted = None
        GUI.__init__(self)
        self.init_gui()


    def init_gui(self):

        print('extractGUI initialized.')
        # Declaring variables
        BLACK = (0,0,0)
        WHITE = (240,240,240)
        RED_B = (200,20,20)
        RED_D = (160,0,0)
        GREEN = (20,200,20)
        sizeX = 800
        sizeY = 500
        buttonX = 160
        buttonY = 80
        loading_bar = 0
        cancel_button_pos_x = round(sizeX/2)-round(buttonX/2)+200
        cancel_button_pos_y = round(sizeY/2)-round(buttonY/2)+120
        continue_button_pos_x = round(sizeX/2)-round(buttonX/2)-200
        continue_button_pos_y = round(sizeY/2)-round(buttonY/2)+120
        screen = pygame.display.set_mode((sizeX, sizeY))
        pygame.display.set_caption("Extracting notes...")
        scanned_dir = './resources/scanned/'
        image_dir = 'mary.png'

        # Displaying name of project
        extractSurf, extractRect = self.createText("Extracting notes...",(0,0,0))
        extractRect.center = (round(sizeX/2),50)
        successSurf, successRect = self.createText("Notes extracted successfully!",(0,0,0))
        successRect.center = (round(sizeX/2),50)
        failSurf, failRect = self.createText("Extraction failed. Press Cancel.",(0,0,0))
        failRect.center = (round(sizeX/2),50)
        


        # The loop will carry on until the user exit the game (e.g. clicks the close button).
        self.state = True

        # Starting note extraction thread
        q = Queue()
        notes_thread = Thread(target=self.init_thread, args=(q,extractNotes,[q, scanned_dir + image_dir]), daemon=True)
        notes_thread.start()

        # The clock will be used to control how fast the screen updates
        clock = pygame.time.Clock()

        # -------- Main Program Loop -----------
        while self.state:
            # Main event loop (main screen)
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    self.state = False  # Flag that we are done so we exit this loop

            # Creating variables
            screen.fill(WHITE)

            # Draw text
            if self.extracted == None:
                screen.blit(extractSurf, extractRect)
            elif self.extracted == True:
                screen.blit(successSurf, successRect)
            elif self.extracted == False:
                screen.blit(failSurf, failRect)

            # Getting information from thread
            if not q.empty():
                print('Queue received information.')
                msg = q.get()
                q.task_done()
                if isinstance(msg,int):
                    loading_bar = msg
                    print(loading_bar)
                elif isinstance(msg,list):
                    notes_array = msg
                    if notes_array == None or len(notes_array) == 0:
                        self.extracted = False
                    else:
                        self.extracted = True
                    print(notes_array)

            # Draw loading bar container
            pygame.draw.rect(screen, BLACK, (round(sizeX/2) - 100, round(sizeY/2) - 40 - 50, 200, 80), 4)

            # Draw buttons and loading bar
            if self.extracted == None:
                pygame.draw.rect(screen, GREEN, (round(sizeX/2) - 90, round(sizeY/2) - 30 - 50, 180*(loading_bar/100), 60))
                loadSurf, loadRect = self.createText(str(loading_bar) + ' %',(0,0,0))
            elif self.extracted == False:
                self.createButton(screen,"CANCEL",cancel_button_pos_x,cancel_button_pos_y,buttonX,buttonY,RED_B,RED_D,self.moveToNewScreen,mainGUI)
                pygame.draw.rect(screen, RED_B, (round(sizeX/2) - 90, round(sizeY/2) - 30 - 50, 180*(loading_bar/100), 60))
                loadSurf, loadRect = self.createText('FAILED',(0,0,0))
            elif self.extracted == True:
                self.createButton(screen,"CANCEL",cancel_button_pos_x,cancel_button_pos_y,buttonX,buttonY,RED_B,RED_D,self.moveToNewScreen,mainGUI)
                self.createButton(screen,"CONTINUE",continue_button_pos_x,continue_button_pos_y,buttonX,buttonY,RED_B,RED_D,self.moveToNewScreen,[musicGUI,[notes_array]])
                pygame.draw.rect(screen, GREEN, (round(sizeX/2) - 90, round(sizeY/2) - 30 - 50, 180*(loading_bar/100), 60))
                loadSurf, loadRect = self.createText(str(loading_bar) + ' %',(0,0,0))

            loadRect.center = (round(sizeX/2),round(sizeY/2) - 50)
            screen.blit(loadSurf, loadRect)

            # Refresh the game
            pygame.display.flip()

            # Limit to 60 frames per second
            clock.tick(60)

        # Once we have exited the main program loop we can stop the game engine:
        print('Exiting extractGUI.')
        pygame.quit()
        quit()


class musicGUI(GUI, motorCONTROL, Thread):

    def __init__(self, notes_array):
        GUI.__init__(self)
        self.notes_array = notes_array
        self.noteActive = []
        self.trigger = 0
        self.isPaused = False
        self.decreasing = 1
        self.init_gui()


    def controlMusic(self):
        if self.isPaused:
            self.decreasing = 1
            self.isPaused = False
        else:
            self.decreasing = 0
            self.isPaused = True


    def init_gui(self):
        # Declaring variables
        print('musicGUI initialized.')
        BLACK = (0,0,0)
        WHITE = (240,240,240)
        RED_B = (200,20,20)
        RED_D = (160,0,0)
        sizeX = 800
        sizeY = 500
        buttonX = 120
        buttonY = 80
        control_button_pos_x = round(sizeX/2)-round(buttonX/2)-200
        control_button_pos_y = round(sizeY/2)-round(buttonY/2)+120
        quit_button_pos_x = round(sizeX/2)-round(buttonX/2)+200
        quit_button_pos_y = round(sizeY/2)-round(buttonY/2)+120
        screen = pygame.display.set_mode((sizeX, sizeY))
        progress = 0
        ratio = 2.5
        BPM = 60 # Adjust this for the speed of the song.
        FPS = 120
        FPM = FPS * 60
        FPB = round(FPM/BPM)
        detector = 300
        all_notes = []
        all_triggers = []
        all_separators = []

        pentagram = {
            'start_X': 0,
            'start_Y': 100,
            'space_X': FPB,
            'space_Y': 8*ratio,
            'start_note': 800
        }

        quarter_note = pygame.image.load('resources/musicnotes/quarter.png')
        quarter_note = pygame.transform.scale(
            quarter_note, (round(pentagram['space_Y'] * ratio), round(pentagram['space_Y'] * ratio)))
        half_note = pygame.image.load('resources/musicnotes/half.png')
        half_note = pygame.transform.scale(
            half_note, (round(pentagram['space_Y'] * ratio), round(pentagram['space_Y'] * ratio)))
        whole_note = pygame.image.load('resources/musicnotes/whole.png')
        whole_note = pygame.transform.scale(
            whole_note, (round(pentagram['space_Y'] * 1.1), round(pentagram['space_Y'] * 1.1)))

        diff_note = {
            1: quarter_note,
            2: half_note,
            4: whole_note
        }

        font = pygame.font.Font('freesansbold.ttf', 20)

        text = {
            'a': font.render('A', True, BLACK),
            'b': font.render('B', True, BLACK),
            'c': font.render('C', True, BLACK),
            'd': font.render('D', True, BLACK),
            'e': font.render('E', True, BLACK),
            'f': font.render('F', True, BLACK),
            'g': font.render('G', True, BLACK)
        }

        textRect = text['a'].get_rect()
        textRect.center = (20, 100)

        pygame.display.set_caption("Pentagram GUI")

        counter = 1

        # Process notes_array
        _notes_array = self.notes_array
        notes_array = []
        for note_bundle in _notes_array:
            for note in note_bundle:
                notes_array.append(note)

        for note in notes_array:
            if (counter - 1) % 4 == 0:
                all_separators.append(counter * pentagram['space_X'] + pentagram['start_X'] - int(pentagram['space_X']/8) + pentagram['start_note'])
            note = note.split(' ')
            note_position, counter, note_trigger = note_decoder(note, counter, pentagram)
            all_triggers.append(note_trigger)
            all_notes.append(note_position)

        trigger = all_triggers.pop(0)

        # Start queue thread to control motor
        q = Queue(maxsize=1)
        motor = Thread(target=self.init_thread, args=(q,motorCONTROL,[q,all_triggers]), daemon=True)
        motor.start()

        # The loop will carry on until the user exit the game (e.g. clicks the close button).
        self.state = True

        # The clock will be used to control how fast the screen updates
        clock = pygame.time.Clock()

        lastnote_trigger = -1*(all_notes[-1]['X'] + sizeX + 100)
        print(lastnote_trigger)

        # -------- Main Program Loop -----------
        while self.state:
            # --- Main event loop
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    self.state = False  # Flag that we are done so we exit this loop

            # Draw background
            screen.fill(WHITE)

            # Draw buttons
            if self.isPaused:
                self.createButton(screen,"RESUME",control_button_pos_x,control_button_pos_y,buttonX,buttonY,RED_B,RED_D,self.controlMusic)
            else:
                self.createButton(screen,"PAUSE",control_button_pos_x,control_button_pos_y,buttonX,buttonY,RED_B,RED_D,self.controlMusic)
            self.createButton(screen,"ABORT",quit_button_pos_x,quit_button_pos_y,buttonX,buttonY,RED_B,RED_D,self.quitScreen)

            # Draw pentagram
            for line in range(5):
                pygame.draw.line(screen, BLACK, [pentagram['start_X'], pentagram['start_Y'] + pentagram['space_Y'] * (line + 1)],
                                [sizeX, pentagram['start_Y'] + pentagram['space_Y'] * (line + 1)], 1)

            # Draw notes
            for note in all_notes:
                screen.blit(
                    diff_note[note['duration']], (note['X'] + pentagram['start_note'] + progress, note['Y']))
                screen.blit(
                    text[note['pitch']], (note['X'] + pentagram['start_note'] + progress + 10, pentagram['start_Y'] + 8 * pentagram['space_Y']))


            # Draw note detector
            pygame.draw.line(screen, BLACK,
                    [detector, pentagram['start_Y'] + pentagram['space_Y']],
                    [detector, pentagram['start_Y'] + pentagram['space_Y'] * 5])


            # Logic for motor command communication (need to add individual notes' awareness of location for command sending)
            progress -= self.decreasing
            trigger_logic = -1*(pentagram['start_note'] + progress) + detector
            if trigger_logic == trigger[0]:
                print('trigger_logic == trigger')
                print(progress)
                self.motorCommand(q,trigger[1])
                print(trigger[1])
                if len(all_triggers) != 0:
                    trigger = all_triggers.pop(0)
                print('Trigger value: ' +  str(trigger[0]))

            if progress < lastnote_trigger:
                print(progress)
                self.state = False

            pygame.display.flip()

            # --- Limit to 60 frames per second
            clock.tick(FPS)

        # Once all notes are performed, go back to main screen.
        print('Exiting mainGUI')
        self.motorCommand(q,'changeState')
        self.moveToNewScreen(mainGUI)
