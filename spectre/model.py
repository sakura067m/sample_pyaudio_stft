from . import np, getLogger
import pyaudio

logger = getLogger(__name__)
fft = np.fft.fft

from .view import Spectre
from PyQt5.QtWidgets import QApplication
from time import time

last_data=None

class RealTimeSTFT(Spectre):

    def __init__(self, fs, nfft=512, marker_size=2, parent=None):
       super().__init__(fs, nfft, marker_size, parent)
       

    def start_stream(self):
        p = pyaudio.PyAudio()
        self.p = p
        stream = p.open(format=pyaudio.paInt16,
                        rate = self.fs,
                        channels = 1,
                        frames_per_buffer = self.nfft,
                        input = True,
                        input_device_index = 2,
                        output = False,
                        stream_callback=self.fft
                        )
        self.stream = stream


    def on_quit(self):
        if self.p:
            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()


    def fft(self,in_data, frame_count, time_info, status):
        if self.nfft > frame_count:
##            self._data[:,1] = 0
##            self._l.set_offsets(self._data)
##            self.draw()
            return (None, pyaudio.paContinue)
##        ct = time_info["current_time"]
        ct = time()
        if ct-self.t>1/60:
##        if True:
            self.t = ct
            try:
                data = np.frombuffer(in_data, dtype=np.int16)
                z = fft(data[:self.nfft])
            except:
                global last_data
                last_data = in_data
                raise
            a = 20*np.log10(np.abs(z))[:self.nyq]
            b = a[np.isfinite(a)]
            ymin = np.min(b)
            ymax = np.max(b)
            if ymin < self._ymin:
                self._ymin = ymin
                if ymax > self._ymax:
                    self._ymax = ymax
                    self.axis.set_ylim(ymin,ymax)
                else:
                    self.axis.set_ylim(bottom=ymin)
            elif ymax > self._ymax:
                self._ymax = ymax
                self.axis.set_ylim(top=ymax)


            self._data[:,1] = a
            self._l.set_offsets(self._data)
            self.draw()
##        print(ct, self.t, any(in_data), len(in_data),time_info)
        return (None, pyaudio.paContinue)

    @classmethod
    def go(cls, fs, nfft=4096, marker_size=2, argv=[], **args):
        app = QApplication(argv)
        me = RealTimeSTFT(fs, nfft, marker_size)
        app.aboutToQuit.connect(me.on_quit)
        me.show()
        me.start_stream()
        return app.exec_()


if __name__ == "__main__":
    import sys
    sys.exit(RealTimeSTFT(44100, argv=sys.argv()))
