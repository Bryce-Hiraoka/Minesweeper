import pyautogui
import random
from PIL import Image
import time

# Minesweeper bot V1 randomness
# Inspired by Code Bullet Video (https://www.youtube.com/watch?v=ehAStJmx_Fo)

# Ensure the proper set up for script

# r1: 522
# r2: 566
# r3: 604
# r4: 649
# r5: 690
# r6: 736
# r7: 774
# r8: 816
# r9: 853

# c1: 800
# c2: 840
# c3: 885
# c4: 922
# c5: 970
# c6: 1010
# c7: 1049
# c8: 1090


img = pyautogui.screenshot(region=(958,423, 1, 1))
pixel = img.getcolors()[0][1][0]

if pixel != 252:
    print("Set up not correct!!!")

else:

    start_time = time.time()
    time_limit = 900

    # main loop
    for _ in range(100000):

        if time.time() - start_time > time_limit:
            print("timeout")
            break

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
