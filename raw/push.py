from pathlib import Path
from time import sleep
from threading import Thread
from requests import post

def push(source: str):
  path = Path(".") / f"{source}.csv"
  with open(path, "r") as file:
    for line in file.readlines()[1:]:
        post(f"http://localhost/post?source={source}&data={line}")
        sleep(0.5)

for source in ["posix", "gds", "aisio"]:
   Thread(target=push, args=[source]).start()
