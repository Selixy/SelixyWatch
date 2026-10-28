import http.client
import json
import os
import subprocess
import sys
import tempfile

NOM_PLAYLIST = 'Test (vidéo factice)'
DUREE_S = 120


def requete(port, chemin, corps, entetes):
    liaison = http.client.HTTPConnection('127.0.0.1', port, timeout=120)
    liaison.request('POST', chemin, body=corps, headers={'Content-Length': str(len(corps)), **entetes})
    reponse = liaison.getresponse()
    return reponse.status, json.loads(reponse.read() or b'{}')


def fabriquer(dossier, duree):
    video = os.path.join(dossier, 'factice.mp4')
    mini = os.path.join(dossier, 'mini.jpg')
    source = ['-f', 'lavfi', '-i', 'testsrc2=size=1280x720:rate=30', '-f', 'lavfi', '-i', 'sine=frequency=440:sample_rate=44100']
    base = ['ffmpeg', '-v', 'error', '-y', *source, '-t', str(duree)]
    subprocess.run([*base, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'veryfast', '-crf', '30', '-g', '30', '-c:a', 'aac', '-b:a', '64k', '-movflags', '+faststart', video], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', video, '-ss', '3', '-frames:v', '1', '-vf', 'scale=320:-1', '-q:v', '5', mini], check=True)
    return video, mini


def semer(port, duree=DUREE_S):
    with tempfile.TemporaryDirectory() as dossier:
        video, mini = fabriquer(dossier, duree)
        code, playlist = requete(port, '/api/arbre/creer', json.dumps({'nom': NOM_PLAYLIST, 'type': 'playlist'}).encode(), {'Content-Type': 'application/json'})
        octets = open(video, 'rb').read()
        entetes = {'X-Playlist': playlist['id'], 'X-Nom': 'Vidéo factice (compteur et bip)', 'X-Duree': str(duree), 'Content-Type': 'video/mp4'}
        code, media = requete(port, '/api/medias', octets, entetes)
        requete(port, f"/api/medias/{media['id']}/miniature", open(mini, 'rb').read(), {'Content-Type': 'image/jpeg'})
    return playlist['id'], media['id']


if __name__ == '__main__':
    print(semer(int(sys.argv[1]) if len(sys.argv) > 1 else 3240))
