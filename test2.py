import numpy as np
from matplotlib import pyplot as plt
from scipy.io.wavfile import read as wave_read
from scipy.signal import stft


"""
see,
    https://water2litter.net/rum/post/python_scipy_io_wavfile_read/
    https://qiita.com/MuAuan/items/8850e037babcff991b8e
"""

fft = np.fft.fft

CHUNK=512
fs, data = wave_read("cat.wav")

fc = fs//CHUNK
x_fft = np.linspace(0,fs,CHUNK)
nyq = len(x_fft)//2


##

dt = fs//60
f,t,z = stft(data[:,0], fs=fs, nperseg=CHUNK)
a = np.abs(z)
plt.pcolormesh(t, f, np.abs(z), vmin=0, vmax=np.max(a))
plt.ylim([f[1],f[-1]])
plt.yscale("log")
plt.ylabel("Freq.[Hz]")
plt.xlabel("t[sec]")
plt.show()
