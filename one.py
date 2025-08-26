import pyautogui

#bomb = 178,66,66
#3 = 246,23,23

middle_x = {
    1: 1055, 
    2: 1119, 
    3: 1183, 
    4: 1247, 
    5: 1311, 
    6: 1375, 
    7: 1439, 
    8: 1503
}

middle_y = {
    1: 471, 
    2: 535, 
    3: 599, 
    4: 663, 
    5: 727, 
    6: 791, 
    7: 855, 
    8: 919
}

positions = [(-1, 1),(1, -1), (1,1), (-1,-1), (1,0), (0,1), (-1,0), (0, -1)] 

class Square:
    def __init__(self, x_coordinate, y_coordinate, value):
        self.x = x_coordinate
        self.y = y_coordinate
        self.value = value
        type = get_type(self.x, self.y)

        left = (self.x - 1, self.y)
        right = (self.x + 1, self.y)
        up = (self.x, self.y - 1)
        down = (self.x, self.y + 1)
        up_left = (self.x - 1, self.y - 1)
        up_right = (self.x + 1, self.y - 1)
        down_left = (self.x - 1, self.y + 1)
        down_right = (self.x + 1, self.y + 1)
        

        match type:
            case "middle":
                self.neighbors_coords = [left, right, up, down, up_left, up_right, down_left, down_right]     
            case "top_right":
                self.neighbors_coords = [left, down, down_left]        
            case "top_left":
                self.neighbors_coords = [right, down, down_right]
            case "bottom_right":
                self.neighbors_coords = [left, up, up_left]        
            case "bottom_left":
                self.neighbors_coords = [right, up, up_right]
            case "top_middle":
                self.neighbors_coords = [left, right, down, down_left, down_right]
            case "bottom_middle":
                self.neighbors_coords = [left, right, up, up_left, up_right]
            case "right_middle":
                self.neighbors_coords = [left, up, down, up_left, down_left]          
            case "left_middle":
                self.neighbors_coords = [right, up, down, up_right, down_right]
            case _:
                print("Square Type Error")


        
class Board:
    def __init__(self):
        self.board = []
        for i in range(8):
            self.board.append([])
            for _ in range(8):
                self.board[i].append(0)
    
    def display_board(self):
        for row in self.board:
            print(row)

    def update_square(self, x, y, value):
        self.board[x][y] = value

    def set_neighbors(self, neighbors_coords, box):
        bomb_neighbor = 0
        bomb = []
        for x, y in neighbors_coords:
            #print(x, y)
            if self.board[y - 1][x - 1] != 0:
                if self.board[y - 1][x - 1] == "B":
                    bomb_neighbor += 1
                elif self.board[y - 1][x - 1] == "U":
                    bomb.append((x, y))
                continue 
            else:
                value = get_value(middle_x[x], middle_y[y])
                if value == "U":
                    bomb.append((x, y))
                elif value == "B":
                    bomb_neighbor += 1
                self.update_square(y - 1, x - 1, value)
        if len(bomb) + bomb_neighbor == box.value and bomb_neighbor < box.value:
            for pot in bomb:
                print(pot)
                self.update_square(pot[1] - 1, pot[0] - 1, 'B')
                pyautogui.click(x=middle_x[pot[0]], y=middle_y[pot[1]], button='right')
                print("bomb at", pot[0], pot[1])
        
        if bomb_neighbor == box.value:
            bomb_click(bomb)
        


# Specifies where on the board the given coordinate is        
def get_type(x, y):
    on_top = y == 1
    on_bottom = y == 8
    on_right = x == 8
    on_left = x == 1

    combo = (on_top, on_bottom, on_right, on_left)

    lookup = {
        (False, False, False, False): "middle",
        (True, False, True, False): "top_right",
        (True, False, False, True): "top_left",
        (True, False, False, False): "top_middle",
        (False, True, True, False): "bottom_right",
        (False, True, False, True): "bottom_left",
        (False, True, False, False): "bottom_middle",
        (False, False, True, False): "right_middle",
        (False, False, False, True): "left_middle"
    }

    return lookup[combo]

def get_value(x, y):
    value = ""
    color_neigh_center = pyautogui.screenshot(region=(x, y + 3, 1, 1)).getcolors()[0][1]
    #print(color_neigh_center)
    if color_neigh_center[0] == 189:
        color = pyautogui.screenshot(region=(x, y - 27, 1, 1)).getcolors()[0][1][0]
        if color == 255:
            value = "U"
        else:
            value = "N"
    elif color_neigh_center[0] == 178:
        value = "B"
    else:
        if color_neigh_center[2] == 255:
            value = 1
        elif color_neigh_center[1] == 123:
            value = 2
        elif color_neigh_center[2] == 123:
            value = 4
        else:
            value = 3
    
    return value

def bomb_click(neighbor_coords):
    for x, y in neighbor_coords:
        pyautogui.click(x=middle_x[x], y=middle_y[y], button="left")



tester = Board()
for _ in range(15):
    progress = False
    for loop in [1, 2, 3, 4]:
        if loop == 1:
            # finds all '1' boxes on screen and saves them as coordinates
            try:
                print('1',)
                number = list(pyautogui.locateAllOnScreen('States/one.PNG', confidence=0.984))
            except:
                continue
        elif loop == 2:
            # finds all '2' boxes on screen and saves them as coordinates
            try:
                print('2')
                number = list(pyautogui.locateAllOnScreen('States/two.png', confidence=0.984))
            except:
                continue
        elif loop == 3:
            # finds all '3' boxes on screen and saves them as coordinates
            try:
                print('3')
                number = list(pyautogui.locateAllOnScreen('States/three.png', confidence=0.930))
            except:
                continue
        elif loop == 4:
            # finds all '4' boxes on screen and saves them as coordinates
            try:
                print('4')
                number = list(pyautogui.locateAllOnScreen('States/four.png', confidence=0.984))
            except:
                continue
        #number = list(pyautogui.locateAllOnScreen('States/one.PNG', confidence=0.984))
        #number = list(pyautogui.locateAllOnScreen('States/two.PNG', confidence=0.984))
        #number = list(pyautogui.locateAllOnScreen('States/three.PNG', confidence=0.930))


        x_coordinates = [1055, 1119, 1183, 1247, 1311, 1375, 1439, 1503]
        y_coordinates = [471, 535, 599, 663, 727, 791, 855, 919]
        pxl_to_edg = 32


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
            
            print(x[0], y[0])

            if loop == 1:
                box = Square(x[0], y[0], 1)
                tester.update_square(y[0] - 1, x[0] - 1, 1)
            elif loop == 2:
                box = Square(x[0], y[0], 2) 
                tester.update_square(y[0] - 1, x[0] - 1, 2)
            elif loop == 3:
                box = Square(x[0], y[0], 3)
                tester.update_square(y[0] - 1, x[0] - 1, 3)
            else:
                box = Square(x[0], y[0], 4)
                tester.update_square(y[0] - 1, x[0] - 1, 4)
    
            tester.set_neighbors(box.neighbors_coords, box)
            tester.display_board()

    check = pyautogui.screenshot(region=(1265, 342, 1, 1)).getcolors()[0][1][0]
    if check == 0:
        print("Win")
        break
    elif check == 59:
        print("Lost :(")
        break
