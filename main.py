import cv2
import sys
import time
from tqdm import tqdm
import threading

import helpers

# Define constants
FRAME_RATE = 29  # frames per second
waitTime = int(1000 / FRAME_RATE)
FRAME_SIZE = (640, 480)  # video frame size
BUFFER_SIZE = FRAME_RATE * 60 * 3  # number of frames to keep in buffer (3 minute)

# Initialize circular buffer
frame_buffer = []
buffer_idx = 0

# Initialize camera capture
capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # get rid of the cv2.CAP_DSHOW when running on rpi
capture.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_SIZE[0])
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_SIZE[1])
capture.set(cv2.CAP_PROP_FPS, FRAME_RATE)
capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))

# Initialize flag variable
is_recording = True
stop_recording = False


def record():
    global frame_buffer
    global buffer_idx
    global is_recording
    global stop_recording

    # Loop through frames
    while is_recording and not stop_recording:
        # print("Recording...")
        # Capture frame from camera
        ret, frame = capture.read()

        # Check if frame was captured successfully
        if not ret:
            print("Cannot open camera!")
            break

        # Add frame to buffer
        if len(frame_buffer) < BUFFER_SIZE:
            frame_buffer.append(frame)
        else:
            frame_buffer[buffer_idx] = frame

        # Increment buffer index
        buffer_idx = (buffer_idx + 1) % BUFFER_SIZE


def exit_captures():
    capture.release()
    cv2.destroyAllWindows()


def diagnostic():
    print("Recording for 2 minutes to save a test file")
    # Recording
    thread = threading.Thread(target=record)
    thread.start()

    for i in tqdm(range(2*60)):
        time.sleep(1)

    stop_recording = True
    print("done")

    # # display all the frames in buffer
    # for frame in frame_buffer:
    #     cv2.imshow("Frames in buffer", frame)
    #     if cv2.waitKey(int(1000/FRAME_RATE))

    # initialize writer
    out = cv2.VideoWriter('TestVideo.avi', cv2.VideoWriter_fourcc(*'XVID'), FRAME_RATE, FRAME_SIZE)

    print('Saving test video')
    last_1_minutes = helpers.get_last_X_minutes(frame_buffer, 1, FRAME_RATE)
    for i in tqdm(range(len(last_1_minutes))):
        out.write(frame_buffer[i])
        cv2.waitKey(int(1000 / FRAME_RATE))

    # Closing all windows
    exit_captures()


if __name__ == '__main__':

    thread = threading.Thread(target=record)
    thread.start()

    input("Click enter to stop")
    stop_recording = True
