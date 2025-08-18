# Grafana dashboard for benchmark results

This is a small setup for animating a benchmarking dashboard for AiSiO, GDS, POSIX and
BaM. The `docker-compose.yaml` hosts a dockerised version of Grafana and a dockerised
dashboard server, which provides the local data-sources and a web interface embedding the
provided dashboard. It is all behind a reverse proxy and can be accessed at
`http://localhost`.

## Data sources

The dashboard expects three data sources, which are three independent processes running
the Flask server in `./data-server/server.py`.

### Run locally

To run locally, the benchmarking data must be provided beforehand in the
`./data-server/data` directory. The `generate-logs.py` helper script can be used to
generate artificial logs.

The docker containers `posix`, `gds` and `aisio` will act as servers for each of the
three data-sources.

### Run on external hosts

If run on external hosts, nginx expects the servers to be hosted on port 4000 for each.
The host IP addresses should be defined in a `.env` file define the variables
`POSIX_HOST`, `GDS_HOST`, and `AISIO_HOST`.

The server can be run with:

```sh
usage: server [-h] [--data-path DATA_PATH]
              [--time-column TIME_COLUMN]
              [--port PORT]

options:
  -h, --help            show this help message
                        and exit
  --data-path DATA_PATH, -d DATA_PATH
                        Path to to the data
                        source CSV (default:
                        data.csv)
  --time-column TIME_COLUMN, -t TIME_COLUMN
                        Name of the CSV column
                        indicating time in
                        milliseconds (default:
                        Time)
  --port PORT, -p PORT  Port to host the Flask
                        server on (default:
                        4000)
```

Edit the `docker-compose.yaml` and remove, or comment out, the `posix`, `gds` and `aisio`
containers. Additionally, edit the `nginx` container to not depend on these containers,
and instead add the IP addresses for the hosts under key `extra_hosts`.

The provided script `run-server.py` can be used to provision a host on a specific port (default: 4000).

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

### Resetting the benchmark

When run locally, the "Reset" button in the UI makes a fetch to the `/reset-data`
endpoint on the data server, which rewrites the pregenerated data to the `./data.csv`
file, imitating a real-time flow of data. If run on an external host, this endpoint
should not be used, as there will be no pregenerated data. Instead, another way of
resetting the `./data.csv` should be used (e.g. re-running the benchmarks).

## Run

To view the dashboard, run

```sh
docker compose up --build
```

and go to `http://localhost`.
