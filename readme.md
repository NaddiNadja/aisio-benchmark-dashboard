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

## Run

To view the dashboard, run

```sh
docker compose up --build
```

and go to `http://localhost`.

### Benchmarking

The `misc/run-benchmark.py` script can be used to run the SIL benchmarking tool and push
the data to the data-server.

```bash
usage: run-benchmark [-h] [--dataserver DATASERVER] [--host HOST] [--username USERNAME] [--key_filename KEY_FILENAME] [{posix,gds,aisio}]

positional arguments:
  {posix,gds,aisio}     Which benchmark to run. (default: aisio)

options:
  -h, --help            show this help message and exit
  --dataserver DATASERVER, -d DATASERVER
                        Hostname of server to push the benchmark results to. (default: localhost)
  --host HOST           Host on which to run the benchmark. If none given, it is run locally. (default: None)
  --username USERNAME, -u USERNAME
                        Username to login with on host. Not necessary if run locally. (default: )
  --key_filename KEY_FILENAME, -k KEY_FILENAME
                        Path to a private key which grants access to establish an SSH connection with the host. Not necessary if run locally. (default: )
```

For example, it can be used as so:

```bash
python run-benchmark.py aisio -d <host-of-dashboard> --host <host-of-benchmark> -u root -k /path/to/private-key
```

You can change some parameters in the benchmarking tool, such as the batch size and
number of batches, in the Python script. The dashboard should adjust automatically.
