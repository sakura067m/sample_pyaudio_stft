import sys
from . import RealTimeSTFT

def main():
    return RealTimeSTFT.go(48000, argv=sys.argv)

if __name__ == "__main__":
    sys.exit(main())
