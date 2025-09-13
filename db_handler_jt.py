import sqlite3
from datetime import datetime

DB_NAME = 'foglalasok.db'

def adatbazis_beallitasa():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS foglalasok (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vezeteknev TEXT NOT NULL,
            keresztnev TEXT NOT NULL,
            szolgaltatas TEXT NOT NULL,
            kezdes_ido TEXT NOT NULL,
            vege_ido TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def foglalasok_lekerdezese(nap: datetime.date):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    query = "SELECT id, vezeteknev, keresztnev, szolgaltatas, kezdes_ido, vege_ido FROM foglalasok WHERE kezdes_ido LIKE ? ORDER BY kezdes_ido"
    cursor.execute(query, (nap.strftime('%Y-%m-%d') + '%',))
    bookings = cursor.fetchall()
    conn.close()
    return bookings

def foglalas_hozzaadasa(vezeteknev: str, keresztnev: str, szolgaltatas: str, kezdes_ido: datetime, vege_ido: datetime):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO foglalasok (vezeteknev, keresztnev, szolgaltatas, kezdes_ido, vege_ido)
        VALUES (?, ?, ?, ?, ?)
    ''', (vezeteknev, keresztnev, szolgaltatas, kezdes_ido.strftime('%Y-%m-%d %H:%M'), vege_ido.strftime('%Y-%m-%d %H:%M')))
    conn.commit()
    conn.close()

def foglalas_torlese(booking_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM foglalasok WHERE id = ?", (booking_id,))
    conn.commit()
    conn.close()
