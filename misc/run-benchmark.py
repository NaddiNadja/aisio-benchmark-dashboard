import logging as log
import sys
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from paramiko import AutoAddPolicy, SSHClient
from pathlib import Path
from requests import post
from subprocess import Popen, PIPE, STDOUT


BATCH_SIZE = 4096
BATCHES = 300

DEBUG = True
RUN_BENCH_CMD = {
  "posix": f"echo 3 > /proc/sys/vm/drop_caches; stdbuf -oL sil /dev/nvme1n2 --data-dir train --batches {BATCHES} --batch-size {BATCH_SIZE} --mnt /mnt/two --backend posix",
  "gds": f"echo 3 > /proc/sys/vm/drop_caches; stdbuf -oL sil /dev/nvme1n2 --data-dir train --batches {BATCHES} --batch-size {BATCH_SIZE} --mnt /mnt/two --backend gds",
  "aisio": f"echo 3 > /proc/sys/vm/drop_caches; stdbuf -oL sil /dev/libnvm0 --data-dir train --batches {BATCHES} --batch-size {BATCH_SIZE} --gpu-nqueues 6 --backend libnvm-gpu",
}

def run(args: dict):
  def post_line(stdout):
    line:str = stdout.readline()
    if DEBUG:
      print(line)

    if not line or line[0] not in "0123456789":
      return
    
    line = line.split(",")
    line[1] = str(int(line[1]) / BATCHES * 1000)

    post(f"http://{args.dataserver}/post?source={args.source}&data={','.join(line)}")

  if args.host:
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    ssh.connect(
      hostname=args.host,
      username=args.username,
      key_filename=args.key_filename
    )

    _, stdout, _ = ssh.exec_command(RUN_BENCH_CMD[args.source])
    stdout.channel.set_combine_stderr(True)

    while not stdout.channel.exit_status_ready():
      post_line(stdout)

    stdout.channel.recv_exit_status()

    ssh.close()
  else:
    with Popen(
      RUN_BENCH_CMD[args.source],
      stdout=PIPE,
      stderr=STDOUT,
      shell=True,
      text=True,
    ) as process:
      while process.poll() is None:
        post_line(process.stdout)

      process.wait()

  return 0


def setupLogging():
  logFormatter = log.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] %(message)s")
  rootLogger = log.getLogger()

  fileHandler = log.FileHandler(f"./benchmark.log")
  fileHandler.setFormatter(logFormatter)
  fileHandler.setLevel(log.INFO)
  rootLogger.addHandler(fileHandler)

  consoleHandler = log.StreamHandler(stream=sys.stderr)
  consoleHandler.setFormatter(logFormatter)
  consoleHandler.setLevel(log.ERROR)
  rootLogger.addHandler(consoleHandler)


def parse_args():
  parser = ArgumentParser(
    prog=Path(sys.argv[0]).stem,
    formatter_class=ArgumentDefaultsHelpFormatter,
  )
  parser.add_argument(
    "source",
    nargs="?",
    choices=["posix","gds","aisio"],
    default="aisio",
    help="Which benchmark to run.",
  )
  parser.add_argument(
    "--dataserver",
    "-d",
    default="localhost",
    help="Hostname of server to push the benchmark results to.",
  )
  parser.add_argument(
    "--host",
    default=None,
    help="Host on which to run the benchmark. If none given, it is run locally.",
  )
  parser.add_argument(
    "--username",
    "-u",
    type=str,
    default="",
    help="Username to login with on host. Not necessary if run locally."
  )
  parser.add_argument(
    "--key_filename",
    "-k",
    type=str,
    default="",
    help="Path to a private key which grants access to establish an SSH connection with the host. Not necessary if run locally."
  )

  args = parser.parse_args()
  return args


if __name__ == "__main__":
  setupLogging()
  args = parse_args()
  print(f"Running {args.source} benchmarks")
  run(args)
