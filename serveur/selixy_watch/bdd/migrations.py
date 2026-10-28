import os

DOSSIER_MIGRATIONS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "migrations")
VERROU_MIGRATIONS = 724501


def versions_disponibles():
    return sorted(n for n in os.listdir(DOSSIER_MIGRATIONS) if n.endswith(".sql"))


def versions_appliquees(connexion):
    connexion.execute("CREATE TABLE IF NOT EXISTS migrations (version text PRIMARY KEY, appliquee_le timestamptz NOT NULL DEFAULT now())")
    return {ligne["version"] for ligne in connexion.execute("SELECT version FROM migrations")}


def appliquer_une(connexion, version):
    with open(os.path.join(DOSSIER_MIGRATIONS, version), encoding="utf-8") as f:
        connexion.execute(f.read())
    connexion.execute("INSERT INTO migrations (version) VALUES (%s)", (version,))


def migrer(connexion):
    connexion.execute("SELECT pg_advisory_xact_lock(%s)", (VERROU_MIGRATIONS,))
    faites = versions_appliquees(connexion)
    nouvelles = [v for v in versions_disponibles() if v not in faites]
    for version in nouvelles:
        appliquer_une(connexion, version)
    return nouvelles
