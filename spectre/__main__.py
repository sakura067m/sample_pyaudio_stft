import sys
from . import RealTimeSTFT, getLogger, StreamHandler, handler_format, DEBUG
from argparse import ArgumentParser

logger = getLogger(__name__)

description = """\
spectrum analyzer
"""

def main():
    parser = ArgumentParser(prog="spectre",
                            description=description
                            )
    parser.add_argument("-f", '--fs',
                        help='sampling rate',
                        type=int,
                        default=44100,
                        )
    parser.add_argument("-w", '--nfft',
                        help='window size',
                        type=int,
                        default=512,
                        )
    parser.add_argument("-s", '--marker_size',
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
        logger.setLevel(DEBUG)
        stream_handler = StreamHandler(sys.stdout)
        stream_handler.setFormatter(handler_format)
        stream_handler.setLevel(DEBUG)
        logger.addHandler(stream_handler)
    logger.info(args)
                        
    return RealTimeSTFT.go(**vars(args), argv=sys.argv)

if __name__ == "__main__":
    sys.exit(main())
