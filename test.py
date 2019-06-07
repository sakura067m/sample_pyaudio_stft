import numpy as np
from matplotlib import pyplot as plt
import pyaudio
from itertools import cycle

"""
see, https://www.logical-arts.jp/archives/112
"""

fft = np.fft.fft

CHUNK=1024*4
fs=44100
p=pyaudio.PyAudio()

fc = fs//CHUNK
x_fft = np.linspace(0,fs,CHUNK)
nyq = len(x_fft)//2

stream = p.open(format = pyaudio.paInt16,
                channels = 1,
                rate = fs,
                frames_per_buffer = CHUNK,
                input = True,
                )

nf = fc * 5
frames = [None]*nf

for i in range(nf):
    frames[i] = stream.read(CHUNK)

stream.stop_stream()
stream.close()
p.terminate()

##
data = np.empty(CHUNK*nf)
n = CHUNK*nf
for k,chunk in enumerate(frames):
    data[k*CHUNK:(k+1)*CHUNK] = np.frombuffer(chunk, dtype=np.int16) / 32768
dt = fs//60
spectrogram = np.empty((60*5-1,nyq), dtype=np.float64)
for k,r in enumerate(spectrogram):
    if k*dt+CHUNK > n: break
    spectr = fft(data[k*dt:k*dt+CHUNK])
    r[...] = np.log(np.absolute(spectr[:nyq]))

btm = np.min(spectrogram)
print("bottom:",btm)
plt.ylim(bottom=btm)
ax = plt.bar(x_fft[:nyq], spectrogram[0], width=fc)
for sp in cycle(spectrogram[:k]):
    for bar,new_x in zip(ax, sp):
        bar.set_height(new_x)
    plt.pause(0.01)
