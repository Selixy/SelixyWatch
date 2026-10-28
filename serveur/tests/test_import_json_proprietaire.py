import unittest

from tests.aides_banc_import import BancImport
from tests.aides_bdd import ADRESSE, RAISON


@unittest.skipUnless(ADRESSE, RAISON)
class TestImportJsonProprietairePro(BancImport):
    def test_proprietaire_pro_et_autres_free(self):
        code, texte = self.lancer("--renommer", "lntel=Lintel", "--appliquer")
        self.assertEqual(code, 0, texte)
        offres = {c["id"]: (c["offre"], c["quota_octets"], c["email_valide_le"]) for c in self.lignes("SELECT * FROM comptes")}
        self.assertEqual(offres["aaaaaaaaaaaaaaaa"], ("pro", 20 * 1024 ** 3, None))
        self.assertEqual({v for k, v in offres.items() if k != "aaaaaaaaaaaaaaaa"}, {("free", 0, None)})
