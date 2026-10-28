def propre(texte, maxi):
    t = "".join(c for c in str(texte) if c.isprintable())
    return " ".join(t.split())[:maxi]
