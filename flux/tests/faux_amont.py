import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

CONTENU = bytes(range(100))


class Amont(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/interdit':
            return self.send_error(403)
        debut, fin = (int(x) for x in self.headers['Range'].removeprefix('bytes=').split('-'))
        if debut >= len(CONTENU):
            self.send_response(416)
            self.send_header('Content-Range', f'bytes */{len(CONTENU)}')
            self.send_header('Content-Length', '0')
            return self.end_headers()
        morceau = CONTENU[debut:fin + 1]
        self.send_response(206)
        self.send_header('Content-Range', f'bytes {debut}-{debut + len(morceau) - 1}/{len(CONTENU)}')
        self.send_header('Content-Length', str(len(morceau)))
        self.end_headers()
        self.wfile.write(morceau)

    def log_message(self, *arguments):
        return


def demarrer_faux_amont():
    serveur = ThreadingHTTPServer(('127.0.0.1', 0), Amont)
    threading.Thread(target=serveur.serve_forever, daemon=True).start()
    return serveur
