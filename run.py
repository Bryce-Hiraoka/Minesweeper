# 1265, 342

import subprocess
import pyautogui


files = ["one.py", "two.py", "three.py"]

# Run each file 5 times
for i in range(5):
    print(f"\n--- Run {i+1} ---")
    for file in files:
        print(f"Running {file}...")
        subprocess.run(["python", file])
        check = pyautogui.screenshot(region=(1265, 342, 1, 1)).getcolors()[0][1]
        print(check)
