import cv2
import time


def get_stats(RECORDING_DURATION=5):
    capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    frame_count = 0

    start_time = time.time()
    while time.time() - start_time < RECORDING_DURATION:
        # Capture frame from camera
        ret, frame = capture.read()

        # Check if frame was captured successfully
        if not ret:
            break

        # Display frame
        cv2.imshow('Testing', frame)
        frame_count += 1

        # Wait for 1 millisecond before capturing the next frame
        cv2.waitKey(1)

    width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

    print(f"avg.FPS: {frame_count / 5}")
    print(f"Frame height: {height} px")
    print(f"Frame width: {width} px")


def get_last_X_minutes(buffer, minutes, FPS):
    # Calculate the number of frames to retrieve (5 minutes worth at 26 FPS)
    num_frames = minutes * 60 * FPS

    # If the buffer has fewer frames than the requested number, return the entire buffer
    if len(buffer) <= num_frames:
        return buffer

    # Otherwise, return the last num_frames frames from the buffer
    else:
        return buffer[-num_frames:]
