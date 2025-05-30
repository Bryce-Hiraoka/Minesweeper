import pyautogui
import random
from PIL import Image

# x = 782 - 820, 824 - 862 , 866 - 904, 908 - 946, 950 - 988, 992 - 1030, 1034 - 1072, 1076 - 1114, 1118 - 1156
# y = 506 - 544, 548 - 586, 590 - 628, 632 - 670, 674 - 712, 716 - 754, 758 - 796, 800 - 838, 842 - 880 

# middle x = 801, 843, 885, 927, 969, 1011, 1053, 1095, 1137
# middle y = 525, 567, 609, 651, 693, 735, 777, 819, 861

# grey is 29 px long

class Box:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

def get_neighbors(x, y):
    move = 42

    # Middle blocks
    if x[0] > 1 and x[0] < 9 and y[0] > 1 and y[0] < 9:
        r = pyautogui.screenshot(region=(x[1] + move , y[1], 1, 1)).getcolors()[0][1][0]
        l = pyautogui.screenshot(region=(x[1] - move , y[1], 1, 1)).getcolors()[0][1][0]
        u = pyautogui.screenshot(region=(x[1], y[1] - move, 1, 1)).getcolors()[0][1][0]
        d = pyautogui.screenshot(region=(x[1], y[1] + move, 1, 1)).getcolors()[0][1][0]
        ru = pyautogui.screenshot(region=(x[1] + move , y[1] - move, 1, 1)).getcolors()[0][1][0]
        rd = pyautogui.screenshot(region=(x[1] + move , y[1] + move, 1, 1)).getcolors()[0][1][0]
        lu = pyautogui.screenshot(region=(x[1] - move , y[1] - move, 1, 1)).getcolors()[0][1][0]
        ld = pyautogui.screenshot(region=(x[1] - move , y[1] + move, 1, 1)).getcolors()[0][1][0]

        return [r, l, u, d, ru, rd, lu, ld]
    
    # top row
    elif x[0] > 1 and x[0] < 9 and y[0] == 1:
        r = pyautogui.screenshot(region=(x[1] + move , y[1], 1, 1)).getcolors()[0][1][0]
        l = pyautogui.screenshot(region=(x[1] - move , y[1], 1, 1)).getcolors()[0][1][0]
        d = pyautogui.screenshot(region=(x[1], y[1] + move, 1, 1)).getcolors()[0][1][0]
        rd = pyautogui.screenshot(region=(x[1] + move , y[1] + move, 1, 1)).getcolors()[0][1][0]
        ld = pyautogui.screenshot(region=(x[1] - move , y[1] + move, 1, 1)).getcolors()[0][1][0]

        return [r, l, d, rd, ld]

    # bottom row
    elif x[0] > 1 and x[0] < 9 and y[0] == 9:
        r = pyautogui.screenshot(region=(x[1] + move , y[1], 1, 1)).getcolors()[0][1][0]
        l = pyautogui.screenshot(region=(x[1] - move , y[1], 1, 1)).getcolors()[0][1][0]
        u = pyautogui.screenshot(region=(x[1], y[1] - move, 1, 1)).getcolors()[0][1][0]
        ru = pyautogui.screenshot(region=(x[1] + move , y[1] - move, 1, 1)).getcolors()[0][1][0]
        lu = pyautogui.screenshot(region=(x[1] - move , y[1] - move, 1, 1)).getcolors()[0][1][0]

        return [r, l, u, ru]
    
    # left row
    elif x[0] == 1 and y[0] > 1 and y[0] < 9:
        l = pyautogui.screenshot(region=(x[1] - move , y[1], 1, 1)).getcolors()[0][1][0]
        u = pyautogui.screenshot(region=(x[1], y[1] - move, 1, 1)).getcolors()[0][1][0]
        d = pyautogui.screenshot(region=(x[1], y[1] + move, 1, 1)).getcolors()[0][1][0]
        lu = pyautogui.screenshot(region=(x[1] - move , y[1] - move, 1, 1)).getcolors()[0][1][0]
        ld = pyautogui.screenshot(region=(x[1] - move , y[1] + move, 1, 1)).getcolors()[0][1][0]

        return [l, u, d, lu, ld]

    # right row
    elif x[0] == 9 and y[0] > 1 and y[0] < 9:
        r = pyautogui.screenshot(region=(x[1] + move , y[1], 1, 1)).getcolors()[0][1][0]
        u = pyautogui.screenshot(region=(x[1], y[1] - move, 1, 1)).getcolors()[0][1][0]
        d = pyautogui.screenshot(region=(x[1], y[1] + move, 1, 1)).getcolors()[0][1][0]
        ru = pyautogui.screenshot(region=(x[1] + move , y[1] - move, 1, 1)).getcolors()[0][1][0]
        rd = pyautogui.screenshot(region=(x[1] + move , y[1] + move, 1, 1)).getcolors()[0][1][0]

        return [r, u, d, ru, rd]

    # top left
    elif x[0] == 1 and y[0] == 1:
        r = pyautogui.screenshot(region=(x[1] + move , y[1], 1, 1)).getcolors()[0][1][0]
        d = pyautogui.screenshot(region=(x[1], y[1] + move, 1, 1)).getcolors()[0][1][0]
        rd = pyautogui.screenshot(region=(x[1] + move , y[1] + move, 1, 1)).getcolors()[0][1][0]

        return [r, d, rd]
     
    # top right
    elif x[0] == 1 and y[0] == 1:
        l = pyautogui.screenshot(region=(x[1] - move , y[1], 1, 1)).getcolors()[0][1][0]
        d = pyautogui.screenshot(region=(x[1], y[1] + move, 1, 1)).getcolors()[0][1][0]
        ld = pyautogui.screenshot(region=(x[1] - move , y[1] + move, 1, 1)).getcolors()[0][1][0]
        
        return [l, d, ld]

    # bottom left
    elif x[0] == 1 and y[0] == 1:
        r = pyautogui.screenshot(region=(x[1] + move , y[1], 1, 1)).getcolors()[0][1][0]
        u = pyautogui.screenshot(region=(x[1], y[1] - move, 1, 1)).getcolors()[0][1][0]
        ru = pyautogui.screenshot(region=(x[1] + move , y[1] - move, 1, 1)).getcolors()[0][1][0]

        return [r, u, ru]

    # bottom right
    elif x[0] == 1 and y[0] == 1:
        l = pyautogui.screenshot(region=(x[1] - move , y[1], 1, 1)).getcolors()[0][1][0]
        u = pyautogui.screenshot(region=(x[1], y[1] - move, 1, 1)).getcolors()[0][1][0]
        lu = pyautogui.screenshot(region=(x[1] - move , y[1] - move, 1, 1)).getcolors()[0][1][0]

        return [l, u, lu]


board = [['' for i in range(9)] for i in range(9)]

#print(board)

ones = list(pyautogui.locateAllOnScreen('one.png'))

for coors in ones:
    x = coors[0]

    if x < 820:
        x = (1, 801)
    elif x < 862:
        x = (2, 843)
    elif x < 904:
        x = (3,885)
    elif x < 946:
        x = (4,927)
    elif x < 988:
        x = (5,969)
    elif x < 1030:
        x = (6,1011)
    elif x < 1072:
        x = (7,1095)
    elif x < 1114:
        x = (8,1053)
    else:
        x = (9,1137)
    

    y = coors[1]

    if y < 544:
        y = (1,525)
    elif y < 586:
        y = (2,567)
    elif y < 628:
        y = (3,609)
    elif y < 670:
        y = (4,651)
    elif y < 712:
        y = (5,693)
    elif y < 754:
        y = (6,735)
    elif y < 796:
        y = (7,777)
    elif y < 838:
        y = (8,819)
    else:
        y = (9,861)

    neighbors = get_neighbors(x, y)
    print(x, y, neighbors)
    
