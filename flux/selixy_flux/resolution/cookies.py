import os
import shutil

from selixy_flux.journal import journal


def copie_a_jour(source, copie):
    return os.path.isfile(copie) and os.path.getmtime(copie) >= os.path.getmtime(source)


def avec_cookies(options, source, copie):
    if not os.path.isfile(source):
        return options
    try:
        if not copie_a_jour(source, copie):
            shutil.copyfile(source, copie)
    except OSError as erreur:
        journal.error('cookies illisibles (%s) : %s', source, erreur)
        return options
    return {**options, 'cookiefile': copie}
