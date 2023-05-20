# Saving 1 second clips instead of frames
import cv2

# Define constants
FRAME_RATE = 60  # frames per second
waitTime = int(1000 / FRAME_RATE)
FRAME_SIZE = (1920, 1080)  # video frame size

# Initialize camera capture
capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # get rid of the cv2.CAP_DSHOW when running on rpi
capture.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_SIZE[0])
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_SIZE[1])
capture.set(cv2.CAP_PROP_FPS, FRAME_RATE)
capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))

out = cv2.VideoWriter('outpy.avi', cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'), FRAME_RATE, FRAME_SIZE)


while True:
    # Capture frame from camera
    ret, frame = capture.read()

    # Check if frame was captured successfully
    if not ret:
        break
    out.write(frame)

    # Display frame
    cv2.imshow('Dashcam', frame)

    # Wait for key press to exit
    if cv2.waitKey(waitTime) == ord('q'):
        break
capture.release()
out.release()