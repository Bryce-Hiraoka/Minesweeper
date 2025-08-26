import subprocess

files = ["one.py", "two.py", "three.py"]

# Run each file 5 times
for i in range(5):
    print(f"\n--- Run {i+1} ---")
    for file in files:
        print(f"Running {file}...")
        subprocess.run(["python", file])