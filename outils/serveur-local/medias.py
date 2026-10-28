import mimetypes
import os
import time

TAILLE_BLOC = 1 << 20


def servir_plage(h, chemin):
    if not os.path.isfile(chemin):
        h.send_error(404)
        return
    time.sleep(float(os.environ.get('LATENCE_MEDIAS', '0')))
    taille = os.path.getsize(chemin)
    debut, fin, code = 0, taille - 1, 200
    plage = h.headers.get('Range', '')
    if plage.startswith('bytes=') and '-' in plage:
        a, b = plage[6:].split('-', 1)
        debut = int(a) if a else max(0, taille - int(b))
        fin = min(int(b), taille - 1) if a and b else taille - 1
        code = 206
    h.send_response(code)
    h.send_header('Content-Type', mimetypes.guess_type(chemin)[0] or 'application/octet-stream')
    h.send_header('Accept-Ranges', 'bytes')
    h.send_header('Content-Length', str(fin - debut + 1))
    if code == 206:
        h.send_header('Content-Range', f'bytes {debut}-{fin}/{taille}')
    h.end_headers()
    with open(chemin, 'rb') as f:
        f.seek(debut)
        reste = fin - debut + 1
        while reste > 0:
            bloc = f.read(min(TAILLE_BLOC, reste))
            if not bloc:
                break
            h.wfile.write(bloc)
            reste -= len(bloc)
