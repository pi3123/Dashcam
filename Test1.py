import cv2
import threading

# Define constants
FRAME_RATE = 29  # frames per second
waitTime = int(1000 / FRAME_RATE)
FRAME_SIZE = (640, 480)  # video frame size
BUFFER_SIZE = FRAME_RATE * 60 * 3  # number of frames to keep in buffer (3 minutes)

# Initialize circular buffer
frame_buffer = []
buffer_idx = 0

# Initialize camera capture
capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # get rid of the cv2.CAP_DSHOW when running on rpi
capture.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_SIZE[0])
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_SIZE[1])
capture.set(cv2.CAP_PROP_FPS, FRAME_RATE)
capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))

# Initialize flag variables
is_recording = True
stop_recording = False


# Function to record video frames
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


# Start recording in the background
thread = threading.Thread(target=record)
thread.start()

# Wait for specific keyword from the user
input_keyword = input("Enter 'stop' to stop recording: ")
if input_keyword == "stop":
    stop_recording = True

# Wait for the background thread to finish
thread.join()

# Release resources
capture.release()

for frame in frame_buffer:
    cv2.imshow("Frame",frame)
    cv2.waitKey(int(1000/ FRAME_RATE))
# The recording has stopped
print("Recording finished.")
