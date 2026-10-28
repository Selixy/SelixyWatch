from contextlib import contextmanager

from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from selixy_watch.bdd.adresse import adresse

TAILLE_MIN = 2
TAILLE_MAX = 16

_reserve = {}


def reserve():
    if "pool" not in _reserve:
        _reserve["pool"] = ConnectionPool(
            adresse(), min_size=TAILLE_MIN, max_size=TAILLE_MAX, kwargs={"row_factory": dict_row}, open=True
        )
    return _reserve["pool"]


@contextmanager
def transaction():
    with reserve().connection() as connexion:
        yield connexion


def fermer():
    pool = _reserve.pop("pool", None)
    if pool:
        pool.close()
