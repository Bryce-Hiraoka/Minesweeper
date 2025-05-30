import pyautogui
import random
from PIL import Image

# x = 782 - 820, 824 - 862 , 866 - 904, 908 - 946, 950 - 988, 992 - 1030, 1034 - 1072, 1076 - 1114, 1118 - 1156
# y = 506 - 544, 548 - 586, 590 - 628, 632 - 670, 674 - 712, 716 - 754, 758 - 796, 800 - 838, 842 - 880 

# middle x = 801, 843, 885, 927, 969, 1011, 1053, 1095, 1137
# middle y = 525, 567, 609, 651, 693, 735, 777, 819, 861

# grey is 29 px long

class Box:
    def __init__(self, board_x, board_y, pixel_x, pixel_y, value):
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

        self.neighbors = {}

class One(Box):
    def __init__(self, board_x, board_y, pixel_x, pixel_y, value):

        super().__init__(board_x, board_y, pixel_x, pixel_y, value)

    def check_complete(self):
        potential_bombs = 0
        bomb_coordinates = ()
        for i in self.neighbors:
            if isinstance(self.neighbors[i], Box) and self.neighbors[i].value == "unknown":
                potential_bombs += 1
                print(self.neighbors[i].board_x, self.neighbors[i].board_y)
                bomb_coordinates = (self.neighbors[i].pixel_x, self.neighbors[i].pixel_y)
            
            if potential_bombs > 1:
                return False
        
        if potential_bombs != 1:
            return False
        else:
            return bomb_coordinates
        
        
# checks if the current box's neighbors are known or unknown
def neighbor_check(neighbors, current_box):
    inc = 20

    if "right" in neighbors and check_grey(neighbors["right"]):
        color = pyautogui.screenshot(region=(current_box.pixel_x + inc , current_box.pixel_y, 1, 1)).getcolors()[0][1][0]
        if color == 255:
            value = "unknown"
        else:
            value = 0
        neighbors["right"] = Box(current_box.board_x + 1, current_box.board_y, current_box.right, current_box.pixel_y, value)

    if "left" in neighbors and check_grey(neighbors["left"]):
        color = pyautogui.screenshot(region=(current_box.pixel_x - inc , current_box.pixel_y, 1, 1)).getcolors()[0][1][0]
        if color == 255:
            value = "unknown"
        else:
            value = 0
        neighbors["left"] = Box(current_box.board_x - 1, current_box.board_y, current_box.left, current_box.pixel_y, value)

    if "up" in neighbors and check_grey(neighbors["up"]):
        color = pyautogui.screenshot(region=(current_box.pixel_x, current_box.pixel_y - inc, 1, 1)).getcolors()[0][1][0]
        if color == 255:
            value = "unknown"
        else:
            value = 0
        neighbors["up"] = Box(current_box.board_x, current_box.board_y - 1, current_box.pixel_x, current_box.up, value)

    if "down" in neighbors and check_grey(neighbors["down"]):
        color = pyautogui.screenshot(region=(current_box.pixel_x, current_box.pixel_y + inc, 1, 1)).getcolors()[0][1][0]
        if color == 255:
            value = "unknown"
        else:
            value = 0
        neighbors["down"] = Box(current_box.board_x, current_box.board_y + 1, current_box.pixel_x, current_box.down, value)

    if "rightup" in neighbors and check_grey(neighbors["rightup"]):
        color = pyautogui.screenshot(region=(current_box.pixel_x + inc , current_box.pixel_y - inc, 1, 1)).getcolors()[0][1][0]
        if color == 255:
            value = "unknown"
        else:
            value = 0
        neighbors["rightup"] = Box(current_box.board_x + 1, current_box.board_y - 1, current_box.right, current_box.up, value)

    if "rightdown" in neighbors and check_grey(neighbors["rightdown"]):
        color = pyautogui.screenshot(region=(current_box.pixel_x + inc , current_box.pixel_y + inc, 1, 1)).getcolors()[0][1][0]
        print(color)
        if color == 255:
            value = "unknown"
        else:
            value = 0
        neighbors["rightdown"] = Box(current_box.board_x + 1, current_box.board_y + 1 , current_box.right, current_box.down, value)
          
    if "leftup" in neighbors and check_grey(neighbors["leftup"]):
        color = pyautogui.screenshot(region=(current_box.pixel_x - inc , current_box.pixel_y - inc, 1, 1)).getcolors()[0][1][0]
        if color == 255:
            value = "unknown"
        else:
            value = 0
        neighbors["leftup"] = Box(current_box.board_x - 1, current_box.board_y - 1, current_box.left, current_box.up, value)

    if "leftdown" in neighbors and check_grey(neighbors["leftdown"]):
        color = pyautogui.screenshot(region=(current_box.pixel_x - inc , current_box.pixel_y + inc, 1, 1)).getcolors()[0][1][0]
        if color == 255:
            value = "unknown"
        else:
            value = 0
        neighbors["leftdown"] = Box(current_box.board_x - 1, current_box.board_y + 1, current_box.left, current_box.down, value)

    return neighbors

# checks if a box is unknown or nothing based on pixel color of corner
def check_grey(color):
    if color[0] == 198:
        return True
    
    return False


# gets center pixel of touching boxes and stores in dictionary with rgb values
def get_neighbors(box):
    neighbors = {}

    # Middle blocks
    if box.board_x > 1 and box.board_x < 9 and box.board_y > 1 and box.board_y < 9:
        neighbors["right"] = pyautogui.screenshot(region=(box.right, box.pixel_y, 1, 1)).getcolors()[0][1]
        neighbors["left"] = pyautogui.screenshot(region=(box.left , box.pixel_y, 1, 1)).getcolors()[0][1]
        neighbors["up"] = pyautogui.screenshot(region=(box.pixel_x, box.up, 1, 1)).getcolors()[0][1]
        neighbors["down"] = pyautogui.screenshot(region=(box.pixel_x, box.down, 1, 1)).getcolors()[0][1]
        neighbors["rightup"] = pyautogui.screenshot(region=(box.right , box.up, 1, 1)).getcolors()[0][1]
        neighbors["rightdown"] = pyautogui.screenshot(region=(box.right, box.down, 1, 1)).getcolors()[0][1]
        neighbors["leftup"] = pyautogui.screenshot(region=(box.left, box.up, 1, 1)).getcolors()[0][1]
        neighbors["leftdown"] = pyautogui.screenshot(region=(box.left, box.down, 1, 1)).getcolors()[0][1]

        new_neighbors = neighbor_check(neighbors, box)
        return (new_neighbors)

    # top row
    elif box.board_x > 1 and box.board_x < 9 and box.board_y == 1:
        neighbors["right"] = pyautogui.screenshot(region=(box.right, box.pixel_y, 1, 1)).getcolors()[0][1]
        neighbors["left"] = pyautogui.screenshot(region=(box.left , box.pixel_y, 1, 1)).getcolors()[0][1]
        neighbors["down"] = pyautogui.screenshot(region=(box.pixel_x, box.down, 1, 1)).getcolors()[0][1]
        neighbors["rightdown"] = pyautogui.screenshot(region=(box.right, box.down, 1, 1)).getcolors()[0][1]
        neighbors["leftdown"] = pyautogui.screenshot(region=(box.left, box.down, 1, 1)).getcolors()[0][1]

        new_neighbors = neighbor_check(neighbors, box)
        return (new_neighbors)

    # bottom row
    elif box.board_x > 1 and box.board_x < 9 and box.board_y == 9:
        neighbors["right"] = pyautogui.screenshot(region=(box.right, box.pixel_y, 1, 1)).getcolors()[0][1]
        neighbors["left"] = pyautogui.screenshot(region=(box.left , box.pixel_y, 1, 1)).getcolors()[0][1]
        neighbors["up"] = pyautogui.screenshot(region=(box.pixel_x, box.up, 1, 1)).getcolors()[0][1]
        neighbors["rightup"] = pyautogui.screenshot(region=(box.right , box.up, 1, 1)).getcolors()[0][1]
        neighbors["leftup"] = pyautogui.screenshot(region=(box.left, box.up, 1, 1)).getcolors()[0][1]

        new_neighbors = neighbor_check(neighbors, box)
        return (new_neighbors)
    
    # left row
    elif box.board_x == 9 and box.board_y > 1 and box.board_y < 9:
        neighbors["left"] = pyautogui.screenshot(region=(box.left , box.pixel_y, 1, 1)).getcolors()[0][1]
        neighbors["up"] = pyautogui.screenshot(region=(box.pixel_x, box.up, 1, 1)).getcolors()[0][1]
        neighbors["down"] = pyautogui.screenshot(region=(box.pixel_x, box.down, 1, 1)).getcolors()[0][1]
        neighbors["leftup"] = pyautogui.screenshot(region=(box.left, box.up, 1, 1)).getcolors()[0][1]
        neighbors["leftdown"] = pyautogui.screenshot(region=(box.left, box.down, 1, 1)).getcolors()[0][1]

        new_neighbors = neighbor_check(neighbors, box)
        return (new_neighbors)

    # right row
    elif box.board_x == 1 and box.board_y > 1 and box.board_y < 9:
        neighbors["right"] = pyautogui.screenshot(region=(box.right, box.pixel_y, 1, 1)).getcolors()[0][1]
        neighbors["up"] = pyautogui.screenshot(region=(box.pixel_x, box.up, 1, 1)).getcolors()[0][1]
        neighbors["down"] = pyautogui.screenshot(region=(box.pixel_x, box.down, 1, 1)).getcolors()[0][1]
        neighbors["rightup"] = pyautogui.screenshot(region=(box.right , box.up, 1, 1)).getcolors()[0][1]
        neighbors["rightdown"] = pyautogui.screenshot(region=(box.right, box.down, 1, 1)).getcolors()[0][1]

        new_neighbors = neighbor_check(neighbors, box)
        return (new_neighbors)

    # top left
    elif box.board_x == 1 and box.board_y == 1:
        neighbors["right"] = pyautogui.screenshot(region=(box.right, box.pixel_y, 1, 1)).getcolors()[0][1]
        neighbors["down"] = pyautogui.screenshot(region=(box.pixel_x, box.down, 1, 1)).getcolors()[0][1]
        neighbors["rightdown"] = pyautogui.screenshot(region=(box.right, box.down, 1, 1)).getcolors()[0][1]

        new_neighbors = neighbor_check(neighbors, box)
        return (new_neighbors)
     
    # top right
    elif box.board_x == 1 and box.board_y == 1:
        neighbors["left"] = pyautogui.screenshot(region=(box.left , box.pixel_y, 1, 1)).getcolors()[0][1]
        neighbors["down"] = pyautogui.screenshot(region=(box.pixel_x, box.down, 1, 1)).getcolors()[0][1]
        neighbors["leftdown"] = pyautogui.screenshot(region=(box.left, box.down, 1, 1)).getcolors()[0][1]

        new_neighbors = neighbor_check(neighbors, box)
        return(new_neighbors)

    # bottom left
    elif box.board_x == 1 and box.board_y == 1:
        neighbors["right"] = pyautogui.screenshot(region=(box.right, box.pixel_y, 1, 1)).getcolors()[0][1]
        neighbors["up"] = pyautogui.screenshot(region=(box.pixel_x, box.up, 1, 1)).getcolors()[0][1]
        neighbors["rightup"] = pyautogui.screenshot(region=(box.right , box.up, 1, 1)).getcolors()[0][1]

        new_neighbors = neighbor_check(neighbors, box)
        return (new_neighbors)

    # bottom right
    elif box.board_x == 1 and box.board_y == 1:
        neighbors["left"] = pyautogui.screenshot(region=(box.left , box.pixel_y, 1, 1)).getcolors()[0][1]
        neighbors["up"] = pyautogui.screenshot(region=(box.pixel_x, box.up, 1, 1)).getcolors()[0][1]
        neighbors["leftup"] = pyautogui.screenshot(region=(box.left, box.up, 1, 1)).getcolors()[0][1]

        new_neighbors = neighbor_check(neighbors, box)
        return (new_neighbors)


board = [['' for i in range(9)] for i in range(9)]

# finds all '1' boxes on screen and saves them as coordinates
ones = list(pyautogui.locateAllOnScreen('States/one.png'))

# uses the coordinates of picture to determine which box each '1' is in
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

    # change get neighbors later to be hidden
    current_one = One(x[0], y[0], x[1], y[1], 1)
    current_one.neighbors = get_neighbors(current_one)

    if coor := current_one.check_complete():
        pyautogui.click(x=coor[0], y=coor[1], button='right')
    


        

    
