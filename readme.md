# Grafana dashboard for benchmark results

This is a small setup for animating a benchmarking dashboard for AiSiO, GDS, POSIX and
BaM. The `docker-compose.yaml` hosts multiple docker containers with Grafana, the
dashboard, and a data-server. It is all behind a reverse proxy and can be accessed on
port 80.

## Data

The data server has no data to begin with, but has an endpoint on `/post`, wich expects
2 parameters:

- `source`: one of the three tools, `posix`, `gds`, or `aisio`.  Case insensitive.
- `data`: a single CSV line with 4 comma-separated columns `Time, Batches, IOPS, MiB/s`.

Example: `http://localhost/post?source=posix&data=0,0,0,0`

The `misc/generate-logs.py` helper script can be used to generate artificial logs, and the
`misc/push.py` script can be used to push data from a local file to the data server
endpoint.

The provided script `run-server.py` can be used to provision a host on a specific port
(default: 4000).

```sh
./run-server POSIX
# or
./run-server GDS 4001
```

The `./run-benchmark.sh` script is WIP, but should start the sil benchmarking tool on the
hosts defined in `.env`. The commands necessary to run on the hosts are:

```sh
echo 3 > /proc/sys/vm/drop_caches # clear cache
stdbuf -oL sil <drive> --root-dir train --mnt /mnt/nvme --batch-size 888 --batches 1000 --backend <gds or posix> > /tmp/data-server/data.csv
```

## Run

To view the dashboard, run

```sh
docker compose up --build
```

and go to `http://localhost`.
