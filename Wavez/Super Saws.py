# =============================================================================
# User specific settings 
# =============================================================================
import os
import datetime

# Define the directory path
directory_path = 'C:/Users/IOX20/OneDrive - Texas A&M University/BMEN 211/Plugin/'

# Change the current working directory to the directory path
os.chdir(directory_path)

# =============================================================================
# Imports
# =============================================================================

import numpy as np
from scipy.io import wavfile # WAV File Generation
import matplotlib.pyplot as plt # Waveform Plotting
import scipy
from scipy import signal


# =============================================================================
# Inputs
# =============================================================================
note = 'C'
octave = -2
duration = 10
sample_rate = 44100

#Supersaw specific parameters
num_voices = 12
detune = 0.2

# =============================================================================
# Functions
# =============================================================================
def get_note_frequency(note, octave):
    """
    Given a note and octave, return the corresponding frequency.
    """
    note_map = {
        'C': 261.63,
        'C#': 277.18,
        'D': 293.66,
        'D#': 311.13,
        'E': 329.63,
        'F': 349.23,
        'F#': 369.99,
        'G': 392.00,
        'G#': 415.30,
        'A': 440.00,
        'A#': 466.16,
        'B': 493.88
    }
    return note_map[note] * (2**octave)


def graph_waveform(equation, frequency, duration, sample_rate):
    # Generate the time array and evaluate the equation at each time point
    time_array = np.arange(0, duration, 1 / sample_rate)
    waveform = eval(equation)
    
    # Scale the waveform to the range of [-1, 1]
    scaled_waveform = waveform / np.max(np.abs(waveform))

    # Set the x-axis limits to one period of the waveform
    period = 1 / frequency
    plt.xlim(0, period)
    
    # Plot the waveform
    plt.plot(time_array, scaled_waveform)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.title(file_name)
    plt.show()


def generate_supersaw(num_voices, detune, frequency, duration, sample_rate, file_name):
    # Generate the time array
    time_array = np.arange(0, duration, 1 / sample_rate)

    # Generate the sawtooth waveforms with detuned frequencies and phases
    sawtooth_waveforms = []
    for i in range(num_voices):
        detune_factor = detune * (i - (num_voices - 1) / 2)
        voice_frequency = frequency * (2 ** (detune_factor / 1200))
        voice_phase = 2 * np.pi * i / num_voices
        voice_waveform = scipy.signal.sawtooth(2 * np.pi * voice_frequency * time_array + voice_phase)
        sawtooth_waveforms.append(voice_waveform)

    # Sum the sawtooth waveforms together and scale the waveform to the range of [-1, 1]
    waveform = np.sum(sawtooth_waveforms, axis=0) / num_voices
    scaled_waveform = waveform / np.max(np.abs(waveform))

    # Convert the waveform to integers
    int_waveform = np.int16(scaled_waveform * 32767)
    
    # Export the waveform as a sound file
    file_name = file_name.replace('frequency', f'{frequency}mhz')
    file_name = f"{file_name}.wav"
    wavfile.write(file_name, sample_rate, int_waveform)


# =============================================================================
# Code
# =============================================================================

# Get the frequency for the given note and octave
frequency = get_note_frequency(note, octave)

# Generate file name based on input parameters and current date
detune_cents = round(detune * 100, 2)
date_string = datetime.datetime.now().strftime("%Y%m%d")
file_name = f"Supersaw_{note}{octave}_voices{num_voices}_detune{detune_cents}c_{date_string}.wav"

# Call the function to export the waveform as a sound file
generate_supersaw(num_voices, detune, frequency, duration, sample_rate, file_name)



# Call the function to graph the waveform
#graph_waveform(equation, frequency, duration, sample_rate)
