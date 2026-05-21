import sqlite3

# nome del file del database
db_name = "spese_personali.db"

def inizializza_database():
    connessione = sqlite3.connect(db_name)
    cursore = connessione.cursor()
    
    # attivo le chiavi esterne per sqlite
    cursore.execute("PRAGMA foreign_keys = ON;")
    
    # creo la tabella delle categorie
    cursore.execute("CREATE TABLE IF NOT EXISTS Categorie (nome TEXT PRIMARY KEY NOT NULL CHECK(nome <> ''));")
    
    # creo la tabella delle spese
    query_spese = "CREATE TABLE IF NOT EXISTS Spese (id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT NOT NULL CHECK(data LIKE '____-__-__'), importo REAL NOT NULL CHECK(importo > 0), nome_categoria TEXT NOT NULL, descrizione TEXT, FOREIGN KEY (nome_categoria) REFERENCES Categorie(nome) ON DELETE RESTRICT);"
    cursore.execute(query_spese)
    
    # creo la tabella dei budget
    query_budget = "CREATE TABLE IF NOT EXISTS Budget (id INTEGER PRIMARY KEY AUTOINCREMENT, mese TEXT NOT NULL CHECK(mese LIKE '____-__'), nome_categoria TEXT NOT NULL, importo_budget REAL NOT NULL CHECK(importo_budget > 0), UNIQUE(mese, nome_categoria), FOREIGN KEY (nome_categoria) REFERENCES Categorie(nome) ON DELETE CASCADE);"
    cursore.execute(query_budget)
    
    connessione.commit()
    connessione.close()

def gestione_categorie():
    print("\n--- GESTIONE CATEGORIE ---")
    nome = input("Inserisci il nome della nuova categoria: ")
    nome = nome.strip().capitalize()
    
    if nome == "":
        print("Errore: Il nome non può essere vuoto.")
        return

    connessione = sqlite3.connect(db_name)
    cursore = connessione.cursor()
    
    # controllo se esiste gia
    cursore.execute("SELECT nome FROM Categorie WHERE nome = ?;", (nome,))
    risultato = cursore.fetchone()
    
    if risultato != None:
        print("La categoria esiste già.")
    else:
        cursore.execute("INSERT INTO Categorie (nome) VALUES (?);", (nome,))
        connessione.commit()
        print("Categoria inserita correttamente.")
        
    connessione.close()

def inserisci_spesa():
    print("\n--- INSERISCI SPESA ---")
    data = input("Inserisci data (YYYY-MM-DD): ")
    data = data.strip()
    
    try:
        importo_str = input("Inserisci importo: ")
        importo = float(importo_str)
    except ValueError:
        print("Errore: devi inserire un numero.")
        return

    if importo <= 0:
        print("Errore: l'importo deve essere maggiore di zero.")
        return

    categoria = input("Inserisci il nome della categoria: ")
    categoria = categoria.strip().capitalize()
    
    descrizione = input("Inserisci descrizione facoltativa: ")
    descrizione = descrizione.strip()
    
    if descrizione == "":
        descrizione = None

    connessione = sqlite3.connect(db_name)
    cursore = connessione.cursor()
    
    cursore.execute("SELECT nome FROM Categorie WHERE nome = ?;", (categoria,))
    risultato = cursore.fetchone()
    
    if risultato == None:
        print("Errore: la categoria non esiste.")
        connessione.close()
        return

    cursore.execute("INSERT INTO Spese (data, importo, nome_categoria, descrizione) VALUES (?, ?, ?, ?);", (data, importo, categoria, descrizione))
    connessione.commit()
    print("Spesa inserita correttamente.")
    connessione.close()

def definisci_budget():
    print("\n--- DEFINISCI BUDGET MENSILE ---")
    mese = input("Inserisci mese (YYYY-MM): ")
    mese = mese.strip()
    
    categoria = input("Inserisci il nome della categoria: ")
    categoria = categoria.strip().capitalize()
    
    try:
        importo_str = input("Inserisci importo del budget: ")
        importo_budget = float(importo_str)
    except ValueError:
        print("Errore: devi inserire un numero.")
        return

    if importo_budget <= 0:
        print("Errore: Il budget deve essere maggiore di zero.")
        return

    connessione = sqlite3.connect(db_name)
    cursore = connessione.cursor()
    
    cursore.execute("SELECT nome FROM Categorie WHERE nome = ?;", (categoria,))
    risultato = cursore.fetchone()
    
    if risultato == None:
        print("Errore: la categoria non esiste.")
        connessione.close()
        return

    # uso on conflict per aggiornare il budget se esiste gia
    cursore.execute("INSERT INTO Budget (mese, nome_categoria, importo_budget) VALUES (?, ?, ?) ON CONFLICT(mese, nome_categoria) DO UPDATE SET importo_budget = excluded.importo_budget;", (mese, categoria, importo_budget))
    connessione.commit()
    print("Budget mensile salvato correttamente.")
    connessione.close()

def visualizza_report():
    connessione = sqlite3.connect(db_name)
    cursore = connessione.cursor()
    
    while True:
        print("\n--- MENU DEI REPORT ---")
        print("1. Totale spese per categoria")
        print("2. Spese mensili vs budget")
        print("3. Elenco completo delle spese ordinate per data")
        print("4. Ritorna al menu principale")
        
        scelta = input("Inserisci la tua scelta: ")
        scelta = scelta.strip()
        
        match scelta:
            case "1":
                cursore.execute("SELECT nome_categoria, SUM(importo) FROM Spese GROUP BY nome_categoria;")
                righe = cursore.fetchall()
                print("\nCategoria - Totale Speso")
                for riga in righe:
                    print(f"{riga[0]} : {riga[1]}")
                    
            case "2":
                query_report = "SELECT b.mese, b.nome_categoria, b.importo_budget, IFNULL(SUM(s.importo), 0) as speso FROM Budget b LEFT JOIN Spese s ON b.nome_categoria = s.nome_categoria AND s.data LIKE b.mese || '%' GROUP BY b.mese, b.nome_categoria;"
                cursore.execute(query_report)
                righe = cursore.fetchall()
                for riga in righe:
                    mese = riga[0]
                    cat = riga[1]
                    budget = riga[2]
                    speso = riga[3]
                    
                    if speso > budget:
                        stato = "SUPERAMENTO BUDGET"
                    else:
                        stato = "NEI LIMITI"
                        
                    print(f"\nMese: {mese} | Categoria: {cat} | Budget: {budget} | Speso: {speso} | Stato: {stato}")
                    
            case "3":
                cursore.execute("SELECT data, nome_categoria, importo, descrizione FROM Spese ORDER BY data ASC;")
                righe = cursore.fetchall()
                print("\nElenco Spese:")
                for riga in righe:
                    desc = riga[3]
                    if desc == None:
                        desc = "Nessuna descrizione"
                    print(f"{riga[0]} - {riga[1]} - {riga[2]} euro - {desc}")
                    
            case "4":
                break
                
            case _:
                print("Scelta non valida. Riprovare.")
                
    connessione.close()

def main():
    inizializza_database()
    print("=========================================")
    print("   BENVENUTO NEL SISTEMA GESTIONE SPESE  ")
    print("=========================================")
    
    while True:
        print("\nSISTEMA SPESE PERSONALI")
        print("1. Gestione Categorie")
        print("2. Inserisci Spesa")
        print("3. Definisci Budget Mensile")
        print("4. Visualizza Report")
        print("5. Esci")
        
        scelta = input("Inserisci la tua scelta: ")
        scelta = scelta.strip()
        
        match scelta:
            case "1":
                gestione_categorie()
            case "2":
                inserisci_spesa()
            case "3":
                definisci_budget()
            case "4":
                visualizza_report()
            case "5":
                print("Arrivederci!")
                break
            case _:
                print("Scelta non valida. Riprovare.")

if __name__ == "__main__":
    main()
