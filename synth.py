#!/usr/bin/env python
import random
from midiutil import MIDIFile
import math

def generateDuration (i, n, range = [0,1]):
	return (math.sin(-1 * math.radians(math.pi * i/n)) * range[0]) + (range[1] - range[0])

tempo = random.randint(60,300)

beat_track   = 0
beat_channel = 0
beat_time	= 0	# In beats
beat_pitch	 = 60
beat_tempo   = tempo # In BPM
beat_volume  = 70  # 0-127, as per the MIDI standard

music_track   = 1
music_channel = 1
music_time	= 0	# In beats
music_pitch	 = 60
music_tempo   = tempo # In BPM
music_volume  = 100  # 0-127, as per the MIDI standard

MyMIDI = MIDIFile(2, adjust_origin = False)

MyMIDI.addTempo(beat_track, beat_time, beat_tempo)
MyMIDI.addTempo(music_track, music_time, music_tempo)

# Underlying Beat Generation

beat_degrees = [60, 62, 64, 65, 67, 69, 71, 72]

degree_units = [60, 62, 64, 65, 67, 69, 71, 72, 0]

degrees = []

durations = []

beat_degrees.extend(beat_degrees)

for i in range(random.randint(0,4)):
	beat_degrees.pop(random.randint(0,len(beat_degrees)-1))
	random.shuffle(beat_degrees)

for i in range(len(beat_degrees)):
	durations.append(generateDuration(i, len(beat_degrees), [1,3]))

# npd = No. of Notes per beat duration
npd = random.randint(2, 4) * len(beat_degrees);

for i in range(npd):
	degrees.append(random.choice(degree_units))

# nrep = No. of times to repeat tune
nrep = 1

for i in range(nrep):
	beat_degrees.extend(beat_degrees)
	durations.extend(durations)
	degrees.extend(degrees)

beat_degrees.extend(list(reversed(beat_degrees)))
durations.extend(list(reversed(durations)))
degrees.extend(list(reversed(degrees)))

MyMIDI.addProgramChange(beat_track, beat_channel, beat_time, random.randint(0,128))

# Add Beats Track to MIDIFile Object

t = 0

for i, pitch in enumerate(beat_degrees):
	duration = durations[i % len(durations)]
	MyMIDI.addNote(beat_track, beat_channel, pitch, beat_time + t, durations[i], beat_volume)
	t = t + durations[i]

t = 0

MyMIDI.addProgramChange(music_track, music_channel, music_time, random.randint(0,128))

for i, pitch in enumerate(degrees):
	duration = durations[i % len(durations)] * len(beat_degrees) / len(degrees)
	if(pitch != 0):
		MyMIDI.addNote(music_track, music_channel, pitch, music_time + t, duration, music_volume)
		t = t + duration
	else:
		t = t + duration

duration = 0
for i in range(len(durations)):
	duration = duration + durations[i]

print("No. of main track notes: %d" % len(degrees))
print("No. of beat track notes: %d" % len(beat_degrees))

with open("output.mid", "wb") as outfile:
	MyMIDI.writeFile(outfile)