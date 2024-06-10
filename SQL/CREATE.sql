/*
	Author: Marc-Andre Bossanyi 
	Email: ma.bossanyi@gmail.com
	Creation Date: 2024/04/28
	Last Updated: 2024/06/09
*/

-- Script CREATE for the table "Rarity"
CREATE TABLE Rarity(
	idRarity SERIAL NOT NULL, 
	name VARCHAR(64) NOT NULL, 
	numberStars INT NOT NULL, 
	isDeleted BOOL NOT NULL, 
	CONSTRAINT pk_idRarity PRIMARY KEY (idRarity)
); 


-- Script CREATE for the table "Element"
CREATE TABLE Element(
	idElement SERIAL NOT NULL, 
	name VARCHAR(64) NOT NULL, 
	color VARCHAR(64) NOT NULL, 
	isDeleted BOOL NOT NULL, 
	CONSTRAINT pk_idElement PRIMARY KEY (idElement)
); 


-- Script CREATE for the table "Affiliation"
CREATE TABLE Affiliation(
	idAffiliation SERIAL NOT NULL,
	name VARCHAR(64) NOT NULL,
	isDeleted BOOL NOT NULL,
	CONSTRAINT pk_idAffiliation PRIMARY KEY (idAffiliation)
);


-- Script CREATE for the table "Role"
CREATE TABLE Role(
	idRole SERIAL NOT NULL, 
	name VARCHAR(64) NOT NULL, 
	isDeleted BOOL NOT NULL, 
	CONSTRAINT pk_idRole PRIMARY KEY (idRole)
); 


-- Script CREATE for the table "Mythology"
CREATE TABLE Mythology(
	idMythology SERIAL NOT NULL, 
	name VARCHAR(64) NOT NULL, 
	isDeleted BOOL NOT NULL, 
	CONSTRAINT pk_idMythology PRIMARY KEY (idMythology)
);


-- Script CREATE for the table "Esper"
CREATE TABLE Esper(
	idEsper SERIAL NOT NULL,
	name VARCHAR(64) NOT NULL, 
	idRarity INT NOT NULL, 
	idElement INT NOT NULL, 
	idRole INT NOT NULL, 
	idMythology INT NOT NULL, 
	idAffiliation INT NOT NULL,
	version VARCHAR(16) NOT NULL,
	age INT NOT NULL, 
	birthday DATE NOT NULL, 
	isOwned BOOL NOT NULL, 
	isDeleted BOOL NOT NULL, 
	maxHp INT NOT NULL,
	maxAtk INT NOT NULL, 
	maxDef INT NOT NULL, 
	spd INT NOT NULL, 
	cRate INT NOT NULL, 
	cDmg INT NOT NULL, 
	acc INT NOT NULL, 
	resist INT NOT NULL,
	CONSTRAINT pk_idEsper PRIMARY KEY (idEsper), 
	CONSTRAINT fk_idRarity FOREIGN KEY (idRarity) REFERENCES Rarity(idRarity), 
	CONSTRAINT fk_idElement FOREIGN KEY (idElement) REFERENCES Element(idElement), 
	CONSTRAINT fk_idRole FOREIGN KEY (idRole) REFERENCES Role(idRole), 
	CONSTRAINT fk_idMythology FOREIGN KEY (idMythology) REFERENCES Mythology(idMythology), 
	CONSTRAINT fk_idAffiliation FOREIGN KEY (idAffiliation) REFERENCES Affiliation(idAffiliation)
);


-- Script CREATE for the table "Boss"
CREATE TABLE Boss(
	idBoss SERIAL NOT NULL,
	name VARCHAR(64) NOT NULL, 
	idElement INT NOT NULL, 
	idMythology INT NOT NULL, 
	isDeleted BOOL NOT NULL,
	CONSTRAINT pk_idBoss PRIMARY KEY (idBoss), 
	CONSTRAINT fk_idElement FOREIGN KEY (idElement) REFERENCES Element(idElement), 
	CONSTRAINT fk_idMythology FOREIGN KEY (idMythology) REFERENCES Mythology(idMythology)
);


-- Script CREATE for the table "Relic"
CREATE TABLE Relic(
	idRelic SERIAL NOT NULL, 
	name VARCHAR(64) NOT NULL, 
	description VARCHAR(256) NOT NULL, 
	idBoss INT NOT NULL,
	isDeleted BOOL NOT NULL, 
	CONSTRAINT pk_idRelic PRIMARY KEY (idRelic), 
	CONSTRAINT fk_idBoss FOREIGN KEY (idBoss) REFERENCES Boss(idBoss)
); 


-- Script CREATE for the table "EsperRelic"
CREATE TABLE EsperRelic(
	idEsperRelic SERIAL NOT NULL, 
	idEsper INT NOT NULL, 
	idFourPiecesRelic INT NOT NULL,
	idTwoPiecesRelic INT NOT NULL,
	CONSTRAINT pk_idEsperRelic PRIMARY KEY (idEsperRelic), 
	CONSTRAINT fk_idEsper FOREIGN KEY (idEsper) REFERENCES Esper(idEsper), 
	CONSTRAINT fk_idFourPiecesRelic FOREIGN KEY (idFourPiecesRelic) REFERENCES Relic(idRelic),
	CONSTRAINT fk_idTwoPiecesRelic FOREIGN KEY (idTwoPiecesRelic) REFERENCES Relic(idRelic)
);