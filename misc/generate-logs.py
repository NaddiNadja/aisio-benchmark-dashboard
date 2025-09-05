import random, time
from pathlib import Path
from threading import Thread


ds = Path(__file__).parent

def getrandtime():
  return random.randint(500, 1500) / 1000

def generate_parallel_logs():
  """Generate synthetic logs to use for testing the Grafana dashboard"""

  def worker(source, mn, mx):
    with open(ds / f"{source}.csv", "w") as file:
      file.write("Time, Batches, IOPS, MiB/s\n"),

      t = 0
      i = 0
      while i < 1000:
        file.write(f"{t}, {i}, 100, {i/(t or 0.000001)}\n")
        file.flush()
        t += getrandtime()
        i += random.randint(mn,mx)

      t += getrandtime()
      file.write(f"{t}, 1000, 100, {1000/t}\n")

  Path.mkdir(ds, exist_ok=True)
  threads=[]

  for (source, mn, mx) in [("aisio", 80, 85), ("gds", 20, 25), ("posix", 10, 12)]:
    t = Thread(target=worker, args=(source, mn, mx))
    threads.append(t)
    t.start()


if __name__ == "__main__":
  generate_parallel_logs()
