# =============================================================================
# Devlog
# =============================================================================
'''
# Currently Implemented:
    # Waveform generation given equation
        # Note and octave specificity
    # Graph of one period of waveform

# Things to implement:
    # Live tuning of samples
        # Master Volume knob
            #-20dB to +10dB
        # UI
            # Graphs of waveform
                # Serum Esque, but with many waveforms
                    # Color code with legend
            # Knobs; potentiometer esque, include faders for misc parameters
    # Multiple Voices
        # Summation of waves via function
            # Detune as parameter
            # Number of voices as parameter
            # Toggle for using set of equations under nomenclature (equation n)
                # Otherwise prompt inputs of equations
            # Toggle for supersaw / superimposed fxns (duplicate equations)
        # Graph og waveforms dotted and final waveform solid
    # Add Noise
        # Toggle for type / frequency
        # Parameters for level, randomness
    # Frequency Analysis
        # Bode Diagram plot of signal
        # Visual EQ? Once live tuning gets set up
    # LFO / Waveform to modulate parameters
        # Macro system
'''

# =============================================================================
# User specific settings 
# =============================================================================
import os

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

# =============================================================================
# Inputs
# =============================================================================
note = 'C'
octave = -2
duration = 1
sample_rate = 44100

################################## Equations ##################################
'''
# Sinusoidal wave with point of inflection
equation = "np.sin(2 * np.pi * frequency * time_array) + 0.5 * np.sin(4 * np.pi * frequency * time_array)"

# Sinusoidal wave
equation = "np.sin(2 * np.pi * frequency * time_array)"  # Sine Wave

# Sawtooth wave
equation = "2 * (time_array * frequency - np.floor(0.5 + time_array * frequency))"  # Sawtooth Wave

# Triangle wave
equation = "2 * np.abs(2 * (time_array * frequency - np.floor(0.5 + time_array * frequency))) - 1"  # Triangle Wave

# Square wave
equation = "np.sign(np.sin(2 * np.pi * frequency * time_array))"  # Square Wave

# Unit Step equation
equation = "np.heaviside(time_array, 0.5)" # Unit Step
'''

equation = "np.sign(np.sin(2 * np.pi * frequency * time_array))"  # Square Wave



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

def generate_waveform(equation, frequency, duration, sample_rate, file_name):

    # Generate the time array and evaluate the equation at each time point
    time_array = np.arange(0, duration, 1 / sample_rate)
    waveform = eval(equation)

    # Scale the waveform to the range of [-1, 1] and convert it to integers
    scaled_waveform = waveform / np.max(np.abs(waveform))
    int_waveform = np.int16(scaled_waveform * 32767)

    # Export the waveform as a sound file
    file_name = file_name.replace('frequency', f'{frequency}mhz')
    file_name = f"{file_name}.wav"
    wavfile.write(file_name, sample_rate, int_waveform)

    # Plot the waveform
    fig, ax = plt.subplots()
    period_samples = int(sample_rate / frequency)
    ax.plot(time_array[:period_samples], waveform[:period_samples])
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    plt.show()


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



# =============================================================================
# Code
# =============================================================================

# Get the frequency for the given note and octave
frequency = get_note_frequency(note, octave)

# Filter illegal characters from the file name
file_name = equation
file_name = file_name.replace('np.', '')
file_name = file_name.replace('*', 'x')
file_name = file_name.replace('<', 'less than')
file_name = file_name.replace('np.pi', 'pi')
file_name = file_name.replace('time_array', f'time_array_{int(sample_rate)}hz')

# Call the function to export the waveform as a sound file
generate_waveform(equation, frequency, duration, sample_rate, file_name)

# Call the function to graph the waveform
graph_waveform(equation, frequency, duration, sample_rate)