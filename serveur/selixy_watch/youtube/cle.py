import os
import re

from selixy_watch.configuration import DOSSIER


def cle_youtube():
    cle = os.environ.get("YOUTUBE_API_KEY", "").strip()
    if not cle:
        try:
            with open(os.path.join(DOSSIER, "cle_youtube.txt"), encoding="utf-8") as f:
                cle = f.read().strip()
        except OSError:
            cle = ""
    return cle if re.fullmatch(r"[\w-]{20,80}", cle) else ""
