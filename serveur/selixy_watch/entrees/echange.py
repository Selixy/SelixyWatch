import json


def repondre(h, code, corps, entetes=()):
    data = json.dumps(corps, ensure_ascii=False).encode()
    h.send_response(code)
    h.send_header("Content-Type", "application/json; charset=utf-8")
    h.send_header("Content-Length", str(len(data)))
    h.send_header("Cache-Control", "no-store")
    for k, v in entetes:
        h.send_header(k, v)
    h.end_headers()
    h.wfile.write(data)


def longueur_annoncee(h):
    return int(h.headers.get("Content-Length", "0"))


def corps_json(h, maxi=4096):
    n = longueur_annoncee(h)
    if n <= 0 or n > maxi:
        raise ValueError
    d = json.loads(h.rfile.read(n))
    if not isinstance(d, dict):
        raise ValueError
    return d
