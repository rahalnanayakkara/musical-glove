import music21 
import numpy as np
import threading
import time

from playsound import playsound 


score = music21.converter.parse('Piano Fingering.musicxml')
# score.show()

right_hand = score.parts[0]
for part in score.parts:
    print(part)

# for i in range(1,len(right_hand[:])):
#   measure = right_hand.measure(i)
#   for notes in measure.notes:
#     notes.articulations.append(music21.articulations.Fingering(5))

# right_hand = score.parts[0]

# finger_number = []
# note_duration = []
# measure_offest = []
# notes_offest = []
# for i in range(1,len(right_hand[:])):
#   measure = right_hand.measure(i)
#   measure_offest.append( float(measure.offset) )
#   print(f"Measure {i}")
#   for notes in measure.notes:
#     print(notes.articulations)

# score.show()
# score.write('musicxml', 'my_score.xml')

# Total_counts = int( max(measure_offest)*len(measure_offest) / (len(measure_offest)-1)/min(note_duration) )
# right_hand_counts = np.zeros((5,Total_counts), dtype=np.int8)
# note_offset_counts = np.round(np.array(notes_offest)/min(note_duration)).astype(int)
# note_duration_counts = np.round(np.array(note_duration)/min(note_duration)).astype(int)

# for i in range(len(note_offset_counts)):
#   if finger_number[i] == 1:   
#     right_hand_counts[0, note_offset_counts[i] : note_offset_counts[i]+note_duration_counts[i] ] = 1 #for finger number 1
#   elif finger_number[i] == 2:
#     right_hand_counts[1, note_offset_counts[i] : note_offset_counts[i]+note_duration_counts[i] ] = 1 #for finger number 2
#   elif finger_number[i] == 3:
#     right_hand_counts[2, note_offset_counts[i] : note_offset_counts[i]+note_duration_counts[i] ] = 1 #for finger number 3
#   elif finger_number[i] == 4:
#     right_hand_counts[3, note_offset_counts[i] : note_offset_counts[i]+note_duration_counts[i] ] = 1 #for finger number 3
#   elif finger_number[i] == 5:
#     right_hand_counts[4, note_offset_counts[i] : note_offset_counts[i]+note_duration_counts[i] ] = 1 #for finger number 3
#   else:
#     print("6 fingers are not supported")

# tempo_markings = score.flat.getElementsByClass(music21.tempo.TempoIndication)

# # Get the BPM from the first tempo marking (if present)
# if len(tempo_markings) > 0:
#     bpm = tempo_markings[0].getQuarterBPM()
#     print("BPM = ",bpm)

# time_per_beat = 60/bpm
# print("time per beat = ",time_per_beat)
# time_per_shortest_note = time_per_beat*min(note_duration)
# print("time per shortest note = ",time_per_shortest_note)

# def play_midi():
#     """Thread worker function"""
#     print('Worker thread 1 started')
    
#     # display(Audio(out_wav, autoplay=True, rate=44100))
#     playsound("out.mp3")
#     print('Worker thread 1 finished')

# def serial_out():
#     """Thread worker function"""
#     print('Worker thread 2 started')
#     # time.sleep(7)
#     for i in range(Total_counts):
#       # print(bytearray(list(right_hand_counts[:,i])))
#       write_data(list(right_hand_counts[:,i]))
#       time.sleep(time_per_shortest_note)
#     # end_time = time.monotonic()  
#     # print(end_time-start_time)
#     write_data([0,0,0,0,0])
#     print('Worker thread 2 finished') 

# # Create a new thread
# thread1 = threading.Thread(target=play_midi)
# thread2 = threading.Thread(target=serial_out)

# # Start the thread
# thread1.start()
# thread2.start()

# # Wait for the thread to finish
# thread1.join()
# thread2.join()

# print('Main thread finished')