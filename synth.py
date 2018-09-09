#!/usr/bin/env python

# Metadata
__author__ = "Sagnik Modak"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Sagnik Modak"
__email__ = "sagnikmodak1118@gmail.com"
__status__ = "Prototype"

# Main Code

import random
from midiutil import MIDIFile
import math

# Function to generate a smooth duration difference.
# This is so that the starting notes are gapped farther apart, the notes in the middle are gapped close together
# and the notes towards the end are again gapped further apart. This creates an effect of Rising Tension, Climax
# and finally, Free-falling.

def generateLinearDuration(i, n, range = [0, 1]):
	i = i if (i > n/2) else (n - i)
	return (float(i * (range[1] - range[0])) / n) + range[0]

# Or you can use the traditional constant difference function
# This returns the average of max and min duration
# We mimic the arguments as the above function so they can be
# easily used interchangeably
def generateConstantDuration(i, n, range = [0,1]):
	return range[1]

tempo = random.randint(60,300) # A random tempo between 60 and 300

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

# Basic units of degrees from which to build main track notes

# Note also: 0 means unconditional gaps in notes

degree_units = [60, 62, 64, 65, 67, 69, 71, 72, 0]

degrees = []

durations = []

# Randomly select a duration function

duration_func = random.choice([generateLinearDuration, generateConstantDuration])


beat_degrees.extend(beat_degrees)

for i in range(random.randint(0,4)):
	beat_degrees.pop(random.randint(0,len(beat_degrees)-1))
	random.shuffle(beat_degrees)

for i in range(len(beat_degrees)):
	durations.append(duration_func(i, len(beat_degrees), [1,2]))

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

# Creating macro-symmetry in degrees and durations by making them palindromic

beat_degrees.extend(list(reversed(beat_degrees)))
durations.extend(list(reversed(durations)))
degrees.extend(list(reversed(degrees)))

# MIDI Programs = Instruments. There are also things like Alarm Clock Sounds, Rain sounds, Echoes, etc.
# We want to avoid those. So we make a list of allowed beat track instruments and another for allowed
# Main Track instruments. This also lets us sort instruments correctly for the correct task.

beat_track_instruments = list(range(8, 15)) +  list(range(32, 39)) + list(range(88, 95)) + list(range(112, 119))
main_track_instruments = list(range(7)) + list(range(16, 31)) + list(range(40, 79)) + list(range(104, 111))

# Choosing the instruments randomly from the list

beat_track_instr = beat_track_instruments[random.randint(0, len(beat_track_instruments) - 1)]
main_track_instr = main_track_instruments[random.randint(0, len(main_track_instruments) - 1)]

# Changing Beat Track to Beat Track Instrument

MyMIDI.addProgramChange(beat_track, beat_channel, beat_time, beat_track_instr)

# Add Beat Track to MIDIFile Object

t = 0

for i, pitch in enumerate(beat_degrees):
	duration = durations[i % len(durations)]
	MyMIDI.addNote(beat_track, beat_channel, pitch, beat_time + t, durations[i], beat_volume)
	t = t + durations[i]

# Changing Main Track to Main Track Instrument

MyMIDI.addProgramChange(music_track, music_channel, music_time, main_track_instr)

# Add Main Track to MIDIFile Object
total_duration = t
t = 0

for i, pitch in enumerate(degrees):
	duration = float(durations[i % len(durations)]) * len(beat_degrees) / len(degrees)
	if(pitch != 0):
		MyMIDI.addNote(music_track, music_channel, pitch, music_time + t, duration, music_volume)
		t = t + duration
	else:
		t = t + duration

# Displaying info

print("No. of main track notes: %d" % len(degrees))
print("No. of beat track notes: %d" % len(beat_degrees))
print("Function used: %s" % duration_func.__name__)

# Writing output to MIDI file

with open("output.mid", "wb") as outfile:
	MyMIDI.writeFile(outfile)
