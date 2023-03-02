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
duration = 5
sample_rate = 44100

#Supersaw specific parameters
num_voices = 48
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
    '''
    duration = len(signal) / sample_rate
    t = np.linspace(0, duration, len(signal), endpoint=False)
    plt.plot(t, signal)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    if equation is not None:
        plt.title(f'Waveform and Equation:\n{equation}')
    else:
        plt.title('Waveform')
    plt.show()
    '''


def generate_supersaw(num_voices, detune, frequency, duration, sample_rate, file_name):
    freq = get_note_frequency(note, octave)
    t = np.linspace(0, duration, int(duration*sample_rate), endpoint=False)
    supersaw = np.zeros(len(t))
    for i in range(num_voices):
        freq_i = freq*(i+1) + (i+1)*detune*freq
        saw_i = signal.sawtooth(2 * np.pi * freq_i * t)
        supersaw += saw_i / (i+1)
    supersaw /= np.max(np.abs(supersaw))
    equation = ''
    for i in range(num_voices):
        freq_i = freq*(i+1) + (i+1)*detune*freq
        if i > 0:
            equation += ' + '
        equation += f'sawtooth({freq_i:.2f} * 2 * pi * t) / {i+1}'
    equation += f', {num_voices} voices, detune={detune:.2f}'
    return supersaw, equation, file_name


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
supersaw, equation, file_name = generate_supersaw(num_voices, detune, frequency, duration, sample_rate, file_name)


# Call the function to graph the waveform
graph_waveform(equation, frequency, duration, sample_rate)
