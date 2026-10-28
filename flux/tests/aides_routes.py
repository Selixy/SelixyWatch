import io

from selixy_flux.entrees.services import Services


def services(lire=None):
    return Services(
        lambda media: 'dQw4w9WgXcQ' if media == 'aaaaaaaaaaaa' else None,
        lire,
        lambda yt: b'{"duree": 5}',
    )


def lire_factice(appels):
    def lire(yt, piste, plage):
        appels.append((yt, piste, plage))
        return 206, {'Content-Range': 'bytes 0-3/9'}, io.BytesIO(b'abcd')
    return lire
