from argparse import ArgumentParser
from pathlib import Path
from time import sleep
from threading import Thread
from requests import post


HOST = "localhost"


def push(source: str):
  path = Path(".") / f"{source}.csv"
  with open(path, "r") as file:
    start = 0
    for line in file.readlines()[1:]:
      t = float(line.split(",")[0])
      post(f"http://{HOST}/post?source={source}&data={line}")
      sleep(t - start)
      start = t


def parse_args():
  global HOST 

  parser = ArgumentParser()
  parser.add_argument(
    "--dataserver",
    "-d",
    default="localhost",
    help="Hostname of server to push the benchmark results to.",
  )

  args = parser.parse_args()
  HOST = args.dataserver

  return args


if __name__ == "__main__":
  _ = parse_args()

  for source in ["posix", "gds", "aisio"]:
    Thread(target=push, args=[source]).start()
