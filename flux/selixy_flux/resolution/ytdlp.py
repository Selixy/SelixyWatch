import yt_dlp

from selixy_flux.journal import journal
from selixy_flux.relais.erreurs import ErreurAmont, ErreurBlocage
from selixy_flux.resolution.cookies import avec_cookies
from selixy_flux.resolution.source import Lecture, Source

COOKIES = '/secrets/cookies.txt'
COPIE_COOKIES = '/tmp/cookies.txt'
FORMAT = (
    'bv[ext=mp4][vcodec^=avc1][height<=720]+ba[ext=m4a]'
    '/bv[ext=mp4][vcodec^=avc1]+ba[ext=m4a]'
)
OPTIONS = {
    'quiet': True,
    'no_warnings': True,
    'noplaylist': True,
    'cachedir': False,
    'format': FORMAT,
    'socket_timeout': 15,
}


def source_de(piste):
    return Source(piste['url'], dict(piste.get('http_headers') or {}))


def mime_de(type_media, codec):
    return f'{type_media}/mp4; codecs="{codec}"'


def resoudre(yt):
    try:
        with yt_dlp.YoutubeDL(avec_cookies(OPTIONS, COOKIES, COPIE_COOKIES)) as extracteur:
            info = extracteur.extract_info(f'https://www.youtube.com/watch?v={yt}', download=False)
        video, audio = info['requested_formats']
    except (yt_dlp.utils.YoutubeDLError, KeyError, ValueError) as erreur:
        journal.error('résolution de %s impossible : %s', yt, erreur)
        if 'Sign in to confirm' in str(erreur):
            raise ErreurBlocage(0) from erreur
        raise ErreurAmont(0) from erreur
    informations = {
        'duree': info.get('duration') or 0,
        'video': {'mime': mime_de('video', video['vcodec'])},
        'audio': {'mime': mime_de('audio', audio['acodec'])},
    }
    return Lecture(source_de(video), source_de(audio), informations)
