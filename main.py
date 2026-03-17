from fastapi import FastAPI, HTTPException
import sqlite3

app = FastAPI(
    title="Qualis API",
    description="API para consulta de classificação QUALIS de periódicos da CAPES.",
    version="1.0.0"
)

def get_db_connection():
    # row_factory enables dict-like access to database rows
    conn = sqlite3.connect("qualis.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/areas", summary="Lista todas as áreas de avaliação")
def get_areas():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT DISTINCT área_de_avaliação FROM periodicos WHERE área_de_avaliação IS NOT NULL ORDER BY área_de_avaliação")
    areas = [row["área_de_avaliação"] for row in cursor.fetchall()]
    
    conn.close()
    return {"total": len(areas), "areas": areas}

@app.get("/periodicos/{area}", summary="Buscar periódicos por área")
def get_journals_by_area(area: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT título, issn, estrato FROM periodicos WHERE área_de_avaliação = ?",
        (area,)
    )

    journals = [dict(row) for row in cursor.fetchall()]
    conn.close()

    if not journals:
        raise HTTPException(status_code=404, detail="No journals found for this specific area.")
    
    return {
        "area": area,
        "total_journals": len(journals),
        "journals": journals
    }

@app.get("/periodicos/{area}/{estrato}", summary="Filtrar periódicos por área e classificação")
def filter_journals(area: str, estrato: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT título, issn, estrato FROM periodicos WHERE área_de_avaliação = ? AND estrato = ?",
        (area, estrato.upper())
    )

    journals = [dict(row) for row in cursor.fetchall()]
    conn.close()

    if not journals:
        raise HTTPException(status_code=404, detail="No journals found with these filters.")
    
    return {
        "area": area, 
        "stratum": estrato.upper(), 
        "total": len(journals), 
        "journals": journals
    }