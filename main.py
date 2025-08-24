from PIL import ImageGrab
import time
import numpy as np
import pyautogui
import keyboard

paused = False
running = True

def toggle_pause():
    global paused
    paused = not paused  # Flip pause state
    
def stop_program():
    global running
    running = False  # Exit the loop

tolerance = 30


keyboard.add_hotkey('f5', toggle_pause)
keyboard.add_hotkey('f6', stop_program)

print("Press F5 to pause/unpause the application and F6 to terminate it.")

# Capture the screen to search for colors. We put it in an infinite loop to constantly update
while running:
    if not paused:

        screenMonitor = ImageGrab.grab()

        screenshot = np.array(screenMonitor)

        brightness = np.mean(screenshot, axis=-1)

        # This creates a boolean mask where True pixels are within tolerance of your target color
        mask = ((np.all(np.abs(screenshot - [208, 203, 203]) <= tolerance, axis=-1) | np.all(np.abs(screenshot - [173, 216, 230]) <= tolerance, axis=-1)) & (brightness > 120))

        # Converts our mask variable to x and y positions to actually find where the target pixels are located
        ycoord, xcoord = np.where(mask)

        # Some error handling since if no coordinates are found array will return empty and crash the program
        # We also have a distance filter here so our mouse does not jump randomly everywhere
        if len(xcoord) > 0 and len(ycoord) > 0:
            target_x = int(np.mean(xcoord))   
            target_y = int(np.mean(ycoord)) 
            current_x, current_y = pyautogui.position()
            distance = ((current_x - target_x)**2 + (current_y - target_y)**2)**0.5
    
            if distance < 200:  # Only move if within 200 pixels
                pyautogui.moveTo(target_x, target_y, duration=0.4)  

        # We add a bit of delay so we don't overwhelm our computer
        time.sleep(0.1)
    
    # If you pause the program and don't have this the cpu usage will jump to 100% since you're checking infinitely and as fast ap
    else:
        time.sleep(0.1)