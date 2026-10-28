import io


class FauxGestionnaire:
    def __init__(self, ident, corps=b"", entetes=None):
        self.ident = ident
        self.rfile = io.BytesIO(corps)
        self.headers = {"Content-Length": str(len(corps)), **(entetes or {})}
