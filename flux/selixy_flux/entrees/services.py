from typing import Callable, NamedTuple


class Services(NamedTuple):
    identifiant: Callable
    lire: Callable
    informations: Callable
