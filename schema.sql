/* ------------------------------ PARAMÈTRES GÉNÉRAUX ------------------------------ */
SET NAMES utf8mb4;
SET sql_mode = 'STRICT_ALL_TABLES';

CREATE DATABASE IF NOT EXISTS ULBStudyShareDB
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;
USE ULBStudyShareDB;

/* ------------------------------ TABLES PRINCIPALES ------------------------------ */
CREATE TABLE IF NOT EXISTS ObjetCosmetique (
    idObjet         INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nomObjet        VARCHAR(100) NOT NULL,
    description     VARCHAR(500) NOT NULL,
    prixPoints      INT UNSIGNED NOT NULL,
    CONSTRAINT uq_objet_nom UNIQUE (nomObjet),
    CONSTRAINT ck_objet_prix CHECK (prixPoints >= 1)
);

CREATE TABLE IF NOT EXISTS Badge (
    idObjet         INT UNSIGNED PRIMARY KEY,
    CONSTRAINT fk_badge_objet FOREIGN KEY (idObjet)
        REFERENCES ObjetCosmetique(idObjet)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Titre (
    idObjet         INT UNSIGNED PRIMARY KEY,
    CONSTRAINT fk_titre_objet FOREIGN KEY (idObjet)
        REFERENCES ObjetCosmetique(idObjet)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS ThemeProfil (
    idObjet         INT UNSIGNED PRIMARY KEY,
    CONSTRAINT fk_theme_objet FOREIGN KEY (idObjet)
        REFERENCES ObjetCosmetique(idObjet)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Utilisateur (
    idUtilisateur   INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nomUtilisateur  VARCHAR(50) NOT NULL,
    email           VARCHAR(255) NOT NULL,
    motDePasse      VARCHAR(255) NOT NULL,
    dateInscription DATE NOT NULL DEFAULT (CURRENT_DATE),
    niveau          INT UNSIGNED NOT NULL DEFAULT 1,
    nombrePoints    INT UNSIGNED NOT NULL DEFAULT 0,
    idBadgeActif    INT UNSIGNED NULL,
    idTitreActif    INT UNSIGNED NULL,
    idThemeActif    INT UNSIGNED NULL,
    CONSTRAINT uq_utilisateur_nom UNIQUE (nomUtilisateur),
    CONSTRAINT uq_utilisateur_email UNIQUE (email),
    CONSTRAINT ck_utilisateur_niveau CHECK (niveau >= 1),
    CONSTRAINT ck_utilisateur_points CHECK (nombrePoints >= 0),
    CONSTRAINT ck_utilisateur_email_format CHECK (email REGEXP '^[^@[:space:]]+@[^@[:space:]]+\\.[^@[:space:]]+$'),
    CONSTRAINT fk_utilisateur_badge_actif FOREIGN KEY (idBadgeActif)
        REFERENCES Badge(idObjet)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_utilisateur_titre_actif FOREIGN KEY (idTitreActif)
        REFERENCES Titre(idObjet)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_utilisateur_theme_actif FOREIGN KEY (idThemeActif)
        REFERENCES ThemeProfil(idObjet)
        ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Cours (
    codeCours       VARCHAR(20) PRIMARY KEY,
    nomCours        VARCHAR(150) NOT NULL,
    faculte         VARCHAR(150) NOT NULL,
    CONSTRAINT uq_cours_nom UNIQUE (nomCours)
);

CREATE TABLE IF NOT EXISTS AnneeAcademique (
    codeAnnee       VARCHAR(20) PRIMARY KEY,
    libelle         VARCHAR(50) NOT NULL,
    CONSTRAINT uq_annee_libelle UNIQUE (libelle)
);

CREATE TABLE IF NOT EXISTS TransactionPoints (
    idTransaction       INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    dateTransaction     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    montantPoints       INT UNSIGNED NOT NULL,
    natureTransaction   ENUM('gain','depense') NOT NULL,
    motif               VARCHAR(255) NOT NULL,
    idUtilisateur       INT UNSIGNED NOT NULL,
    CONSTRAINT ck_transaction_montant CHECK (montantPoints >= 1),
    CONSTRAINT fk_transaction_utilisateur FOREIGN KEY (idUtilisateur)
        REFERENCES Utilisateur(idUtilisateur)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Resume (
    idResume         INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    titre            VARCHAR(200) NOT NULL,
    description      TEXT NOT NULL,
    datePublication  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    version          INT UNSIGNED NOT NULL DEFAULT 1,
    visibilite       ENUM('publique','privee') NOT NULL DEFAULT 'publique',
    idUtilisateur    INT UNSIGNED NOT NULL,
    codeCours        VARCHAR(20) NOT NULL,
    codeAnnee        VARCHAR(20) NOT NULL,
    CONSTRAINT ck_resume_version CHECK (version >= 1),
    CONSTRAINT fk_resume_utilisateur FOREIGN KEY (idUtilisateur)
        REFERENCES Utilisateur(idUtilisateur)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_resume_cours FOREIGN KEY (codeCours)
        REFERENCES Cours(codeCours)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_resume_annee FOREIGN KEY (codeAnnee)
        REFERENCES AnneeAcademique(codeAnnee)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

/* ------------------------------ ASSOCIATIONS ------------------------------ */
CREATE TABLE IF NOT EXISTS Evalue (
    idUtilisateur    INT UNSIGNED NOT NULL,
    idResume         INT UNSIGNED NOT NULL,
    note             TINYINT UNSIGNED NOT NULL,
    commentaire      VARCHAR(1000) NULL,
    dateEvaluation   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (idUtilisateur, idResume),
    CONSTRAINT ck_evalue_note CHECK (note BETWEEN 1 AND 5),
    CONSTRAINT fk_evalue_utilisateur FOREIGN KEY (idUtilisateur)
        REFERENCES Utilisateur(idUtilisateur)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_evalue_resume FOREIGN KEY (idResume)
        REFERENCES Resume(idResume)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS EstDonnePendant (
    codeCours        VARCHAR(20) NOT NULL,
    codeAnnee        VARCHAR(20) NOT NULL,
    PRIMARY KEY (codeCours, codeAnnee),
    CONSTRAINT fk_est_donne_cours FOREIGN KEY (codeCours)
        REFERENCES Cours(codeCours)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_est_donne_annee FOREIGN KEY (codeAnnee)
        REFERENCES AnneeAcademique(codeAnnee)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Possede (
    idUtilisateur    INT UNSIGNED NOT NULL,
    idObjet          INT UNSIGNED NOT NULL,
    dateAchat        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (idUtilisateur, idObjet),
    CONSTRAINT fk_possede_utilisateur FOREIGN KEY (idUtilisateur)
        REFERENCES Utilisateur(idUtilisateur)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_possede_objet FOREIGN KEY (idObjet)
        REFERENCES ObjetCosmetique(idObjet)
        ON DELETE CASCADE ON UPDATE CASCADE
);

/* ------------------------------ GARDE-FOU - TRIGGERS MÉTIER ------------------------------ */

-- ⚠️ ATTENTION : CETTE SECTION EST GÉNÉRÉ PAR IA
-- Les triggers suivants sont essentiels pour garantir l'intégrité métier de la base de données. 
-- Toute modification doit être effectuée avec précaution et en comprenant bien les règles métier qu'ils appliquent.

DROP TRIGGER IF EXISTS trg_badge_exclusif_ins;
DROP TRIGGER IF EXISTS trg_titre_exclusif_ins;
DROP TRIGGER IF EXISTS trg_theme_exclusif_ins;
DROP TRIGGER IF EXISTS trg_evalue_verifs_ins;
DROP TRIGGER IF EXISTS trg_possede_date_ins;
DROP TRIGGER IF EXISTS trg_utilisateur_objets_actifs_upd;

DELIMITER $$

/* Exclusivité d'un objet cosmétique : badge OU titre OU thème (jamais plusieurs). */
CREATE TRIGGER trg_badge_exclusif_ins
BEFORE INSERT ON Badge
FOR EACH ROW
BEGIN
    IF EXISTS (SELECT 1 FROM Titre WHERE idObjet = NEW.idObjet)
       OR EXISTS (SELECT 1 FROM ThemeProfil WHERE idObjet = NEW.idObjet) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Objet deja classe dans une autre categorie.';
    END IF;
END$$

CREATE TRIGGER trg_titre_exclusif_ins
BEFORE INSERT ON Titre
FOR EACH ROW
BEGIN
    IF EXISTS (SELECT 1 FROM Badge WHERE idObjet = NEW.idObjet)
       OR EXISTS (SELECT 1 FROM ThemeProfil WHERE idObjet = NEW.idObjet) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Objet deja classe dans une autre categorie.';
    END IF;
END$$

CREATE TRIGGER trg_theme_exclusif_ins
BEFORE INSERT ON ThemeProfil
FOR EACH ROW
BEGIN
    IF EXISTS (SELECT 1 FROM Badge WHERE idObjet = NEW.idObjet)
       OR EXISTS (SELECT 1 FROM Titre WHERE idObjet = NEW.idObjet) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Objet deja classe dans une autre categorie.';
    END IF;
END$$

/* Une évaluation doit être postérieure (ou égale) à la publication et interdiction d'auto-évaluation. */
CREATE TRIGGER trg_evalue_verifs_ins
BEFORE INSERT ON Evalue
FOR EACH ROW
BEGIN
    DECLARE v_date_publication DATETIME;
    DECLARE v_auteur INT UNSIGNED;

    SELECT datePublication, idUtilisateur
      INTO v_date_publication, v_auteur
      FROM Resume
     WHERE idResume = NEW.idResume;

    IF NEW.dateEvaluation < v_date_publication THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Date evaluation < date publication.';
    END IF;

    IF NEW.idUtilisateur = v_auteur THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Un utilisateur ne peut pas evaluer son propre resume.';
    END IF;
END$$

/* La date d'achat ne peut pas précéder la date d'inscription. */
CREATE TRIGGER trg_possede_date_ins
BEFORE INSERT ON Possede
FOR EACH ROW
BEGIN
    DECLARE v_date_inscription DATE;

    SELECT dateInscription
      INTO v_date_inscription
      FROM Utilisateur
     WHERE idUtilisateur = NEW.idUtilisateur;

    IF DATE(NEW.dateAchat) < v_date_inscription THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Date achat < date inscription.';
    END IF;
END$$

/* Activation d'objet possible uniquement s'il est possédé par l'utilisateur. */
CREATE TRIGGER trg_utilisateur_objets_actifs_upd
BEFORE UPDATE ON Utilisateur
FOR EACH ROW
BEGIN
    IF NEW.idBadgeActif IS NOT NULL AND NOT EXISTS (
        SELECT 1 FROM Possede
         WHERE idUtilisateur = NEW.idUtilisateur
           AND idObjet = NEW.idBadgeActif
    ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Badge actif non possede par l utilisateur.';
    END IF;

    IF NEW.idTitreActif IS NOT NULL AND NOT EXISTS (
        SELECT 1 FROM Possede
         WHERE idUtilisateur = NEW.idUtilisateur
           AND idObjet = NEW.idTitreActif
    ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Titre actif non possede par l utilisateur.';
    END IF;

    IF NEW.idThemeActif IS NOT NULL AND NOT EXISTS (
        SELECT 1 FROM Possede
         WHERE idUtilisateur = NEW.idUtilisateur
           AND idObjet = NEW.idThemeActif
    ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Theme actif non possede par l utilisateur.';
    END IF;
END$$

DELIMITER ;
