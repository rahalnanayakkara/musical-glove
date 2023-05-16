import music21 
import numpy as np
import threading
import time
import serial
import xml.etree.ElementTree as ET
from playsound import playsound 


def get_right_hand_notes(note_list):
    right_list = []
    for note in note_list:
        if (note.findall('staff')[0]).text=='1' and len(note.findall('rest'))==0:
            right_list.append(note)
    return right_list


def get_left_hand_notes(note_list):
    left_list = []
    for note in note_list:
        if (note.findall('staff')[0]).text=='2' and len(note.findall('rest'))==0:
            left_list.append(note)
    return left_list


def get_finger_list(filename):
    mytree = ET.parse(filename)
    myroot = mytree.getroot()

    measure_list = 0
    for child in myroot:
        if child.tag=='part':
            measure_list = child
            break

    right_finger_list = []

    for measure_number in range(len(measure_list)):
        measure = measure_list[measure_number]

        all_note_list = measure.findall('note')
        rh_note_list = get_right_hand_notes(all_note_list)
        
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
            right_finger_list = right_finger_list + measure_finger_list

    left_finger_list = []

    for measure_number in range(len(measure_list)):
        measure = measure_list[measure_number]

        all_note_list = measure.findall('note')
        lh_note_list = get_left_hand_notes(all_note_list)
        
        measure_finger_list = []
        chord_finger_list = []

        for i in range(len(lh_note_list)):
            note = lh_note_list[i]
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
            left_finger_list = left_finger_list + measure_finger_list

    return right_finger_list, left_finger_list


arduino = serial.Serial(port='COM7', baudrate=115200, timeout=.1)

time.sleep(5)

xmlpath = 'Piano Fingering.musicxml'
score = music21.converter.parse(xmlpath)

finger_number, left_finger_number = get_finger_list(xmlpath)

left_hand = score.parts[1]

l_note_duration = []    # Duration attribute
l_measure_offest = []   # 
l_notes_offest = []
for i in range(1,len(left_hand[:])):
  l_measure = left_hand.measure(i)
  l_measure_offest.append( float(l_measure.offset) )
  for notes in l_measure.flat.notes:
    l_note_duration.append(  float(str(notes.duration).split()[1].split('>')[0])  )
    l_notes_offest.append( float(notes.offset)+float(l_measure.offset) )
    
l_Total_counts = int( max(l_measure_offest)*len(l_measure_offest) / (len(l_measure_offest)-1)/min(l_note_duration) )
left_hand_counts = np.zeros((5,l_Total_counts), dtype=np.int8)
l_note_offset_counts = np.round(np.array(l_notes_offest)/min(l_note_duration)).astype(int)
l_note_duration_counts = np.round(np.array(l_note_duration)/min(l_note_duration)).astype(int)

for i in range(len(l_note_offset_counts)):
  for j in left_finger_number[i]:
        left_hand_counts[int(j)-1, l_note_offset_counts[i] : l_note_offset_counts[i]+l_note_duration_counts[i] ] = 1

right_hand = score.parts[0]

note_duration = []    # Duration attribute
measure_offest = []   # 
notes_offest = []
for i in range(1,len(right_hand[:])):
  measure = right_hand.measure(i)
  measure_offest.append( float(measure.offset) )
  for notes in measure.flat.notes:
    note_duration.append(  float(str(notes.duration).split()[1].split('>')[0])  )
    notes_offest.append( float(notes.offset)+float(measure.offset) )
    
Total_counts = int( max(measure_offest)*len(measure_offest) / (len(measure_offest)-1)/min(note_duration) )
right_hand_counts = np.zeros((5,Total_counts), dtype=np.int8)
note_offset_counts = np.round(np.array(notes_offest)/min(note_duration)).astype(int)
note_duration_counts = np.round(np.array(note_duration)/min(note_duration)).astype(int)

for i in range(len(note_offset_counts)):
  for j in finger_number[i]:
        right_hand_counts[int(j)-1, note_offset_counts[i] : note_offset_counts[i]+note_duration_counts[i] ] = 1

print_arr = []
for i in range(Total_counts):
    print_arr.append(bytearray(list(right_hand_counts[:,i])+list(left_hand_counts[:,i])))

tempo_markings = score.flat.getElementsByClass(music21.tempo.TempoIndication)

# Get the BPM from the first tempo marking (if present)
if len(tempo_markings) > 0:
    bpm = tempo_markings[0].getQuarterBPM()
    # print("BPM = ",bpm)

time_per_beat = 60/bpm
# print("time per beat = ",time_per_beat)
time_per_shortest_note = time_per_beat*min(note_duration)
# print("time per shortest note = ",time_per_shortest_note)

def play_midi():
    """Thread worker function"""
    # print('Worker thread 1 started')
    playsound("out.mp3")
    # print('Worker thread 1 finished')

def serial_out():
    """Thread worker function"""
    # print('Worker thread 2 started')
    for i in range(Total_counts):
        arduino.write(print_arr[i])
        time.sleep(time_per_shortest_note)
    arduino.write(bytearray([0,0,0,0,0,0,0,0,0,0]))
    # print('Worker thread 2 finished') 

# Create a new thread
thread1 = threading.Thread(target=play_midi)
thread2 = threading.Thread(target=serial_out)

# Start the thread
thread1.start()
thread2.start()

# Wait for the thread to finish
thread1.join()
thread2.join()

# print('Main thread finished')