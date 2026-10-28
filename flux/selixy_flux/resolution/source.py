from typing import NamedTuple


class Source(NamedTuple):
    url: str
    entetes: dict


class Lecture(NamedTuple):
    video: Source
    audio: Source
    informations: dict
