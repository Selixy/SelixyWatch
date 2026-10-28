import sys
import types
from unittest.mock import MagicMock


def installer_synchro():
    try:
        from selixy_watch.canaux import synchro
        return synchro
    except ImportError:
        import selixy_watch.canaux as paquet
        doublure = types.ModuleType("selixy_watch.canaux.synchro")
        doublure.avant_retrait = MagicMock()
        doublure.playlist_modifiee = MagicMock()
        doublure.playlist_supprimee = MagicMock()
        sys.modules["selixy_watch.canaux.synchro"] = doublure
        paquet.synchro = doublure
        return doublure


SYNCHRO = installer_synchro()
