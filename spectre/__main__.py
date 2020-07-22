import sys
from . import RealTimeSTFT, getLogger, StreamHandler, handler_format, DEBUG
import logging
from argparse import ArgumentParser

logger = getLogger(".".join((__package__, __name__)))

description = """\
spectrum analyzer
"""

def main():
    parser = ArgumentParser(description=description)
    parser.add_argument('fs',
                        nargs='?',
                        help='sampling rate',
                        type=int,
                        default=44100,
                        )
    parser.add_argument('byte_depth',
                        nargs='?',
                        help='byte depth: 1->8bit 2->16bit 3->24bit 4->32bit',
                        choices=[1,2,3,4],
                        type=int,
                        default=2,
                        )
    parser.add_argument('device',
                        nargs='?',
                        help='device index: 0 is default',
                        type=int,
                        default=0,
                        )
    parser.add_argument("-w", '--nfft',
                        nargs='?',
                        help='window size',
                        type=int,
                        default=4096,
                        )
    parser.add_argument("-s", '--marker-size',
                        nargs='?',
                        help='marker size',
                        type=int,
                        default=2,
                        )
    parser.add_argument("-v", '--verbose',
                        help='increase out put',
                        action="store_true",
                        )
    args = parser.parse_args()
    if args.verbose:
##        fmt = '%(asctime)s.%(msecs)d [%(levelname)s: %(name)s] %(message)s'
##        datefmt = '%Y/%m/%d %H:%M:%S'
##        logging.basicConfig(format=fmt, datefmt=datefmt,
##                            level=logging.DEBUG,
##                            )
        mod_logger = getLogger(__package__)
        mod_logger.setLevel(DEBUG)
        stream_handler = StreamHandler(sys.stdout)
        stream_handler.setFormatter(handler_format)
        stream_handler.setLevel(DEBUG)
        logger.addHandler(stream_handler)
    logger.debug(args)
    logger.info("%d bit/%d Hz", args.byte_depth*8, args.fs)
                        
    return RealTimeSTFT.go(**vars(args), argv=sys.argv)

if __name__ == "__main__":
    sys.exit(main())
