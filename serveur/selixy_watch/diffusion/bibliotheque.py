import queue

from selixy_watch.bibliotheque.export_flux import exporter
from selixy_watch.etat import ABONNES, verrou


def signaler(comptes):
    exporter()
    cibles = set(comptes)
    if not cibles:
        return
    with verrou:
        for q, info in list(ABONNES.items()):
            if info.get("ident") not in cibles:
                continue
            try:
                q.put_nowait(("bibliotheque", {}))
            except queue.Full:
                ABONNES.pop(q, None)
