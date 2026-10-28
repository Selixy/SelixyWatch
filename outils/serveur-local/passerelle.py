import http.client
import os
import posixpath
from http.server import SimpleHTTPRequestHandler
from urllib.parse import unquote, urlsplit

from medias import servir_plage

SAUTS = {'transfer-encoding', 'connection', 'keep-alive', 'server', 'date'}
TAILLE_BLOC = 1 << 20
SimpleHTTPRequestHandler.extensions_map['.webmanifest'] = 'application/manifest+json'


class Passerelle(SimpleHTTPRequestHandler):
    interface = ''
    donnees = ''
    port_api = 3240

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

    def translate_path(self, chemin):
        propre = posixpath.normpath(unquote(urlsplit(chemin).path))
        for prefixe in ('/medias/', '/avatars/'):
            if propre.startswith(prefixe):
                return os.path.join(self.donnees, prefixe.strip('/'), propre[len(prefixe):])
        return os.path.join(self.interface, propre.lstrip('/'))

    def relayer(self):
        longueur = int(self.headers.get('Content-Length') or 0)
        entetes = {k: v for k, v in self.headers.items() if k.lower() not in {'host', 'connection'}}
        corps = (self.rfile.read(min(TAILLE_BLOC, longueur)) for _ in range(-(-longueur // TAILLE_BLOC))) if longueur else None
        liaison = http.client.HTTPConnection('127.0.0.1', self.port_api, timeout=3600)
        liaison.request(self.command, self.path, body=corps, headers=entetes)
        reponse = liaison.getresponse()
        self.send_response(reponse.status)
        for nom, valeur in reponse.getheaders():
            if nom.lower() not in SAUTS:
                self.send_header(nom, valeur)
        self.end_headers()
        while bloc := reponse.read1(8192):
            self.wfile.write(bloc)
            self.wfile.flush()

    def do_GET(self):
        if self.path.startswith('/api/'):
            return self.relayer()
        if self.path.startswith(('/medias/', '/avatars/')):
            return servir_plage(self, self.translate_path(self.path))
        return super().do_GET()

    def do_POST(self):
        self.relayer()
