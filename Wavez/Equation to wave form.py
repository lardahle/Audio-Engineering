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
from scipy.io import wavfile

import matplotlib.pyplot as plt

# =============================================================================
# Inputs
# =============================================================================
# Define an equation in terms of time
equation = "np.sin(2 * np.pi * frequency * time_array) + 0.5 * np.sin(4 * np.pi * frequency * time_array)"
frequency = 440
duration = 5
sample_rate = 44100


# =============================================================================
# Functions
# =============================================================================


def generate_waveform(equation, frequency, duration, sample_rate, file_name):
    # Generate the time array and evaluate the equation at each time point
    time_array = np.arange(0, duration, 1 / sample_rate)
    waveform = eval(equation)

    # Scale the waveform to the range of [-1, 1] and convert it to integers
    scaled_waveform = waveform / np.max(np.abs(waveform))
    int_waveform = np.int16(scaled_waveform * 32767)
    
    # Export the waveform as a sound file
    file_name = f"{file_name}.wav"
    wavfile.write(file_name, sample_rate, int_waveform)


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

# Filter illegal characters from the file name
file_name = equation
file_name = file_name.replace('np.', '')
file_name = file_name.replace('*', 'x')
file_name = file_name.replace('np.pi', 'pi')
file_name = file_name.replace('frequency', f'{frequency}mhz')
file_name = file_name.replace('time_array', f'time_array_{int(sample_rate)}hz')

# Call the function to export the waveform as a sound file
generate_waveform(equation, frequency, duration, sample_rate, file_name)

# Call the function to graph the waveform
graph_waveform(equation, frequency, duration, sample_rate)