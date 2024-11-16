import sys
from irp.vcap.video_capture import VideoManager

def main():
    video_capture = VideoManager(sys.argv[1])
    video_capture.play_video()

if __name__ == '__main__':
    main()