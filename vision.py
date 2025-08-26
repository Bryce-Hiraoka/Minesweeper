import pyautogui

x = [1055, 1119, 1183, 1247, 1311, 1375, 1439, 1503]
y = [471, 535, 599, 663, 727, 791, 855, 919]


for i in x:
    for j in y:
        pyautogui.click(i, j, button='right')
        pyautogui.click(i, j, button='right')

