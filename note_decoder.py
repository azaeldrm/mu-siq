def note_decoder(note, counter, pentagram):

    xpos = pentagram['start_X']
    ypos = pentagram['start_Y']
    xspace = pentagram['space_X']
    yspace = pentagram['space_Y']

    location_error = -round(yspace/2)
    note_error = {
        '4': 0,
        '2': -2,
        '1': -location_error * 3
    }

    position = {
        'pitch': note[0][0],
        'X': 0,
        'Y': 0,
        'duration': None
    }

    note_to_pentagram = {
        'c3': 'L0',
        'd3': 'S0',
        'e3': 'L1',
        'f3': 'S1',
        'g3': 'L2',
        'a3': 'S2',
        'b3': 'L3',
        'c4': 'S3',
        'd4': 'L4',
        'e4': 'S4',
        'f4': 'L5',
        'g4': 'S5',
        'a4': 'L6',
        'b4': 'S6',
        'c5': 'L7',
        'd5': 'S7'
    }

    pentagram_to_pos = {
        'S7': ypos - 3*yspace,
        'L7': ypos - 2*yspace - round(yspace/2),
        'S6': ypos - 2*yspace,
        'L6': ypos - 1*yspace - round(yspace/2),
        'S5': ypos - 1*yspace,
        'L5': ypos - round(yspace/2),
        'S4': ypos,
        'L4': ypos + round(yspace/2),
        'S3': ypos + 1*yspace,
        'L3': ypos + 1*yspace + round(yspace/2),
        'S2': ypos + 2*yspace,
        'L2': ypos + 2*yspace + round(yspace/2),
        'S1': ypos + 3*yspace,
        'L1': ypos + 3*yspace + round(yspace/2) ,
        'S0': ypos + 4*yspace,
        'L0': ypos + 4*yspace + round(yspace/2) ,
    }

    # print(note)
    position['X'] = counter*xspace
    note_trigger = position['X']
    position['Y'] = pentagram_to_pos[note_to_pentagram[note[0][0:2]]] + location_error + note_error[note[1]]
    position['duration'] = int(1/(float(note[1])/4))
    counter = counter + position['duration']


    return position, counter, note_trigger





if __name__ == "__main__":

    pentagram = {
        'start_X': 0,
        'start_Y': 100,
        'space_X': 80,
        'space_Y': 20,
        'start_note': 300
    }

    print(note_decoder(['e3', '4', '1'],5,pentagram))
