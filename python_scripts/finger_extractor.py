import xml.etree.ElementTree as ET

def get_right_hand_notes(note_list):
    right_list = []
    for note in note_list:
        if (note.findall('staff')[0]).text=='1' and len(note.findall('rest'))==0:
            right_list.append(note)
    return right_list


def get_unique_notes(note_list):
    count1 = 0
    count2 = 0

    count1 = len(note_list)

    for note in note_list:
        if len(note.findall('chord'))>0:
            count2+=1

    unique_notes = count1 - count2
    return unique_notes

def get_finger_list(filename):
    mytree = ET.parse(filename)
    myroot = mytree.getroot()

    measure_list = 0
    for child in myroot:
        if child.tag=='part':
            measure_list = child
            break

    N_measures = len(measure_list)

    # print(f'Score contains {N_measures} Measures \n')

    finger_list = []

    for measure_number in range(len(measure_list)):
        measure = measure_list[measure_number]

        all_note_list = measure.findall('note')
        rh_note_list = get_right_hand_notes(all_note_list)

        n_unique_notes = get_unique_notes(rh_note_list)
        
        measure_finger_list = []
        chord_finger_list = []

        for i in range(len(rh_note_list)):
            note = rh_note_list[i]
            if len(note.findall('chord'))>0:
                chord_finger_list.append(note.findall('notations')[0].findall('technical')[0].findall('fingering')[0].text)
            else:
                if i>0:
                    measure_finger_list.append(chord_finger_list)
                chord_finger_list = []
                chord_finger_list.append(note.findall('notations')[0].findall('technical')[0].findall('fingering')[0].text)

        if len(chord_finger_list)>0:
            measure_finger_list.append(chord_finger_list)
        
        if len(measure_finger_list)>0:
            finger_list = finger_list + measure_finger_list

    return finger_list


print(get_finger_list("Piano Fingering.musicxml"))