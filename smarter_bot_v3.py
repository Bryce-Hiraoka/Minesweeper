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

# x = 1007 - 1041, 1042 - 1076, 1077 - 1111, 1112 - 1146, 1147 - 1181, 1182 - 1216, 1217 - 1251, 1252 - 1286
# y = 677 - 711, 712 - 746, 747 - 781, 782 - 816, 817 - 851, 852 - 886, 887 - 921, 922 - 956

# middle x = 1055, 1119, 1183, 1247, 1311, 1375, 1439, 1503
# middle y = 471, 535, 599, 663, 727, 791, 855, 919

# class that represents all boxes on the board

x_coordinates = [1055, 1119, 1183, 1247, 1311, 1375, 1439, 1503]
y_coordinates = [471, 535, 599, 663, 727, 791, 855, 919]
pxl_to_edg = 32

class Box:
    def __init__(self, board_x, board_y, pixel_x, pixel_y, value):

        # coordinates of Box in pixel and graph
        self.board_x = board_x
        self.board_y = board_y
        self.pixel_x = pixel_x
        self.pixel_y = pixel_y
        self.value = value

        # center pixel coordinates of box neighbors
        self.right = pixel_x + 64
        self.left = pixel_x - 64
        self.up = pixel_y - 64
        self.down = pixel_y + 64

        # stores boxes neighbors
        self.neighbors = {}

# class for boxes where known value is 1
class One(Box):
    def __init__(self, board_x, board_y, pixel_x, pixel_y, value):

        super().__init__(board_x, board_y, pixel_x, pixel_y, value)

    # method to check if a box is completed 
    # completed -> all but 1 neighbor box is known or a neighbor box is a know bomb
    def check_complete(self):
        print("checking one")
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
        print("wrong")
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
        print("wrong")
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
    if color[0] == 5 and color[1] == 5 and color[2] == 5:
        return True
    return False

def get_value(x, y):
    value = ""
    color_neigh_center = pyautogui.screenshot(region=(x, y, 1, 1)).getcolors()[0][1]
    print(color_neigh_center, "pixel color")
    if color_neigh_center[0] == 189:
        color = pyautogui.screenshot(region=(x, y - 27, 1, 1)).getcolors()[0][1][0]
        if color == 255:
            value = "unknown"
        else:
            value = 0
    elif color_neigh_center[2] == 255:
        color = pyautogui.screenshot(region=(x, y - 15, 1, 1)).getcolors()[0][1]
        print(color, "bomb color")
        if check_bomb(color):
            print("here")
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
                #print("right")
                value = get_value(curr_box.right, curr_box.pixel_y)
                res["right"] = Box(curr_box.board_x + 1, curr_box.board_y, curr_box.right, curr_box.pixel_y, value)

            case "left":
                #print("left")                
                value = get_value(curr_box.left, curr_box.pixel_y)
                res["left"] = Box(curr_box.board_x - 1, curr_box.board_y, curr_box.left, curr_box.pixel_y, value)

            case "up":
                #print("up")                
                value = get_value(curr_box.pixel_x, curr_box.up)
                res["up"] = Box(curr_box.board_x, curr_box.board_y - 1, curr_box.pixel_x, curr_box.up, value)

            case "down":
                #print("down")                                
                value = get_value(curr_box.pixel_x, curr_box.down)
                res["down"] = Box(curr_box.board_x, curr_box.board_y + 1, curr_box.pixel_x, curr_box.down, value)

            case "rightup":
                #print("rightup")                
                value = get_value(curr_box.right, curr_box.up)
                res["rightup"] = Box(curr_box.board_x + 1, curr_box.board_y - 1, curr_box.right, curr_box.up, value)

            case "rightdown":
                #print("rightdown")                                
                value = get_value(curr_box.right, curr_box.down)
                res["rightdown"] = Box(curr_box.board_x + 1, curr_box.board_y + 1, curr_box.right, curr_box.down, value)

            case "leftup":
                #print("leftup")                                
                value = get_value(curr_box.left, curr_box.up)
                res["leftup"] = Box(curr_box.board_x - 1, curr_box.board_y - 1, curr_box.left, curr_box.up, value)

            case "leftdown":
                #print("leftdown")                                
                value = get_value(curr_box.left, curr_box.down)
                res["leftdown"] = Box(curr_box.board_x - 1, curr_box.board_y + 1, curr_box.left, curr_box.down, value)

    return res


# gets center pixel of touching boxes and stores in dictionary with rgb values
def get_neighbors(curr_box):
    print(curr_box.board_x, curr_box.board_y)
    neighbors = {}

    # middle blocks
    if curr_box.board_x > 1 and curr_box.board_x < 8 and curr_box.board_y > 1 and curr_box.board_y < 8:
        # COMBINE THESE TOGEATHER AT SOME POINT 
        return set_neighbors(["right", "left", "up", "down", "rightup", "rightdown", "leftup", "leftdown"], curr_box)

    # top row
    elif curr_box.board_x > 1 and curr_box.board_x < 8 and curr_box.board_y == 1:
        return set_neighbors(["right", "left", "down", "rightdown", "leftdown"], curr_box)

    # bottom row
    elif curr_box.board_x > 1 and curr_box.board_x < 8 and curr_box.board_y == 8:
        return set_neighbors(["right", "left", "up", "rightup", "leftup"], curr_box)
    
    # left row
    elif curr_box.board_x == 8 and curr_box.board_y > 1 and curr_box.board_y < 8:
        return set_neighbors(["left", "up", "down", "leftup", "leftdown"], curr_box)

    # right row
    elif curr_box.board_x == 1 and curr_box.board_y > 1 and curr_box.board_y < 8:
        return set_neighbors(["right", "up", "down", "rightup", "rightdown"], curr_box)

    # top left
    elif curr_box.board_x == 1 and curr_box.board_y == 1:
        return set_neighbors(["right", "down", "rightdown"], curr_box)

    # top right
    elif curr_box.board_x == 8 and curr_box.board_y == 1:    
        return set_neighbors(["left", "down", "leftdown"], curr_box)

    # bottom left
    elif curr_box.board_x == 1 and curr_box.board_y == 8:
        return set_neighbors(["right", "up", "rightup"], curr_box)


    # bottom right
    elif curr_box.board_x == 8 and curr_box.board_y == 8:
        return set_neighbors(["left", "up", "leftup"], curr_box)

# board = [['' for i in range(9)] for i in range(9)]

pyautogui.click(x=1057, y=454)


for loop in [1, 2, 3]:
    if loop == 1:
        # finds all '1' boxes on screen and saves them as coordinates
        try:
            print('1')
            number = list(pyautogui.locateAllOnScreen('States/one.png'))
        except:
            continue
    elif loop == 2:
        # finds all '2' boxes on screen and saves them as coordinates
        try:
            print('2')
            number = list(pyautogui.locateAllOnScreen('States/two.png'))
        except:
            continue
    elif loop == 3:
        # finds all '3' boxes on screen and saves them as coordinates
        try:
            print('3')
            number = list(pyautogui.locateAllOnScreen('States/three.png'))
        except:
            continue

    for coors in number:
        x = coors[0]

        if x < x_coordinates[0] + pxl_to_edg:
            x = (1, x_coordinates[0])
        elif x < x_coordinates[1] + pxl_to_edg:
            x = (2, x_coordinates[1])
        elif x < x_coordinates[2] + pxl_to_edg:
            x = (3, x_coordinates[2])
        elif x < x_coordinates[3] + pxl_to_edg:
            x = (4, x_coordinates[3])
        elif x < x_coordinates[4] + pxl_to_edg:
            x = (5, x_coordinates[4])
        elif x < x_coordinates[5] + pxl_to_edg:
            x = (6, x_coordinates[5])
        elif x < x_coordinates[6] + pxl_to_edg:
            x = (7, x_coordinates[6])
        else:
            x = (8, x_coordinates[7])

        y = coors[1]

        if y < y_coordinates[0] + pxl_to_edg:
            y = (1, y_coordinates[0])
        elif y < y_coordinates[1] + pxl_to_edg:
            y = (2, y_coordinates[1])
        elif y < y_coordinates[2] + pxl_to_edg:
            y = (3, y_coordinates[2])
        elif y < y_coordinates[3] + pxl_to_edg:
            y = (4, y_coordinates[3])
        elif y < y_coordinates[4] + pxl_to_edg:
            y = (5, y_coordinates[4]) 
        elif y < y_coordinates[5] + pxl_to_edg:
            y = (6, y_coordinates[5])
        elif y < y_coordinates[6] + pxl_to_edg:
            y = (7, y_coordinates[6])
        else:
            y = (8, y_coordinates[7])    
        
        if loop == 1:
            current = One(x[0], y[0], x[1], y[1], 1)
        elif loop == 2:
            current = Two(x[0], y[0], x[1], y[1], 1)
        else:
            current = Three(x[0], y[0], x[1], y[1], 1)
        
        current.neighbors = get_neighbors(current)

        print (x, y)
        for i in current.neighbors:
            print(i, current.neighbors[i].value)
                

        bomb_neighbor, pot_bombs, num_bombs = current.check_complete()

        print(bomb_neighbor)

        if bomb_neighbor:
            for coor in pot_bombs:
                print('left click', coor[0], coor[1])
                pyautogui.click(x=coor[0], y=coor[1], button='left')
                progress = True
        elif len(pot_bombs) + num_bombs == loop:
            print("right click", pot_bombs[0][0], pot_bombs[0][1])
            for bomb in pot_bombs:
                pyautogui.click(x=bomb[0], y=bomb[1], button='right')
                progress = True


                


            


            

        
