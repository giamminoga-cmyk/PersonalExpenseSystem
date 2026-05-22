import sqlite3

# Connessione al database (se il file non esiste, lo crea da solo)
conn = sqlite3.connect('spese_personali.db')
cursor = conn.cursor()

def crea_tabelle():
    # Creazione tabella Categorie
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Categorie (
        nome TEXT PRIMARY KEY
    );
    ''')
    
    # Creazione tabella Spese
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Spese (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT,
        importo REAL CHECK(importo > 0),
        nome_categoria TEXT,
        descrizione TEXT,
        FOREIGN KEY(nome_categoria) REFERENCES Categorie(nome)
    );
    ''')
    
    # Creazione tabella Budget
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Budget (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mese TEXT,
        nome_categoria TEXT,
        importo_budget REAL CHECK(importo_budget > 0),
        FOREIGN KEY(nome_categoria) REFERENCES Categorie(nome)
    );
    ''')
    conn.commit()

def gestione_categorie():
    print("\n--- GESTIONE CATEGORIE ---")
    nome = input("Inserisci il nome della nuova categoria: ")
    try:
        cursor.execute("INSERT INTO Categorie (nome) VALUES (?);", (nome,))
        conn.commit()
        print("Categoria salvata con successo!")
    except:
        print("Errore: Categoria già esistente o problema tecnico.")

def inserisci_spesa():
    print("\n--- INSERISCI SPESA ---")
    data = input("Inserisci la data (AAAA-MM-GG): ")
    importo = input("Inserisci l'importo: ")
    categoria = input("Inserisci il nome della categoria: ")
    descrizione = input("Inserisci una descrizione: ")
    
    try:
        importo_float = float(importo)
        cursor.execute("INSERT INTO Spese (data, importo, nome_categoria, descrizione) VALUES (?, ?, ?, ?);", (data, importo_float, categoria, descrizione))
        conn.commit()
        print("Spesa salvata!")
    except:
        print("Errore: Controlla che l'importo sia maggiore di zero e la categoria esista.")

def definisci_budget():
    print("\n--- DEFINISCI BUDGET MENSILE ---")
    mese = input("Inserisci il mese (AAAA-MM): ")
    categoria = input("Inserisci il nome della categoria: ")
    importo = input("Inserisci l'importo del budget: ")
    
    try:
        importo_float = float(importo)
        cursor.execute("INSERT INTO Budget (mese, nome_categoria, importo_budget) VALUES (?, ?, ?);", (mese, categoria, importo_float))
        conn.commit()
        print("Budget salvato!")
    except:
        print("Errore: Controlla che l'importo sia maggiore di zero e la categoria esista.")

def visualizza_report():
    print("\n--- VISUALIZZA REPORT SPESE ---")
    cursor.execute("SELECT data, importo, nome_categoria, descrizione FROM Spese;")
    spese = cursor.fetchall()
    
    totale = 0
    for s in spese:
        print("Data: " + str(s[0]) + " | Importo: " + str(s[1]) + " | Categoria: " + str(s[2]) + " | Descrizione: " + str(s[3]))
        totale = totale + s[1]
        
    print("TOTALE SPESO: " + str(totale))

    print("\n--- REPORT BUDGET ---")
    cursor.execute("SELECT mese, nome_categoria, importo_budget FROM Budget;")
    budget_list = cursor.fetchall()
    
    for b in budget_list:
        print("Mese: " + str(b[0]) + " | Categoria: " + str(b[1]) + " | Budget impostato: " + str(b[2]))
    print("-----------------------------\n")

def main():
    crea_tabelle()
    scelta = "0"
    
    while scelta != "5":
        print("\nSISTEMA SPESE PERSONALI")
        print("1. Gestione Categorie")
        print("2. Inserisci Spesa")
        print("3. Definisci Budget Mensile")
        print("4. Visualizza Report")
        print("5. Esci")
        scelta = input("Cosa vuoi fare? Scrivi un numero: ")
        
        if scelta == "1":
            gestione_categorie()
        elif scelta == "2":
            inserisci_spesa()
        elif scelta == "3":
            definisci_budget()
        elif scelta == "4":
            visualizza_report()
        elif scelta == "5":
            print("Programma finito. Ciao!")
        else:
            print("Numero sbagliato, riprova.")

if __name__ == "__main__":
    main()
