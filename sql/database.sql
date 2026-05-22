-- Abilitazione dei vincoli sulle chiavi esterne per SQLite
PRAGMA foreign_keys = ON;

-- Tabella per salvare i nomi delle categorie
CREATE TABLE Categorie (
    nome TEXT PRIMARY KEY NOT NULL CHECK(nome <> '')
);

-- Tabella per registrare i singoli acquisti
CREATE TABLE Spese (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL CHECK(data LIKE '____-__-__'),
    importo REAL NOT NULL CHECK(importo > 0),
    nome_categoria TEXT NOT NULL,
    descrizione TEXT,
    FOREIGN KEY (nome_categoria) REFERENCES Categorie(nome) ON DELETE RESTRICT
);

-- Tabella per impostare il limite di budget mensile
CREATE TABLE Budget (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mese TEXT NOT NULL CHECK(mese LIKE '____-__'),
    nome_categoria TEXT NOT NULL,
    importo_budget REAL NOT NULL CHECK(importo_budget > 0),
    UNIQUE(mese, nome_categoria),
    FOREIGN KEY (nome_categoria) REFERENCES Categorie(nome) ON DELETE CASCADE
);

-- Inserimento di alcune categorie iniziali di test
INSERT INTO Categorie (nome) VALUES ('Alimentari');
INSERT INTO Categorie (nome) VALUES ('Trasporti');
INSERT INTO Categorie (nome) VALUES ('Salute');

-- Impostazione dei budget mensili di esempio
INSERT INTO Budget (mese, nome_categoria, importo_budget) VALUES ('2026-05', 'Alimentari', 100.00);
INSERT INTO Budget (mese, nome_categoria, importo_budget) VALUES ('2026-05', 'Trasporti', 60.00);

-- Registrazione di alcune spese per verificare i report
INSERT INTO Spese (data, importo, nome_categoria, descrizione) VALUES ('2026-05-15', 45.50, 'Alimentari', 'Spesa Esselunga');
INSERT INTO Spese (data, importo, nome_categoria, descrizione) VALUES ('2026-05-20', 75.50, 'Trasporti', 'Abbonamento mensile treno');
