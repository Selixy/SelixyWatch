#!/usr/bin/env python3
import sys

from selixy_watch.administration.principal import executer
from selixy_watch.bdd.connexion import fermer, transaction

if __name__ == "__main__":
    code, texte = executer(sys.argv[1:], transaction)
    print(texte)
    fermer()
    sys.exit(code)
