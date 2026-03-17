import pandas as pd
import sqlite3

def build_database():
    excel_file = "classificacoes_publicadas_sucupira_teste.xlsx"
    database = "qualis.db"

    print(f"Reading file: {excel_file}...")

    try:
        df = pd.read_excel(excel_file)

        print("Cleaning and standardizing data...")
        # Standardize column names to prevent SQL query syntax errors
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        df.dropna(how="all", inplace=True)

        df['área_de_avaliação'] = df['área_de_avaliação'].str.strip()
        df['estrato'] = df['estrato'].str.strip()
        df['título'] = df['título'].str.strip()
        df['issn'] = df['issn'].str.strip()

        # Replaces "/" for "-", so that doesn't break API routes
        df['área_de_avaliação'] = df['área_de_avaliação'].str.replace('/', '-')
        df['área_de_avaliação'] = df['área_de_avaliação'].str.replace('  ', ' ')
        
        print(f"Exporting data to SQLite db: {database}... ")
        connection = sqlite3.connect(database)
        df.to_sql("periodicos", connection, if_exists="replace", index=False)

        # Creating indexes significantly improves API read performance
        cursor = connection.cursor()
        try:
            cursor.execute("CREATE INDEX idx_issn ON periodicos (issn);")
            cursor.execute("CREATE INDEX idx_titulo ON periodicos (título);")
            cursor.execute("CREATE INDEX idx_area ON periodicos (área_de_avaliação);")
            cursor.execute("CREATE INDEX idx_estrato ON periodicos (estrato);")
        except sqlite3.OperationalError:
            print("Warning: Could not create indexes. Verify column names.")
        
        connection.commit()
        connection.close()

        print("Success! Database created and ready for use.")
    except Exception as e:
        print(f"An error occurred during processing: {e}")
    
if __name__ == "__main__":
    build_database()