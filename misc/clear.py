from argparse import ArgumentParser
from threading import Thread
from requests import post


HOST = "localhost"


def push(source: str):
  post(f"http://{HOST}/post?source={source}&data=0,0,0,0\n")


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
