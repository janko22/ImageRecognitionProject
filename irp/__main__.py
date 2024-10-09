import sys
from irp.vcap.video_capture import start_cap

def main():
    start_cap(sys.argv[1])

if __name__ == '__main__':
    main()