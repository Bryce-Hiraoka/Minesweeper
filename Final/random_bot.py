import pyautogui
import random
from PIL import Image

# Minesweeper bot V1 randomness
# Inspired by Code Bullet Video (https://www.youtube.com/watch?v=ehAStJmx_Fo)

# Ensure the proper set up for script
img = pyautogui.screenshot(region=(958,423, 1, 1))
pixel = img.getcolors()[0][1][0]

if pixel != 252:
    print("Set up not correct!!!")

else:

    # main loop
    while True:

        # pyautogui to screenshot specific pixel to determine state of game (loss, win, neutral)
        img = pyautogui.screenshot(region=(958,423, 1, 1))
    
        # get/store pixel color with pillow
        pixel = img.getcolors()[0][1][0]

        # check for game loss
        if pixel == 53:
            pyautogui.click(x=800, y=315)
        
        # check for game win
        if pixel == 181:
            print("Congrats on finally winning")

        # choose random X and Y coordinate within grid params
        rand_X = random.randint(780, 1150)

        rand_Y = random.randint(510, 870)

        # click at random coordinate
        pyautogui.click(x=rand_X, y=rand_Y, button='left')
