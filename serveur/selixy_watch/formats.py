def extension_media(tete):
    if tete[:3] == b"ID3" or (len(tete) > 1 and tete[0] == 0xFF and tete[1] & 0xE0 == 0xE0):
        return "mp3", "audio"
    if tete[:4] == b"OggS":
        return "ogg", "audio"
    if tete[:4] == b"fLaC":
        return "flac", "audio"
    if tete[:4] == b"RIFF" and tete[8:12] == b"WAVE":
        return "wav", "audio"
    if tete[4:8] == b"ftyp":
        return ("m4a", "audio") if tete[8:12] == b"M4A " else ("mp4", "video")
    if tete[:4] == b"\x1a\x45\xdf\xa3":
        return "webm", "video"
    return None, None


def extension_image(tete):
    if tete[:8] == b"\x89PNG\r\n\x1a\n":
        return "png"
    if tete[:3] == b"\xff\xd8\xff":
        return "jpg"
    if tete[:4] == b"RIFF" and tete[8:12] == b"WEBP":
        return "webp"
    return None
