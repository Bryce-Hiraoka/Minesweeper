import pyautogui

def screenshot(x, y):
    return pyautogui.screenshot(region=(x, y, 1, 1)).getcolors()[0][1]

def locate(number):
    if number == 'one.PNG' or number == 'two.PNG' or number == 'four.PNG':
        return list(pyautogui.locateAllOnScreen('States/' + number, confidence=0.984))
    elif number == 'three.PNG':
        return list(pyautogui.locateAllOnScreen('States/' + number, confidence=0.930))


def click(x, y, type):
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
    print(x, y, type)
    pyautogui.click(x=middle_x[x], y=middle_y[y], button=type)
    pyautogui.moveTo(980, 264)
