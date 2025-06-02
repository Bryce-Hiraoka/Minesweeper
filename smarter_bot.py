import pyautogui
import random
from PIL import Image
import time

# Things to fix: 
# Down Left pixel inc is wrong and needs to be increased to 24
# Combine set_neighbors and check_neighbors
# Down and Left and Up might also be effected by tbe inc issue
# Bug where it sometimes thinks that already known squares are unknown and tries to click (should be fixed once checking is added) -- low prio

# Add:
# 2 and 3 detection and solving
# Guessing when no more guarenteed moves
# Check if a square is already known
# Don't check the same numbers over and over
# Check if game has been won
# Maybe hide neighbor call altogether

# x = 782 - 820, 824 - 862 , 866 - 904, 908 - 946, 950 - 988, 992 - 1030, 1034 - 1072, 1076 - 1114, 1118 - 1156
# y = 506 - 544, 548 - 586, 590 - 628, 632 - 670, 674 - 712, 716 - 754, 758 - 796, 800 - 838, 842 - 880 

# middle x = 801, 843, 885, 927, 969, 1011, 1053, 1095, 1137
# middle y = 525, 567, 609, 651, 693, 735, 777, 819, 861

# grey is 29 px long

# class that represents all boxes on the board
class Box:
    def __init__(self, board_x, board_y, pixel_x, pixel_y, value):

        # coordinates of Box in pixel and graph
        self.board_x = board_x
        self.board_y = board_y
        self.pixel_x = pixel_x
        self.pixel_y = pixel_y
        self.value = value

        # center pixel coordinates of box neighbors
        self.right = pixel_x + 42
        self.left = pixel_x - 42
        self.up = pixel_y - 42
        self.down = pixel_y + 42

        # stores boxes neighbors
        self.neighbors = {}

# class for boxes where known value is 1
class One(Box):
    def __init__(self, board_x, board_y, pixel_x, pixel_y, value):

        super().__init__(board_x, board_y, pixel_x, pixel_y, value)

    # method to check if a box is completed 
    # completed -> all but 1 neighbor box is known or a neighbor box is a know bomb
    def check_complete(self):
        potential_bombs = 0
        bomb_coordinates = []
        bomb_neighbor = False
        num_bombs = 0
        for i in self.neighbors:
            if isinstance(self.neighbors[i], Box):
                if self.neighbors[i].value == "unknown":
                    potential_bombs += 1
                    bomb_coordinates.append((self.neighbors[i].pixel_x, self.neighbors[i].pixel_y))
                if self.neighbors[i].value == "bomb":
                    bomb_neighbor = True
                    num_bombs = 1
        
        return (bomb_neighbor, bomb_coordinates, num_bombs)

class Two(Box):
    def __init__(self, board_x, board_y, pixel_x, pixel_y, value):

        super().__init__(board_x, board_y, pixel_x, pixel_y, value)

    def check_complete(self):

        potential_bombs = 0
        bomb_coordinates = []
        bomb_neighbor = False
        num_bombs = 0

        for i in self.neighbors:
            if isinstance(self.neighbors[i], Box):
                if self.neighbors[i].value == "unknown":
                    potential_bombs += 1
                    bomb_coordinates.append((self.neighbors[i].pixel_x, self.neighbors[i].pixel_y))
                if self.neighbors[i].value == "bomb":
                    num_bombs += 1
                    if num_bombs == 2:
                        bomb_neighbor = True
        
        return (bomb_neighbor, bomb_coordinates, num_bombs)
    
class Three(Box):
    def __init__(self, board_x, board_y, pixel_x, pixel_y, value):

        super().__init__(board_x, board_y, pixel_x, pixel_y, value)

    def check_complete(self):

        potential_bombs = 0
        bomb_coordinates = []
        bomb_neighbor = False
        num_bombs = 0

        for i in self.neighbors:
            if isinstance(self.neighbors[i], Box):
                if self.neighbors[i].value == "unknown":
                    potential_bombs += 1
                    bomb_coordinates.append((self.neighbors[i].pixel_x, self.neighbors[i].pixel_y))
                if self.neighbors[i].value == "bomb":
                    num_bombs += 1
                    if num_bombs == 3:
                        bomb_neighbor = True
        
        return (bomb_neighbor, bomb_coordinates, num_bombs)

        
# desinguishes between an unknown box and a known box with a value of 0 (no number and not a bomb)


# checks if a box is unknown or nothing based on pixel color of corner
def check_grey(color):
    #print(color)
    if color[0] == 198:
        return True
    
    return False

# checks to see if a box is a flagged bomb or not
def check_bomb(color):
    if color[0] == 0 and color[1] == 0 and color[2] == 0:
        return True
    
    return False

def get_value(x, y):
    value = ""
    pixel = pyautogui.screenshot(region=(x, y, 1, 1)).getcolors()[0][1]
    if pixel[0] == 198:
        color = pyautogui.screenshot(region=(x , y - 19, 1, 1)).getcolors()[0][1][0]
        if color == 255:
            value = "unknown"
        else:
            value = 0
    elif check_bomb(pixel):
        value = "bomb"
    else:
        #change this later
        value = "number"
    
    return value

# checks all neighbors or being a flagged bomb, grey box (unknown or value of 0), or number box
def set_neighbors(neighbors, curr_box):
    res = {}

    for direction in neighbors:
        match direction:
            case "right":
                value = get_value(curr_box.right, curr_box.pixel_y)
                res["right"] = Box(curr_box.board_x + 1, curr_box.board_y, curr_box.right, curr_box.pixel_y, value)

            case "left":
                value = get_value(curr_box.left, curr_box.pixel_y)
                res["left"] = Box(curr_box.board_x - 1, curr_box.board_y, curr_box.left, curr_box.pixel_y, value)

            case "up":
                value = get_value(curr_box.pixel_x, curr_box.up)
                res["up"] = Box(curr_box.board_x, curr_box.board_y - 1, curr_box.pixel_x, curr_box.up, value)

            case "down":
                value = get_value(curr_box.pixel_x, curr_box.down)
                res["down"] = Box(curr_box.board_x, curr_box.board_y + 1, curr_box.pixel_x, curr_box.down, value)

            case "rightup":
                value = get_value(curr_box.right, curr_box.up)
                res["rightup"] = Box(curr_box.board_x + 1, curr_box.board_y - 1, curr_box.right, curr_box.up, value)

            case "rightdown":
                value = get_value(curr_box.right, curr_box.down)
                res["rightdown"] = Box(curr_box.board_x + 1, curr_box.board_y + 1, curr_box.right, curr_box.down, value)

            case "leftup":
                value = get_value(curr_box.left, curr_box.up)
                res["leftup"] = Box(curr_box.board_x - 1, curr_box.board_y - 1, curr_box.left, curr_box.up, value)

            case "leftdown":
                value = get_value(curr_box.left, curr_box.down)
                res["leftdown"] = Box(curr_box.board_x - 1, curr_box.board_y + 1, curr_box.left, curr_box.down, value)

    return res



# gets center pixel of touching boxes and stores in dictionary with rgb values
def get_neighbors(curr_box):
    neighbors = {}

    # middle blocks
    if curr_box.board_x > 1 and curr_box.board_x < 9 and curr_box.board_y > 1 and curr_box.board_y < 9:
        # COMBINE THESE TOGEATHER AT SOME POINT 
        return set_neighbors(["right", "left", "up", "down", "rightup", "rightdown", "leftup", "leftdown"], curr_box)

    # top row
    elif curr_box.board_x > 1 and curr_box.board_x < 9 and curr_box.board_y == 1:
        return set_neighbors(["right", "left", "down", "rightdown", "leftdown"], curr_box)

    # bottom row
    elif curr_box.board_x > 1 and curr_box.board_x < 9 and curr_box.board_y == 9:
        return set_neighbors(["right", "left", "up", "rightup", "leftup"], curr_box)
    
    # left row
    elif curr_box.board_x == 9 and curr_box.board_y > 1 and curr_box.board_y < 9:
        return set_neighbors(["left", "up", "down", "leftup", "leftdown"], curr_box)

    # right row
    elif curr_box.board_x == 1 and curr_box.board_y > 1 and curr_box.board_y < 9:
        return set_neighbors(["right", "up", "down", "rightup", "rightdown"], curr_box)

    # top left
    elif curr_box.board_x == 1 and curr_box.board_y == 1:
        return set_neighbors(["right", "down", "rightdown"], curr_box)

    # top right
    elif curr_box.board_x == 9 and curr_box.board_y == 1:    
        return set_neighbors(["left", "down", "leftdown"], curr_box)

    # bottom left
    elif curr_box.board_x == 1 and curr_box.board_y == 9:
        return set_neighbors(["right", "up", "rightup"], curr_box)


    # bottom right
    elif curr_box.board_x == 9 and curr_box.board_y == 9:
        return set_neighbors(["left", "up", "leftup"], curr_box)

# board = [['' for i in range(9)] for i in range(9)]

pyautogui.click(x=801, y=522)
start_time = time.time()

for _ in range(100):

    progress = False
    win = False

    time_limit = 120

    if time.time() - start_time > time_limit:
        print("timeout")
        break

    for i in [1, 2, 3]:
        if i == 1:
            # finds all '1' boxes on screen and saves them as coordinates
            try:
                number = list(pyautogui.locateAllOnScreen('States/one.png'))
            except:
                continue
        elif i == 2:
            # finds all '2' boxes on screen and saves them as coordinates
            try:
                number = list(pyautogui.locateAllOnScreen('States/two.png'))
            except:
                continue
        elif i == 3:
            # finds all '3' boxes on screen and saves them as coordinates
            try:
                number = list(pyautogui.locateAllOnScreen('States/three.png'))
            except:
                continue

        # uses the coordinates of picture to determine which curr_box each '1' is in
        # stores x y corrdinates as a tuple (board coordinate, pixel coordinate)
        for coors in number:
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
                x = (7,1053)
            elif x < 1114:
                x = (8,1095)
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

            # change to have the boxes store thier number value so no need if else statements
            if i == 1:
                current = One(x[0], y[0], x[1], y[1], 1)
            elif i == 2:
                current = Two(x[0], y[0], x[1], y[1], 1)
            else:
                current = Three(x[0], y[0], x[1], y[1], 1)

            print("Board Coordinates", current.board_x, current.board_y, "Pixel Coordinates", current.pixel_x, current.pixel_y)
            current.neighbors = get_neighbors(current)
            
            '''
            for i in current_one.neighbors:
                print(i, current_one.neighbors[i].value)
            '''

            #print(current.neighbors)
            bomb_neighbor, pot_bombs, num_bombs = current.check_complete()

            if bomb_neighbor:
                for coor in pot_bombs:
                    #print('left click', coor[0], coor[1])
                    pyautogui.click(x=coor[0], y=coor[1], button='left')
                    progress = True
            elif len(pot_bombs) + num_bombs == i:
                #print("right click", pot_bombs[0][0], pot_bombs[0][1])
                for bomb in pot_bombs:
                    pyautogui.click(x=bomb[0], y=bomb[1], button='right')
                    progress = True

        # pyautogui to screenshot specific pixel to determine state of game (loss, win, neutral)
        pixel = pyautogui.screenshot(region=(958,423, 1, 1)).getcolors()[0][1][0]
    
        # check for game loss
        if pixel == 53:
            pyautogui.click(x=800, y=315)
            pyautogui.click(x=801, y=522)

        
        # check for game win
        if pixel == 181:
            win = True
            break
            print("Congrats on finally winning")

            
    if win:
        break
    # if stuck click a random coordinate
    # will change later to be better
    if not progress:
        rand_X = random.randint(780, 1150)
        rand_Y = random.randint(510, 870)
        # click at random coordinate
        pyautogui.click(x=rand_X, y=rand_Y, button='left')


            


            

        
