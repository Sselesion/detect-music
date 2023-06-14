import json
import os
import time

from collections import defaultdict
from enum import Enum
from typing import NamedTuple

from ShazamAPI import Shazam


class Dirs(Enum):
    IN = "in"
    OUT = "out"


class Track(NamedTuple):
    title: str = "Unknown title"
    artist: str = "Unknown artist"


def fmt_track(recognized_track: Track) -> str:
    return f"{recognized_track.title} — {recognized_track.artist}"


def get_tracks(dir_in: str) -> str:
    for track_name in os.listdir(dir_in):
        print("Get track '%s'" % track_name)
        yield open(f"in/{track_name}", "rb").read()


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


def main():
    track_count = defaultdict(int)

    for raw_track in get_tracks(Dirs.IN.value):
        recognized_track = get_title_and_artist(raw_track)

        track_name = fmt_track(recognized_track)

        track_count[track_name] += 1

        if track_count[track_name] > 1:
            track_name += f" ({track_count[track_name]})"

        with open(
            f"{Dirs.OUT.value}/{track_name}.mp3",
            "wb",
        ) as wb:
            wb.write(raw_track)


if __name__ == "__main__":
    main()
