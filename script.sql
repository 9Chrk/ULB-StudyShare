/*------------------------------ PARAMÈTRES GÉNÉRAUX ------------------------------*/
SET NAMES utf8mb4;
SET sql_mode = 'STRICT_ALL_TABLES';

CREATE DATABASE IF NOT EXISTS KingdomDB
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;
USE KingdomDB;


/*------------------------------ TABLES PRINCIPALES ------------------------------*/
CREATE TABLE IF NOT EXISTS Utilisateur (
  NomUtilisateur   VARCHAR(50) NOT NULL UNIQUE  PRIMARY KEY,
  MotDePasse       VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Joueur (
  ID               INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  NomUtilisateur   VARCHAR(50) NOT NULL UNIQUE,
  Niveau           INT  NOT NULL CHECK (Niveau BETWEEN 1 AND 50),
  XP               INT  NOT NULL CHECK (XP BETWEEN 0 AND 200000),
  Monnaie          INT  NOT NULL CHECK (Monnaie BETWEEN 0 AND 10000),
  SlotsInventaire  INT  NOT NULL CHECK (SlotsInventaire BETWEEN 1 AND 100)
);

CREATE TABLE IF NOT EXISTS Inventaire (
  ID        INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  Capacite  INT NOT NULL CHECK (Capacite BETWEEN 1 AND 100)
);

CREATE TABLE IF NOT EXISTS Personnage (
  ID            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  Nom           VARCHAR(50) NOT NULL,
  Classe        VARCHAR(50) NOT NULL,
  `Force`         INT NOT NULL CHECK (`Force` BETWEEN 1 AND 25),
  Agilite       INT NOT NULL CHECK (Agilite BETWEEN 1 AND 25),
  Intelligence  INT NOT NULL CHECK (Intelligence BETWEEN 1 AND 25),
  Vie           INT NOT NULL CHECK (Vie BETWEEN 1 AND 150),
  Mana          INT NOT NULL CHECK (Mana BETWEEN 1 AND 150),
  ID_Joueur     INT UNSIGNED,
  ID_Inv        INT UNSIGNED,
  FOREIGN KEY (ID_Joueur) REFERENCES Joueur(ID),
  FOREIGN KEY (ID_Inv)    REFERENCES Inventaire(ID)
);

CREATE TABLE IF NOT EXISTS Sort (
  ID                INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  Nom               VARCHAR(50),
  CoutMana          INT NOT NULL CHECK (CoutMana BETWEEN 1 AND 100),
  TempsRecharge     INT NOT NULL CHECK (TempsRecharge BETWEEN 1 AND 20),
  PuissanceAttaque  INT NOT NULL CHECK (PuissanceAttaque BETWEEN 1 AND 150)
);

CREATE TABLE IF NOT EXISTS Recompense (
  ID        INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  Type      ENUM('OR','OBJET') NOT NULL,
  Quantite  INT NOT NULL CHECK (Quantite > 0),
  NomObjet  VARCHAR(50) NULL,
  CHECK ( (Type='OR'    AND NomObjet IS NULL) OR
          (Type='OBJET' AND NomObjet IS NOT NULL) )
);

CREATE TABLE IF NOT EXISTS Monstre(
  ID       INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  Nom      VARCHAR(50),
  Attaque  INT NOT NULL CHECK (Attaque BETWEEN 1 AND 100),
  Defense  INT NOT NULL CHECK (Defense BETWEEN 1 AND 100),
  Vie      INT NOT NULL CHECK (Vie BETWEEN 1 AND 150)
);

CREATE TABLE IF NOT EXISTS Quete (
  Nom         VARCHAR(50) PRIMARY KEY,
  Description VARCHAR(255) NOT NULL,
  Difficulte  INT NOT NULL CHECK (Difficulte BETWEEN 1 AND 10),
  XPGain      INT NOT NULL,
  OrGain      INT NOT NULL CHECK (OrGain > 0)
);

CREATE TABLE IF NOT EXISTS Objet (
  ID   INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  Nom  VARCHAR(50) NOT NULL,
  Prix INT NOT NULL CHECK (Prix > 0)
);

CREATE TABLE IF NOT EXISTS PNJ (
  Nom      VARCHAR(50) PRIMARY KEY,
  Dialogue VARCHAR(255) NOT NULL,
  ID_Inv  INT UNSIGNED,
  FOREIGN KEY (ID_Inv) REFERENCES Inventaire(ID)
);


/*------------------------------ SOUS TABLES ------------------------------*/
CREATE TABLE IF NOT EXISTS Arme (
  ID_Obj           INT UNSIGNED PRIMARY KEY,
  PuissanceAttaque INT NOT NULL CHECK (PuissanceAttaque BETWEEN 1 AND 100),
  FOREIGN KEY (ID_Obj) REFERENCES Objet(ID)
);

CREATE TABLE IF NOT EXISTS Armure (
  ID_Obj  INT UNSIGNED PRIMARY KEY,
  Defense INT NOT NULL CHECK (Defense BETWEEN 1 AND 100),
  FOREIGN KEY (ID_Obj) REFERENCES Objet(ID)
);

CREATE TABLE IF NOT EXISTS Potion (
  ID_Obj INT UNSIGNED PRIMARY KEY,
  Soin   INT NOT NULL CHECK (Soin BETWEEN 1 AND 100),
  FOREIGN KEY (ID_Obj) REFERENCES Objet(ID)
);

CREATE TABLE IF NOT EXISTS Artefact (
  ID_Obj INT UNSIGNED PRIMARY KEY,
  Effet  VARCHAR(100) NOT NULL,
  FOREIGN KEY (ID_Obj) REFERENCES Objet(ID)
);


/*------------------------------ ASSOCIATIONS ------------------------------*/
CREATE TABLE IF NOT EXISTS PersonnageSort (
  ID_Perso INT UNSIGNED,
  ID_Sort  INT UNSIGNED,
  PRIMARY KEY (ID_Perso, ID_Sort),
  FOREIGN KEY (ID_Perso) REFERENCES Personnage(ID),
  FOREIGN KEY (ID_Sort)  REFERENCES Sort(ID)
);

CREATE TABLE IF NOT EXISTS RecompenseMonstre (
  ID_Recomp   INT UNSIGNED,
  ID_Monstre  INT UNSIGNED,
  Probabilite DECIMAL(3,2) NOT NULL CHECK (Probabilite BETWEEN 0 AND 1),
  PRIMARY KEY (ID_Recomp, ID_Monstre),
  FOREIGN KEY (ID_Recomp) REFERENCES Recompense(ID),
  FOREIGN KEY (ID_Monstre) REFERENCES Monstre(ID)
);

CREATE TABLE IF NOT EXISTS CombatPersonnageMonstre (
  ID_Perso     INT UNSIGNED,
  ID_Monstre   INT UNSIGNED,
  Victoire     BOOLEAN NOT NULL,
  DegatSubit   INT NOT NULL,
  ManaConsomme INT NOT NULL,
  PRIMARY KEY (ID_Perso, ID_Monstre),
  FOREIGN KEY (ID_Perso)   REFERENCES Personnage(ID),
  FOREIGN KEY (ID_Monstre) REFERENCES Monstre(ID)
);

CREATE TABLE IF NOT EXISTS PersonnageQuete (
  ID_Perso INT UNSIGNED,
  ID_Quete VARCHAR(50),
  PRIMARY KEY (ID_Perso, ID_Quete),
  FOREIGN KEY (ID_Perso) REFERENCES Personnage(ID),
  FOREIGN KEY (ID_Quete) REFERENCES Quete(Nom)
);

CREATE TABLE IF NOT EXISTS RecompenseQuete (
  ID_Recomp INT UNSIGNED,
  ID_Quete  VARCHAR(50),
  PRIMARY KEY (ID_Recomp, ID_Quete),
  FOREIGN KEY (ID_Recomp) REFERENCES Recompense(ID),
  FOREIGN KEY (ID_Quete)  REFERENCES Quete(Nom)
);

CREATE TABLE IF NOT EXISTS PersonnageObjet (
  ID_Perso    INT UNSIGNED,
  ID_Objet    INT UNSIGNED,
  Emplacement INT NOT NULL CHECK (Emplacement BETWEEN 1 AND 4),
  PRIMARY KEY (ID_Perso, Emplacement),
  FOREIGN KEY (ID_Perso) REFERENCES Personnage(ID),
  FOREIGN KEY (ID_Objet) REFERENCES Objet(ID)
);

CREATE TABLE IF NOT EXISTS ObjetInventaire (
  ID_Objet INT UNSIGNED,
  ID_Inv   INT UNSIGNED,
  Quantite INT NOT NULL CHECK (Quantite >= 1),
  PRIMARY KEY (ID_Objet, ID_Inv),
  FOREIGN KEY (ID_Objet) REFERENCES Objet(ID),
  FOREIGN KEY (ID_Inv)   REFERENCES Inventaire(ID)
);

CREATE TABLE IF NOT EXISTS QuetePNJ (
  NomQuete VARCHAR(50),
  NomPNJ   VARCHAR(50),
  PRIMARY KEY (NomQuete, NomPNJ),
  FOREIGN KEY (NomQuete) REFERENCES Quete(Nom),
  FOREIGN KEY (NomPNJ)   REFERENCES PNJ(Nom)
);

CREATE TABLE IF NOT EXISTS ObjetPNJ (
  ID_Obj INT UNSIGNED,
  Nom    VARCHAR(50),
  PRIMARY KEY (ID_Obj, Nom),
  FOREIGN KEY (ID_Obj) REFERENCES Objet(ID),
  FOREIGN KEY (Nom)    REFERENCES PNJ(Nom)
);
