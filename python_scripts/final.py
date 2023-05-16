import music21 
import numpy as np
import threading
import time

from playsound import playsound 

import serial

arduino = serial.Serial(port='COM7', baudrate=115200, timeout=.1)

time.sleep(5)

def write_data(x):
    arduino.write(bytearray(x))

score = music21.converter.parse('Piano Fingering.musicxml')

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

right_hand = score.parts[0]
print(score.parts[0])

finger_number = []    # Finger Index (which finger)
note_duration = []    # Duration attribute
measure_offest = []   # 
notes_offest = []
for i in range(1,len(right_hand[:])):
  measure = right_hand.measure(i)
  print(measure)
  measure_offest.append( float(measure.offset) )
  for notes in measure.flat.notes:
    print(notes.articulations,   notes.duration,  measure.offset, notes.offset)#, notes.seconds)
    finger_number.append(  int(str(notes.articulations[0]).split()[1].split('>')[0]) )
    note_duration.append(  float(str(notes.duration).split()[1].split('>')[0])  )
    notes_offest.append( float(notes.offset)+float(measure.offset) )
    
Total_counts = int( max(measure_offest)*len(measure_offest) / (len(measure_offest)-1)/min(note_duration) )
right_hand_counts = np.zeros((5,Total_counts), dtype=np.int8)
note_offset_counts = np.round(np.array(notes_offest)/min(note_duration)).astype(int)
note_duration_counts = np.round(np.array(note_duration)/min(note_duration)).astype(int)

for i in range(len(note_offset_counts)):
  if finger_number[i] == 1:   
    right_hand_counts[0, note_offset_counts[i] : note_offset_counts[i]+note_duration_counts[i] ] = 1 #for finger number 1
  elif finger_number[i] == 2:
    right_hand_counts[1, note_offset_counts[i] : note_offset_counts[i]+note_duration_counts[i] ] = 1 #for finger number 2
  elif finger_number[i] == 3:
    right_hand_counts[2, note_offset_counts[i] : note_offset_counts[i]+note_duration_counts[i] ] = 1 #for finger number 3
  elif finger_number[i] == 4:
    right_hand_counts[3, note_offset_counts[i] : note_offset_counts[i]+note_duration_counts[i] ] = 1 #for finger number 3
  elif finger_number[i] == 5:
    right_hand_counts[4, note_offset_counts[i] : note_offset_counts[i]+note_duration_counts[i] ] = 1 #for finger number 3
  else:
    print("6 fingers are not supported")

tempo_markings = score.flat.getElementsByClass(music21.tempo.TempoIndication)

# Get the BPM from the first tempo marking (if present)
if len(tempo_markings) > 0:
    bpm = tempo_markings[0].getQuarterBPM()
    print("BPM = ",bpm)

time_per_beat = 60/bpm
print("time per beat = ",time_per_beat)
time_per_shortest_note = time_per_beat*min(note_duration)
print("time per shortest note = ",time_per_shortest_note)

def play_midi():
    """Thread worker function"""
    print('Worker thread 1 started')
    
    # display(Audio(out_wav, autoplay=True, rate=44100))
    playsound("out.mp3")
    print('Worker thread 1 finished')

def serial_out():
    """Thread worker function"""
    print('Worker thread 2 started')
    # time.sleep(7)
    for i in range(Total_counts):
      # print(bytearray(list(right_hand_counts[:,i])))
      write_data(list(right_hand_counts[:,i]))
      time.sleep(time_per_shortest_note)
    # end_time = time.monotonic()  
    # print(end_time-start_time)
    write_data([0,0,0,0,0])
    print('Worker thread 2 finished') 

# Create a new thread
thread1 = threading.Thread(target=play_midi)
thread2 = threading.Thread(target=serial_out)

# Start the thread
thread1.start()
thread2.start()

# Wait for the thread to finish
thread1.join()
thread2.join()

print('Main thread finished')