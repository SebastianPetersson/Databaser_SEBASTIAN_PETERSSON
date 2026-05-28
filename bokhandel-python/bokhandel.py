import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

load_dotenv()

server = os.getenv("DB_SERVER")
database = os.getenv("DB_NAME")

connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

engine = create_engine(
    f"mssql+pyodbc:///?odbc_connect={quote_plus(connection_string)}"
)

search_term = input("Sök efter boktitel: ")

query = text("""
    SELECT 
        b.Titel,
        bu.Butiksnamn,
        ls.Antal
    FROM Böcker b
    JOIN LagerSaldo ls ON b.ISBN13 = ls.ISBN
    JOIN Butiker bu ON ls.ButikID = bu.ID
    WHERE b.Titel LIKE :search
""")

with engine.connect() as connection:
    result = connection.execute(
        query,
        {"search": f"%{search_term}%"}
    )

    books = result.fetchall()

    if books:
        print("\nResultat:")
        for book in books:
            print(
                f"{book.Titel} | "
                f"Butik: {book.Butiksnamn} | "
                f"Antal: {book.Antal}"
            )
    
    else:
        print("Ingen bok hittades.")