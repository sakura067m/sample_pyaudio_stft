__all__ = ["RealTimeSTFT"]

import sys
from logging import getLogger, StreamHandler, Formatter, DEBUG
stream_handler = StreamHandler(sys.stdout)
fmt = '%(asctime)s.%(msecs)d [%(levelname)s: %(name)s] %(message)s'
datefmt = '%Y/%m/%d %H:%M:%S'
handler_format = Formatter(fmt=fmt, datefmt=datefmt)

import numpy as np
np.seterr(divide='ignore')

from .model import RealTimeSTFT
