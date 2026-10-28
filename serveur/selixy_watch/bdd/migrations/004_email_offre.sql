ALTER TABLE comptes ADD COLUMN email text;
ALTER TABLE comptes ADD COLUMN email_valide_le timestamptz;
ALTER TABLE comptes ADD COLUMN email_en_attente text;
ALTER TABLE comptes ADD COLUMN offre text NOT NULL DEFAULT 'free' CHECK (offre IN ('free', 'pro'));
ALTER TABLE comptes ALTER COLUMN quota_octets SET DEFAULT 0;
UPDATE comptes SET quota_octets = 0 WHERE offre = 'free';
CREATE UNIQUE INDEX comptes_email_valide ON comptes (lower(email)) WHERE email_valide_le IS NOT NULL;

CREATE TABLE jetons_courriel (
    jeton_hash text PRIMARY KEY,
    compte_id text NOT NULL REFERENCES comptes (id) ON DELETE CASCADE,
    nature text NOT NULL CHECK (nature IN ('confirmation', 'recuperation')),
    email text NOT NULL,
    expire_le timestamptz NOT NULL,
    utilise_le timestamptz
);
CREATE INDEX jetons_courriel_compte ON jetons_courriel (compte_id);
