from threading import Thread
from requests import post

def push(source: str):
  post(f"http://localhost/post?source={source}&data=0,0,0,0")

for source in ["posix", "gds", "aisio"]:
   Thread(target=push, args=[source]).start()
