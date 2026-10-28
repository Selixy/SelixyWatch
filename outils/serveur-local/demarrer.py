import os
import signal
import subprocess
import sys
import tempfile
import time
import urllib.request
from http.server import ThreadingHTTPServer

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from base import fermer_base, ouvrir_base
from donnees_test import semer
from passerelle import Passerelle


def attendre_api(port):
    for _ in range(100):
        try:
            urllib.request.urlopen(f'http://127.0.0.1:{port}/api/sante', timeout=1).close()
            return
        except OSError:
            time.sleep(0.1)


def principal():
    signal.signal(signal.SIGTERM, signal.default_int_handler)
    port = int(os.environ.get('PORT_LOCAL', '8080'))
    donnees = os.environ.get('DONNEES_LOCALES') or os.path.join(tempfile.gettempdir(), 'watch-local')
    os.makedirs(os.path.join(donnees, 'medias'), exist_ok=True)
    os.makedirs(os.path.join(donnees, 'avatars'), exist_ok=True)
    Passerelle.interface = os.path.join(RACINE, 'ui')
    Passerelle.donnees = donnees
    Passerelle.port_api = int(os.environ.get('PORT_API', '3240'))
    adresse_bdd, bdd_lancee = ouvrir_base()
    api = subprocess.Popen([sys.executable, os.path.join(RACINE, 'serveur', 'watch.py')],
                           env={'MAIL_URL': 'stdout', **os.environ, 'STATE_DIRECTORY': donnees, 'COOKIE_SECURE': '0', 'BDD_URL': adresse_bdd, 'PORT': str(Passerelle.port_api)})
    marque = os.path.join(donnees, 'donnees-test-semees')
    if '--donnees-test' in sys.argv and not os.path.exists(marque):
        attendre_api(Passerelle.port_api)
        print('Données de test :', semer(Passerelle.port_api), flush=True)
        open(marque, 'w').close()
    print(f'SelixyWatch en local : http://127.0.0.1:{port}/  (données : {donnees})', flush=True)
    try:
        ThreadingHTTPServer(('127.0.0.1', port), Passerelle).serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        api.terminate()
        fermer_base(bdd_lancee)


if __name__ == '__main__':
    principal()
