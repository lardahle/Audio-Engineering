# =============================================================================
# Input Variables
# =============================================================================


# Modules
import time
import numpy as np
from scipy import signal, io


# =============================================================================
# Code
# =============================================================================
start = time.time()

# Load the original and affected audio files
fs, orig_audio = io.wavfile.read('original.wav')
fs, affected_audio = io.wavfile.read('affected.wav')

# Convert to mono if necessary
if orig_audio.ndim > 1:
    orig_audio = orig_audio[:, 0]
if affected_audio.ndim > 1:
    affected_audio = affected_audio[:, 0]

# Apply Fourier transform to both signals
orig_audio_fft = np.fft.fft(orig_audio)
affected_audio_fft = np.fft.fft(affected_audio)

# Divide transformed affected signal by transformed original signal to obtain transfer function
transfer_function_fft = affected_audio_fft / orig_audio_fft

# Convert transfer function back to time domain using inverse Fourier transform
transfer_function = np.fft.ifft(transfer_function_fft)

# Save transfer function as new audio file
io.wavfile.write('transfer_function.wav', fs, np.real(transfer_function))



################################### Outputs ###################################


end = time.time()
print("The total runtime of the above code was",(end-start), "seconds")
