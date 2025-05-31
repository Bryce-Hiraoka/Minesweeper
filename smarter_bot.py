import pyautogui
import random
from PIL import Image

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
        for i in self.neighbors:
            if isinstance(self.neighbors[i], Box):
                if self.neighbors[i].value == "unknown":
                    potential_bombs += 1
                    bomb_coordinates.append((self.neighbors[i].pixel_x, self.neighbors[i].pixel_y))
                if self.neighbors[i].value == "bomb":
                    bomb_neighbor = True
        
        return (bomb_neighbor, bomb_coordinates)
        
# desinguishes between an unknown box and a known box with a value of 0 (no number and not a bomb)
def neighbor_check(neighbors, current_box):
    inc = 20

    if "right" in neighbors and not isinstance(neighbors["right"], Box) and check_grey(neighbors["right"]):
        color = pyautogui.screenshot(region=(current_box.pixel_x + inc , current_box.pixel_y, 1, 1)).getcolors()[0][1][0]
        if color == 255:
            value = "unknown"
        else:
            value = 0
        neighbors["right"] = Box(current_box.board_x + 1, current_box.board_y, current_box.right, current_box.pixel_y, value)

    if "left" in neighbors and not isinstance(neighbors["left"], Box) and check_grey(neighbors["left"]):
        color = pyautogui.screenshot(region=(current_box.pixel_x - inc , current_box.pixel_y, 1, 1)).getcolors()[0][1][0]
        if color == 128:
            value = "unknown"
        else:
            value = 0
        neighbors["left"] = Box(current_box.board_x - 1, current_box.board_y, current_box.left, current_box.pixel_y, value)

    if "up" in neighbors and not isinstance(neighbors["up"], Box) and check_grey(neighbors["up"]):
        color = pyautogui.screenshot(region=(current_box.pixel_x, current_box.pixel_y - inc, 1, 1)).getcolors()[0][1][0]
        if color == 128:
            value = "unknown"
        else:
            value = 0
        neighbors["up"] = Box(current_box.board_x, current_box.board_y - 1, current_box.pixel_x, current_box.up, value)

    if "down" in neighbors and not isinstance(neighbors["down"], Box) and check_grey(neighbors["down"]):
        color = pyautogui.screenshot(region=(current_box.pixel_x, current_box.pixel_y + inc, 1, 1)).getcolors()[0][1][0]
        if color == 255:
            value = "unknown"
        else:
            value = 0
        neighbors["down"] = Box(current_box.board_x, current_box.board_y + 1, current_box.pixel_x, current_box.down, value)

    if "rightup" in neighbors and not isinstance(neighbors["rightup"], Box) and check_grey(neighbors["rightup"]):
        color = pyautogui.screenshot(region=(current_box.pixel_x + inc , current_box.pixel_y - inc, 1, 1)).getcolors()[0][1][0]
        if color == 255 or color == 128:
            value = "unknown"
        else:
            value = 0
        neighbors["rightup"] = Box(current_box.board_x + 1, current_box.board_y - 1, current_box.right, current_box.up, value)

    if "rightdown" in neighbors and not isinstance(neighbors["rightdown"], Box) and check_grey(neighbors["rightdown"]):
        color = pyautogui.screenshot(region=(current_box.pixel_x + inc , current_box.pixel_y + inc, 1, 1)).getcolors()[0][1][0]
        if color == 255 or color == 128:
            value = "unknown"
        else:
            value = 0
        neighbors["rightdown"] = Box(current_box.board_x + 1, current_box.board_y + 1 , current_box.right, current_box.down, value)
          
    if "leftup" in neighbors and not isinstance(neighbors["leftup"], Box) and check_grey(neighbors["leftup"]):
        color = pyautogui.screenshot(region=(current_box.pixel_x - inc , current_box.pixel_y - inc, 1, 1)).getcolors()[0][1][0]
        if color == 255 or color == 128:
            value = "unknown"
        else:
            value = 0
        neighbors["leftup"] = Box(current_box.board_x - 1, current_box.board_y - 1, current_box.left, current_box.up, value)

    if "leftdown" in neighbors and not isinstance(neighbors["leftdown"], Box) and check_grey(neighbors["leftdown"]):
        color = pyautogui.screenshot(region=(current_box.pixel_x - inc , current_box.pixel_y + inc, 1, 1)).getcolors()[0][1][0]
        print(color, "here is color")
        if color == 255 or color == 128:
            print('unknown found at, ', current_box.pixel_x - inc , current_box.pixel_y + inc)
            value = "unknown"
        else:
            value = 0
        neighbors["leftdown"] = Box(current_box.board_x - 1, current_box.board_y + 1, current_box.left, current_box.down, value)

    return neighbors

# checks if a box is unknown or nothing based on pixel color of corner
def check_grey(color):
    print(color)
    if color[0] == 198:
        return True
    
    return False

# checks to see if a box is a flagged bomb or not
def check_bomb(color):
    if color[0] == 0 and color[1] == 0 and color[2] == 0:
        return True
    
    return False

# checks all neighbors or being a flagged bomb, grey box (unknown or value of 0), or number box
def set_neighbors(neighbors, curr_box):
    res = {}

    for direction in neighbors:
        match direction:
            case "right":
                pixel = pyautogui.screenshot(region=(curr_box.right, curr_box.pixel_y, 1, 1)).getcolors()[0][1]
                if check_bomb(pixel):
                    print("bomb found")
                    res["right"] = Box(curr_box.board_x + 1, curr_box.board_y, curr_box.right, curr_box.pixel_y, "bomb")
                else:
                    res["right"] = pixel
            case "left":
                print('here', curr_box.pixel_x , curr_box.pixel_y, curr_box.board_x, curr_box.board_y)
                pixel = pyautogui.screenshot(region=(curr_box.left , curr_box.pixel_y, 1, 1)).getcolors()[0][1]
                if check_bomb(pixel):
                    print("bomb found")
                    res["left"] = Box(curr_box.board_x + 1, curr_box.board_y, curr_box.left, curr_box.pixel_y, "bomb")
                else:
                    res["left"] = pixel
            case "up":
                pixel = pyautogui.screenshot(region=(curr_box.pixel_x, curr_box.up, 1, 1)).getcolors()[0][1]
                if check_bomb(pixel):
                    res["up"] = Box(curr_box.board_x, curr_box.board_y - 1, curr_box.pixel_x, curr_box.up, "bomb")
                else:
                    res["up"] = pixel
            case "down":
                pixel = pyautogui.screenshot(region=(curr_box.pixel_x, curr_box.down, 1, 1)).getcolors()[0][1]
                if check_bomb(pixel):
                    res["down"] = Box(curr_box.board_x, curr_box.board_y + 1, curr_box.pixel_x, curr_box.down, "bomb")
                else:
                    res["down"] = pixel
            case "rightup":
                pixel = pyautogui.screenshot(region=(curr_box.right , curr_box.up, 1, 1)).getcolors()[0][1]
                if check_bomb(pixel):
                    res["rightup"] = Box(curr_box.board_x + 1, curr_box.board_y - 1, curr_box.right, curr_box.up, "bomb")
                else:
                    res["rightup"] = pixel
            case "rightdown":
                pixel = pyautogui.screenshot(region=(curr_box.right, curr_box.down, 1, 1)).getcolors()[0][1]
                if check_bomb(pixel):
                    res["rightdown"] = Box(curr_box.board_x + 1, curr_box.board_y + 1, curr_box.right, curr_box.down, "bomb")
                else:
                    res["rightdown"] = pixel
            case "leftup":
                pixel = pyautogui.screenshot(region=(curr_box.left, curr_box.up, 1, 1)).getcolors()[0][1]
                if check_bomb(pixel):
                    res["leftup"] = Box(curr_box.board_x - 1, curr_box.board_y - 1, curr_box.left, curr_box.up, "bomb")
                else:
                    res["leftup"] = pixel
            case "leftdown":
                pixel = pyautogui.screenshot(region=(curr_box.left, curr_box.down, 1, 1)).getcolors()[0][1]
                if check_bomb(pixel):
                    res["leftdown"] = Box(curr_box.board_x - 1, curr_box.board_y + 1, curr_box.left, curr_box.down, "bomb")
                else:
                    res["leftdown"] = pixel

    return res



# gets center pixel of touching boxes and stores in dictionary with rgb values
def get_neighbors(curr_box):
    neighbors = {}

    # middle blocks
    if curr_box.board_x > 1 and curr_box.board_x < 9 and curr_box.board_y > 1 and curr_box.board_y < 9:

        # COMBINE THESE TOGEATHER AT SOME POINT 
        neighbors = set_neighbors(["right", "left", "up", "down", "rightup", "rightdown", "leftup", "leftdown"], curr_box)
        new_neighbors = neighbor_check(neighbors, curr_box)
        return (new_neighbors)

    # top row
    elif curr_box.board_x > 1 and curr_box.board_x < 9 and curr_box.board_y == 1:
        neighbors = set_neighbors(["right", "left", "down", "rightdown", "leftdown"], curr_box)
        new_neighbors = neighbor_check(neighbors, curr_box)
        return (new_neighbors)

    # bottom row
    elif curr_box.board_x > 1 and curr_box.board_x < 9 and curr_box.board_y == 9:
        neighbors = set_neighbors(["right", "left", "up", "rightup", "leftup"], curr_box)
        new_neighbors = neighbor_check(neighbors, curr_box)
        return (new_neighbors)
    
    # left row
    elif curr_box.board_x == 9 and curr_box.board_y > 1 and curr_box.board_y < 9:
        neighbors = set_neighbors(["left", "up", "down", "leftup", "leftdown"], curr_box)
        new_neighbors = neighbor_check(neighbors, curr_box)
        return (new_neighbors)

    # right row
    elif curr_box.board_x == 1 and curr_box.board_y > 1 and curr_box.board_y < 9:
        neighbors = set_neighbors(["right", "up", "down", "rightup", "rightdown"], curr_box)
        new_neighbors = neighbor_check(neighbors, curr_box)
        return (new_neighbors)

    # top left
    elif curr_box.board_x == 1 and curr_box.board_y == 1:
        neighbors = set_neighbors(["right", "down", "rightdown"], curr_box)
        new_neighbors = neighbor_check(neighbors, curr_box)
        return (new_neighbors)
     
    # top right
    elif curr_box.board_x == 1 and curr_box.board_y == 1:    
        neighbors = set_neighbors(["left", "down", "leftdown"], curr_box)
        new_neighbors = neighbor_check(neighbors, curr_box)
        return(new_neighbors)

    # bottom left
    elif curr_box.board_x == 1 and curr_box.board_y == 1:
        neighbors = set_neighbors(["right", "up", "rightup"], curr_box)
        new_neighbors = neighbor_check(neighbors, curr_box)
        return (new_neighbors)

    # bottom right
    elif curr_box.board_x == 1 and curr_box.board_y == 1:
        neighbors = set_neighbors(["left", "up", "leftup"], curr_box)
        new_neighbors = neighbor_check(neighbors, curr_box)
        return (new_neighbors)


# board = [['' for i in range(9)] for i in range(9)]

# finds all '1' boxes on screen and saves them as coordinates
ones = list(pyautogui.locateAllOnScreen('States/one.png'))

# uses the coordinates of picture to determine which curr_box each '1' is in
# stores x y corrdinates as a tuple (board coordinate, pixel coordinate)
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

    # change get neighbors later to be hidden
    current_one = One(x[0], y[0], x[1], y[1], 1)
    print(current_one.board_x, current_one.board_y)
    current_one.neighbors = get_neighbors(current_one)
    print(current_one.neighbors)
    bomb_neighbor, pot_bombs = current_one.check_complete()

    if bomb_neighbor:
        for coor in pot_bombs:
            print('left click', coor[0], coor[1])
            pyautogui.click(x=coor[0], y=coor[1], button='left')
    elif len(pot_bombs) == 1:
        print("right click", pot_bombs[0][0], pot_bombs[0][1])
        pyautogui.click(x=pot_bombs[0][0], y=pot_bombs[0][1], button='right')
    


        

    
