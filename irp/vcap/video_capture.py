import cv2

def start_cap(path):
    print(cv2.__version__)
    vcap = cv2.VideoCapture(path)

    if not vcap.isOpened():
        print("Error opening video stream or file")

    while vcap.isOpened():
        ret, frame = vcap.read()
        if ret:
            cv2.imshow('Video', frame)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        else:
            break

    vcap.release()
    cv2.destroyAllWindows()