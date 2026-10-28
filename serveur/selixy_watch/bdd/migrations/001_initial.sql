CREATE TABLE comptes (
    id text PRIMARY KEY,
    pseudo text NOT NULL,
    pseudo_canonique text NOT NULL UNIQUE,
    pseudo_squelette text NOT NULL UNIQUE,
    mdp_hash text,
    avatar text CHECK (avatar IN ('png', 'jpg', 'webp')),
    avatar_version integer NOT NULL DEFAULT 0,
    quota_octets bigint NOT NULL DEFAULT 2147483648,
    cree_le timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE sessions (
    jeton_hash text PRIMARY KEY,
    compte_id text NOT NULL REFERENCES comptes (id) ON DELETE CASCADE,
    cree_le timestamptz NOT NULL DEFAULT now(),
    expire_le timestamptz NOT NULL,
    agent text NOT NULL DEFAULT ''
);
CREATE INDEX sessions_compte ON sessions (compte_id);
CREATE INDEX sessions_expiration ON sessions (expire_le);

CREATE TABLE noeuds (
    id text PRIMARY KEY,
    proprietaire_id text NOT NULL REFERENCES comptes (id) ON DELETE CASCADE,
    parent_id text REFERENCES noeuds (id) ON DELETE CASCADE,
    type text NOT NULL CHECK (type IN ('dossier', 'playlist')),
    nom text NOT NULL,
    rang integer NOT NULL DEFAULT 0,
    cree_le timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX noeuds_parent ON noeuds (parent_id, rang);
CREATE INDEX noeuds_proprietaire ON noeuds (proprietaire_id);

CREATE TABLE medias (
    id text PRIMARY KEY,
    proprietaire_id text NOT NULL REFERENCES comptes (id) ON DELETE CASCADE,
    source text NOT NULL CHECK (source IN ('fichier', 'youtube')),
    reference_youtube text,
    nom text NOT NULL,
    duree integer NOT NULL DEFAULT 0,
    fichier text,
    taille bigint NOT NULL DEFAULT 0,
    miniature boolean NOT NULL DEFAULT false,
    cree_le timestamptz NOT NULL DEFAULT now(),
    UNIQUE (proprietaire_id, reference_youtube)
);
CREATE INDEX medias_proprietaire ON medias (proprietaire_id);

CREATE TABLE playlist_medias (
    id bigserial PRIMARY KEY,
    playlist_id text NOT NULL REFERENCES noeuds (id) ON DELETE CASCADE,
    media_id text NOT NULL REFERENCES medias (id) ON DELETE RESTRICT,
    rang integer NOT NULL
);
CREATE INDEX playlist_medias_rang ON playlist_medias (playlist_id, rang);
CREATE INDEX playlist_medias_media ON playlist_medias (media_id);

CREATE TABLE partages (
    noeud_id text NOT NULL REFERENCES noeuds (id) ON DELETE CASCADE,
    compte_id text NOT NULL REFERENCES comptes (id) ON DELETE CASCADE,
    role text NOT NULL CHECK (role IN ('lecteur', 'editeur')),
    cree_le timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (noeud_id, compte_id)
);
CREATE INDEX partages_compte ON partages (compte_id);

CREATE TABLE invitations (
    jeton_hash text PRIMARY KEY,
    noeud_id text NOT NULL REFERENCES noeuds (id) ON DELETE CASCADE,
    cree_par text NOT NULL REFERENCES comptes (id) ON DELETE CASCADE,
    role text NOT NULL CHECK (role IN ('lecteur', 'editeur')),
    expire_le timestamptz NOT NULL,
    usages_max integer NOT NULL DEFAULT 1 CHECK (usages_max > 0),
    usages integer NOT NULL DEFAULT 0,
    cree_le timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX invitations_noeud ON invitations (noeud_id);

CREATE TABLE messages (
    id bigserial PRIMARY KEY,
    canal_id text NOT NULL REFERENCES noeuds (id) ON DELETE CASCADE,
    compte_id text REFERENCES comptes (id) ON DELETE SET NULL,
    pseudo text NOT NULL,
    texte text NOT NULL,
    cree_le timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX messages_canal ON messages (canal_id, id DESC);
