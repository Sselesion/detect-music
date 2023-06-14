#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import os
import time
from collections import defaultdict
from enum import Enum
from typing import NamedTuple

from ShazamAPI import Shazam


class Track(NamedTuple):
    title: str = "Unknown title"
    artist: str = "Unknown artist"


def fmt_track(recognized_track: Track) -> str:
    return f"{recognized_track.title} — {recognized_track.artist}"


def get_tracks(dir_from: str) -> str:
    for track_name in os.listdir(dir_from):
        print("Get track '%s'" % track_name)
        yield open(os.path.join(dir_from, track_name), "rb").read()


def get_title_and_artist(raw_track: bytes, timeout: int = 2) -> Track:
    time.sleep(timeout)
    shazam = Shazam(raw_track)
    recognize_generator = shazam.recognizeSong()
    for _, match in recognize_generator:
        try:
            current_track = Track(
                title=match["track"]["title"],
                artist=match["track"]["subtitle"],
            )
        except KeyError:
            print("Trying to find again...")
            continue
        else:
            print(f"Track recognize as '{fmt_track(current_track)}'", end="\n\n")
            break

    return current_track


def detect(dir_from: str, dir_to: str):
    track_count = defaultdict(int)

    for raw_track in get_tracks(dir_from):
        recognized_track = get_title_and_artist(raw_track)

        track_name = fmt_track(recognized_track)

        track_count[track_name] += 1

        if track_count[track_name] > 1:
            track_name += f" ({track_count[track_name]})"

        with open(
            os.path.join(dir_to, f"{track_name}.mp3"),
            "wb",
        ) as wb:
            wb.write(raw_track)


def main():
    parser = argparse.ArgumentParser(
        description=f"A program for recognizing track titles using Shazam."
    )

    parser.add_argument(
        "path_from",
        metavar="PATH_FROM",
        type=str,
        nargs=1,
        help="directory where tracks is located.",
    )
    parser.add_argument(
        "path_to",
        metavar="PATH_TO",
        type=str,
        nargs=1,
        help="directory where the recognized tracks will be placed.",
    )
    args = parser.parse_args()

    if os.path.exists(args.path_from[0]) and os.path.exists(args.path_to[0]):
        detect(args.path_from[0], args.path_to[0])
    else:
        print("The directory(s) you specified do not exist.")


if __name__ == "__main__":
    main()
