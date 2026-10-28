def adresse_client(h):
    reelle = h.headers.get("X-Real-IP", "").strip()
    return reelle or h.client_address[0]


def agent_client(h):
    return h.headers.get("User-Agent", "")[:200]
