import logging as log
import sys
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from flask import Flask, Response, request
from pandas import read_csv
from pathlib import Path
from time import sleep
from threading import Thread


app = Flask(__name__)

DATA_PATH: Path = Path("./data.csv")
PREGENERATED_DATA_PATH: Path = Path("./pregenerated.csv")
TIME_COLUMN: str = "Time"


@app.route("/data")
def get_data():
    global DATA_PATH, TIME_COLUMN

    try:
        from_s = (request.args.get("from", type=int) or 0) / 1000
        to_s = (request.args.get("to", type=int) or 0) / 1000

        df = read_csv(DATA_PATH)
        res = df[(df[TIME_COLUMN] >= from_s) & (df[TIME_COLUMN] <= to_s)]
        if not len(res):
            res = df.tail(1)

        return Response(res.to_csv(index=False), mimetype="text/csv")
    except Exception as e:
        log.error(e)
        return Response(None, 500)


@app.route("/reset-data")
def reset():
    def reset_data():
        global DATA_PATH, PREGENERATED_DATA_PATH
        with open(DATA_PATH, "w") as data_file:
            with open(PREGENERATED_DATA_PATH, "r") as pregenerated_file:
                for line in pregenerated_file:
                    data_file.write(line)
                    data_file.flush()
                    sleep(0.5)

    log.info("Resetting data")
    Thread(target = reset_data).start()
    return Response("Successfully reset data", 200)


def setupLogging():
    logFormatter = log.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    rootLogger = log.getLogger()

    fileHandler = log.FileHandler(f"./server.log")
    fileHandler.setFormatter(logFormatter)
    fileHandler.setLevel(log.INFO)
    rootLogger.addHandler(fileHandler)

    consoleHandler = log.StreamHandler(stream=sys.stderr)
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.setLevel(log.ERROR)
    rootLogger.addHandler(consoleHandler)


def parse_args():
    global DATA_PATH, TIME_COLUMN

    parser = ArgumentParser(
        prog=Path(sys.argv[0]).stem,
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--data-path", 
        "-d", 
        type=Path, 
        default=Path("./data.csv"),
        help="Path to to the data source CSV"
    )
    parser.add_argument(
        "--time-column", 
        "-t", 
        type=str, 
        default="Time",
        help="Name of the CSV column indicating time in milliseconds"
    )
    parser.add_argument(
        "--port", 
        "-p", 
        type=int, 
        default=4000,
        help="Port to host the Flask server on"
    )

    args = parser.parse_args()

    DATA_PATH = args.data_path.resolve()
    log.info(f"Path to data source: {DATA_PATH}")

    TIME_COLUMN = args.time_column
    log.info(f"Using column({args.time_column}) as time column")

    return args


if __name__ == "__main__":
    setupLogging()
    args = parse_args()

    app.run(host="0.0.0.0", port=args.port)
