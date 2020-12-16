#!/usr/bin/env python3
import json
import argparse
from pathlib import Path
import subprocess

GPS_TOW_MIN = 0
GPS_TOW_MAX = 604800


def load_sbp_json_data(filepath: str) -> str:

    fpath = Path(filepath)
    sbjson = fpath.read_text()

    return sbjson


def load_sbp_data(filepath: str) -> str:
    def _convert_to_json(sbpdata: bytes) -> str:

        print("converting sbp data to sbp JSON")
        try:
            sbp2json = subprocess.Popen("sbp2json", stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            sbj, errs = sbp2json.communicate(input=sbpdata)
            sbjson = sbj.decode()
            print("sbp2json conversion complete")
            return sbjson
        except FileNotFoundError:
            raise FileNotFoundError(
                "trim_data requires libsbp tool 'SBP2JSON' installed when processing .sbp file\n"
                "see instructions at https://github.com/swift-nav/libsbp"
            )

    fpath = Path(filepath)
    print("loading sbp data: {}".format(filepath))
    sbp = fpath.read_bytes()
    sbpjson = _convert_to_json(sbp)

    return sbpjson


def parse_cli_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser()
    parser.add_argument("-filepath", "-f", type=str, help="path to .sbp or .sbp.json file", required=True)
    parser.add_argument(
        "-tow", "-t", type=float, help="start time and end time in GPSTOW", nargs=2, required=True
    )

    args = parser.parse_args()

    assert (GPS_TOW_MIN < args.tow[0] < GPS_TOW_MAX), "first TOW argument outside GPSTOW bounds (0-604800 seconds)"
    assert (GPS_TOW_MIN < args.tow[1] < GPS_TOW_MAX), "second TOW argument outside GPSTOW bounds (0-604800 seconds)"

    print("args parsed \n file: {} \n Start TOW: {} \n End TOW: {}".format(args.filepath, args.tow[0], args.tow[1]))
    return args


def trim_json_data(jsondata: list, tows: list) -> list:

    startms = tows[0] * 1000
    endms = tows[1] * 1000
    startidx = None
    endidx = None
    tow = -99
    print("startms: {}, endms: {}".format(startms, endms))
    print("parsing sbp json data for start and end epochs")

    for idx, msg in enumerate(jsondata):
        if '"tow":' in msg:
            msgjson = json.loads(msg)

            try:
                tow = msgjson["header"]["t"]["tow"]
            except KeyError:
                pass

            if not startidx and tow >= startms:
                startidx = idx

            if not endidx and tow > endms:
                endidx = idx

        if startidx and endidx:
            print("start index: {}, end index: {} \n trimming data".format(startidx, endidx))
            trimmed_json = jsondata[startidx:endidx]

            return trimmed_json

    print("start_index: {}\n".format(startidx),
          "end_index: {}".format(endidx))
    raise ValueError("could not find start TOW and end TOW in sbp data.")


def write_output_data(trimmed_json: list, outpath: Path) -> None:
    def _convert_to_sbp(sbpjson: list) -> bytes:

        print("converting json data to sbp")
        jsnstr = "\n".join(sbpjson)
        debugpath = Path("debug.json")
        debugpath.write_text(jsnstr)
        jsonbytes = jsnstr.encode()
        try:
            json2sbp = subprocess.Popen("json2sbp", stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            sbpbytes, errs = json2sbp.communicate(input=jsonbytes)
            print("json2sbp conversion complete")
            return sbpbytes
        except FileNotFoundError:
            raise FileNotFoundError(
                "trim_data requires libsbp tool 'JSON2SBP' installed when processing .sbp file\n"
                "see instructions at https://github.com/swift-nav/libsbp"
            )

    print("writing file: {}".format(outpath))
    if ".json" in outpath.suffixes:

        jsonstr = "\n".join(trimmed_json)
        outpath.write_text(jsonstr)

    else:

        sbp = _convert_to_sbp(trimmed_json)
        outpath.write_bytes(sbp)


def create_output_path(filepath: str, tow: list) -> Path:

    fpath = Path(filepath)
    starttow = int(tow[0])
    endtow = int(tow[1])

    spl = fpath.stem.split(".")
    name = spl[0]
    sfxs = "".join(fpath.suffixes)
    outname = "{}-trimmed_{}-{}{}".format(name, starttow, endtow, sfxs)
    outpath = Path(fpath.parent, outname)

    return outpath


def main() -> None:
    """
    trim_data.py - a utility for trimming sbp logs
    """

    print("trim_data started")
    args = parse_cli_args()

    if args.filepath.endswith(".sbp"):
        sbpjson = load_sbp_data(args.filepath)

    elif args.filepath.endswith(".sbp.json"):
        sbpjson = load_sbp_json_data(args.filepath)
    else:
        raise ValueError("trim data input must be .sbp or .sbp.json")

    jsondata = [msg for msg in sbpjson.split("\n")]

    trimmed_json = trim_json_data(jsondata, args.tow)

    if trimmed_json:
        outpath = create_output_path(args.filepath, args.tow)
        write_output_data(trimmed_json, outpath)

    else:
        raise ValueError("json data empty after trimming. ")

    print("trim_data complete")


if __name__ == "__main__":
    main()
