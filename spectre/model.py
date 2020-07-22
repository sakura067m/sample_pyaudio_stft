import sys
from . import np, getLogger
import pyaudio

logger = getLogger(__name__)
fft = np.fft.fft

from .view import Spectre
from PyQt5.QtWidgets import QApplication
from time import time

tmp = ">i{}" if sys.byteorder=="big" else "<i{}"

class RealTimeSTFT(Spectre):

    def __init__(self, fs, byte_depth=2, device=0, nfft=512, marker_size=2, parent=None):
        super().__init__(fs, nfft, marker_size, parent)
        self.byte_depth = byte_depth
        if 3 == byte_depth:
            self.samplewidth = 4
            self.crop = 1
        else:
            self.samplewidth = byte_depth
            self.crop = 0
        self.fmt = tmp.format(self.samplewidth)
        self.device_index = device
       

    def start_stream(self):
        p = pyaudio.PyAudio()
        self.p = p
        stream = p.open(format=pyaudio.get_format_from_width(self.samplewidth,
                                                             unsigned=False
                                                             ),
                        rate = self.fs,
                        channels = 1,
                        frames_per_buffer = self.nfft,
                        input = True,
                        input_device_index = self.device_index,
                        output = False,
                        stream_callback=self.fft
                        )
        self.stream = stream
        p_info = p.get_device_info_by_index(2)
        logger.info("device: %s", p_info["name"])


    def on_quit(self):
        if self.p:
            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()


    def fft(self,in_data, frame_count, time_info, status):
        if pyaudio.paInputUnderflow == status:
            self.silent()
            return (None, pyaudio.paContinue)
##        ct = time_info["current_time"]
        ct = time()
        if ct-self.t>1/30:
            self.t = ct

            data = np.frombuffer(in_data, 'b').reshape(-1, self.samplewidth)
##            data = np.ndarray((frame_count,),
##                              dtype=self.fmt,
##                              buffer=in_data
##                              )
            if (data==0).all(axis=1).sum() > frame_count//4*3:
                self.silent()
                return (None, pyaudio.paContinue)
            # print(data[:10])
            if self.crop:
                data = np.roll(data, -1, axis=1).view(self.fmt).ravel()
##                data = data.view(self.fmt).ravel()
                z = fft(data>>8, self.nfft)
            else:
                z = fft(data.view(self.fmt).ravel(), self.nfft)
            
            a = 20*np.log10(np.abs(z[:self.nyq]))
            if not np.isfinite(a).all():
                self.silent()
                return (None, pyaudio.paContinue)
            if self.isSilent: self.working()
            self.update_with(a)
        return (None, pyaudio.paContinue)

    @classmethod
    def go(cls, fs, byte_depth=2, device=0, nfft=4096, marker_size=2, argv=[], **etc):
        app = QApplication(argv)
        me = RealTimeSTFT(fs, byte_depth, device, nfft, marker_size)
        app.aboutToQuit.connect(me.on_quit)
        me.show()
        me.start_stream()
        return app.exec_()


if __name__ == "__main__":
    sys.exit(RealTimeSTFT(44100, argv=sys.argv()))
