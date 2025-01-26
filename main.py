import cv2
import time
import numpy as np
import screen_brightness_control as sbc

# Initialize the camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Cannot open camera")
    exit()
    
def adjust_brightness(luminance):
    # Define luminance and brightness ranges
    min_luminance = 0.1
    max_luminance = 0.9
    min_brightness = 0.0 
    max_brightness = 1.0 
    # Normalize luminance to brightness
    brightness = (luminance - min_luminance) / (max_luminance - min_luminance) 
    brightness = max(min_brightness, min(brightness, max_brightness)) 
    return brightness

def set_screen_brightness(brightness):
    # Set the screen brightness
    sbc.set_brightness(brightness)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Calculate luminance
    luminance = np.mean(gray) / 255.0
    # Adjust brightness based on luminance
    brightness = adjust_brightness(luminance)
    setbr = int(brightness * 100)
    # Set screen brightness
    set_screen_brightness(setbr)
    # Display the resulting frame with brightness info
    """ cv2.putText(frame, f'Brightness: {setbr}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imshow('Camera Feed', frame) """
    print(f'Brightness: {setbr}')
    time.sleep(5)
    # Break the loop on 'q' key press
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()