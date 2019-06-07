import numpy as np

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib import pyplot as plt


class Spectre(FigureCanvas):

    def __init__(self, fs, nfft=512, parent=None):
        figure = plt.figure()
        super().__init__(figure)
        self.fs = fs
        self.nfft = nfft
        self._bar = None
        self.p = None
        self.t=0

        ax = figure.add_subplot(1,1,1)
        self.axis = ax
        ax.set_xscale("log")
        ax.set_xlim([10,fs//2])
        self._ymin = -100
        self._ymax = 100
        ax.set_ylim([-100, 100])

        nyq = nfft//2
        self.nyq=nyq

        data = np.zeros((nyq,2), dtype=np.float64)
        self._data = data
        data[:,0] = np.linspace(0,fs//2,num=nyq)
        self._l = ax.scatter(data[:,0],data[:,1])

        self.show()

    def start_stream(self):
        pass


    def on_quit(self):
        pass

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    me = Spectrogram(44100,nfft=4096)
    app.aboutToQuit.connect(me.on_quit)
    me.show()
    me.start_stream()
    app.exec_()
