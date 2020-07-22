from logging import getLogger
import numpy as np

logger = getLogger(__name__)

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib import pyplot as plt


class Spectre(FigureCanvas):

    def __init__(self, fs, nfft=512, marker_size=None, parent=None):
        figure = plt.figure()
        super().__init__(figure)
        self.fs = fs
        self.nfft = nfft
        self._bar = None
        self.p = None
        self.t=0
        self.isSilent = True

        ax = figure.add_subplot(1,1,1)
        self.axis = ax
        ax.set_xscale("log")
        ax.set_xlim([10,fs//2])
        self._ymin = 0
        self._ymax = 100
        ax.set_ylim([0, 100])

        nyq = nfft//2
        self.nyq=nyq

        data = np.zeros((nyq,2), dtype=np.float64)
        self._data = data
        data[:,0] = np.linspace(0,fs//2,num=nyq)
        self._l = ax.scatter(data[:,0],data[:,1], s=marker_size)
        
        self.show()

    def start_stream(self):
        pass


    def on_quit(self):
        pass

    def update_with(self, a):
        b = a[np.isfinite(a)]
        ymin = np.min(b)
        ymax = np.max(b)
        if ymin < self._ymin:
            self._ymin = ymin
            if ymax > self._ymax:
                self._ymax = ymax
                self.axis.set_ylim(ymin, ymax)
            else:
                self.axis.set_ylim(bottom=ymin)
        elif ymax > self._ymax:
            self._ymax = ymax
            self.axis.set_ylim(top=ymax)

        self._data[:,1] = a
        self._l.set_offsets(self._data)
        self.draw_idle()

    def silent(self):
        self.isSilent = True
        self.axis.set_title("<Quiet>")
        self._data[:,1] = 0
        self._l.set_offsets(self._data)
        self.draw_idle()

    def working(self):
        self.isSilent = False
        self.axis.set_title("working")
        
        
        

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    me = Spectrogram(44100,nfft=4096)
    app.aboutToQuit.connect(me.on_quit)
    me.show()
    me.start_stream()
    app.exec_()
