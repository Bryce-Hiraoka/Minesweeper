import pyautogui

class Board:
    def __init__(self):
        self.board = [[0 for _ in range(8)] for _ in range(8)]

    def display_board(self):
        for row in self.board:
            print(row)

    def update_square(self, x, y, value):
        self.board[y][x] = value


def find_ones(tester: Board):
    x_coordinates = [1055, 1119, 1183, 1247, 1311, 1375, 1439, 1503]
    y_coordinates = [471, 535, 599, 663, 727, 791, 855, 919]
    pxl_to_edg = 32

    # map loop to (asset, confidence) so we don’t duplicate code
    scans = {
        1: ('../Final/States/one.PNG',   0.984, 1),
        2: ('../Final/States/two.PNG',   0.984, 2),
        3: ('../Final/States/three.PNG', 0.930, 3),
        4: ('../Final/States/four.PNG',  0.984, 4),
    }

    for loop in (1, 2, 3, 4):
        asset, conf, value = scans[loop]
        number = list(pyautogui.locateAllOnScreen(asset, confidence=conf))  # <-- close paren

        for coors in number:
            x = coors[0]
            if   x < x_coordinates[0] + pxl_to_edg: x = (1, x_coordinates[0])
            elif x < x_coordinates[1] + pxl_to_edg: x = (2, x_coordinates[1])
            elif x < x_coordinates[2] + pxl_to_edg: x = (3, x_coordinates[2])
            elif x < x_coordinates[3] + pxl_to_edg: x = (4, x_coordinates[3])
            elif x < x_coordinates[4] + pxl_to_edg: x = (5, x_coordinates[4])
            elif x < x_coordinates[5] + pxl_to_edg: x = (6, x_coordinates[5])
            elif x < x_coordinates[6] + pxl_to_edg: x = (7, x_coordinates[6])
            else:                                   x = (8, x_coordinates[7])

            y = coors[1]
            if   y < y_coordinates[0] + pxl_to_edg: y = (1, y_coordinates[0])
            elif y < y_coordinates[1] + pxl_to_edg: y = (2, y_coordinates[1])
            elif y < y_coordinates[2] + pxl_to_edg: y = (3, y_coordinates[2])
            elif y < y_coordinates[3] + pxl_to_edg: y = (4, y_coordinates[3])
            elif y < y_coordinates[4] + pxl_to_edg: y = (5, y_coordinates[4])
            elif y < y_coordinates[5] + pxl_to_edg: y = (6, y_coordinates[5])
            elif y < y_coordinates[6] + pxl_to_edg: y = (7, y_coordinates[6])
            else:                                   y = (8, y_coordinates[7])

            tester.update_square(x[0] - 1, y[0] - 1, value)  # note: consistent (col,row) ↔ (x,y)


if __name__ == "__main__":
    tester = Board()
    find_ones(tester)   # pass the board instead of relying on a global
    tester.display_board()
