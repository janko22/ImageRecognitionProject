import sys
from irp.vcap.video_capture import VideoCapture

def main():
    video_capture = VideoCapture(sys.argv[1])
    video_capture.play_video()

if __name__ == '__main__':
    main()