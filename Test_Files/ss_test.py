import pyautogui
from PIL import Image
from test import Board
tester = Board()
colors = {
    (0,0,255): 1,
    (189, 189, 189): 0,
    (0,123,0): 2,
    (207,118,118): 9,
    (255,0,0): 3,
    (0,0,123): 4
}

right = 1535
left = 1024
bottom = 951
top = 440

box_height = int(round((bottom - top) / 8))
box_width = int(round((right - left) / 8))

screenshot = pyautogui.screenshot()

for y in range(8):
    for x in range(8):
        pixel_x = int(round((x + 0.5) * box_width + left))
        pixel_y = int(round((y + 0.5) * box_height + top))
        color = screenshot.getpixel((pixel_x - 3, pixel_y))
        tester.update_square(x, y, colors[color])

tester.display_board()


