import cv2
import sys
import time
from tqdm import tqdm
import threading

import helpers

# Define constants
FRAME_RATE = 26  # frames per second
waitTime = int(1000 / FRAME_RATE)
FRAME_SIZE = (1920, 1080)  # video frame size
BUFFER_SIZE = 26 * 60 * 3  # number of frames to keep in buffer (3 minute)

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


def record():
    frame_count = 0
    global frame_buffer
    global buffer_idx
    global is_recording

    # Loop through frames
    while is_recording:
        # Capture frame from camera
        ret, frame = capture.read()

        # Check if frame was captured successfully
        if not ret:
            break

        # Add frame to buffer
        if len(frame_buffer) < BUFFER_SIZE:
            frame_buffer.append(frame)
        else:
            frame_buffer[buffer_idx] = frame

        # Increment buffer index
        buffer_idx = (buffer_idx + 1) % BUFFER_SIZE

        # Display frame
        cv2.imshow('Dashcam', frame)
        frame_count += 1

        # Wait for key press to exit
        if cv2.waitKey(1) == ord('q') or not is_recording:
            is_recording = False
            break

    print(f"Received Frames {frame_count}")


def exit_captures():
    capture.release()
    cv2.destroyAllWindows()


def diagnostic():
    # start_time = time.time()
    # Recording
    recordThread = threading.Thread(target=record)
    recordThread.start()
    # time.sleep(4)
    # is_recording = False

    # # get stats
    # time_taken = time.time() - start_time
    # size_taken_MB = sys.getsizeof(frame_buffer) / 1024
    #
    # print(f"FPS:{int(len(frame_buffer) / time_taken)}")
    # print(f"Recorded Frames: {len(frame_buffer)}")
    # print(f"Space taken by buffer:{size_taken_MB} kB")
    # print(f"Time taken : {time_taken} seconds")
    # size_per_second = size_taken_MB / time_taken
    # size_per_hour = size_per_second * 3600
    # print(f"Est size of 1 hour video: {size_per_hour} kB")

    # Show all frames in buffer

    # initialize writer
    out = cv2.VideoWriter('outpy.avi', cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'), FRAME_RATE, FRAME_SIZE)

    last_1_minutes = helpers.get_last_X_minutes(frame_buffer, 1, FRAME_RATE)
    for i in tqdm(range(len(last_1_minutes))):
        out.write(frame_buffer[i])
        cv2.waitKey(int(1000/FRAME_RATE))

    # Closing all windows
    exit_captures()


if __name__ == '__main__':
    diagnostic()
