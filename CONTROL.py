from time import sleep

class motorCONTROL:

    def __init__(self, q, notes_array):
        self.q = q
        self.notes_array = notes_array
        self.state = False
        self.init_control()

    def hit(self):
        # Commands for the servo motor to hit and pull back
        print('Hiting drum...')
        sleep(0.5)
        print('Hit performed.')


    def change_pitch(self, note = None):
        return self.hit()


    def init_control(self):

        # Initialize variables for mantaining CONTROL's triggers
        self.state = True
        print('motorCONTROL current state: ' + str(self.state))

        while self.state:
            data = self.q.get()
            if data == 'hit':
                self.hit()
            if data == 'changeState':
                self.state = False
            self.q.task_done()

        print('motorCONTROL current state: ' + str(self.state))

    '''
    Here we'll write the command functions for motor impulse input and output.
    Motor should be running only when called by a particular input state,
    and in order to control the function we'll execute it on a loop that
    checks if the state of the note is within a particular GUI range, which will
    launch a state change on the Object, and when the function to check the state
    is triggered, a motor inpulse will be sent to interpret a physical reaction.
    '''


    # for notes in self.notes_array:
            #     note = notes.split(" ")
            #     nPitch = note[0]
            #     duration = 1/int(note[1])
            #     print('[Note: ' + nPitch + ", Duration: " + str(duration) + ']')
            #     sleep(duration*4.3)
            # self.state = False