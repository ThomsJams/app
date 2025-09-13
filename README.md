# Fodrászat Időpontfoglaló Rendszer  
Hallgató: Jakab Tamás  
Feladat leírása:  
A projekt egy egyszerű, grafikus felülettel rendelkező időpontfoglaló alkalmazás egy fodrászat számára. A program lehetővé teszi új időpontok rögzítését a szabad helyek függvényében, figyelembe véve a különböző szolgáltatások eltérő időtartamát. A rögzített időpontok listázhatók és törölhetők. A foglalások egy SQLite adatbázisban tárolódnak.  

Modulok és a modulokban használt függvények  
1. Tanult modulok  
tkinter: A grafikus felület (GUI) létrehozásáért és kezeléséért felelős modul.  
tkinter.Tk: A fő ablak objektum.  
tkinter.StringVar: Változók tárolására a GUI elemekben.  
tkinter.ttk.Frame, tkinter.ttk.LabelFrame, tkinter.ttk.Label, tkinter.ttk.Entry, tkinter.ttk.Combobox, tkinter.ttk.Button, tkinter.ttk.Treeview, tkinter.ttk.Scrollbar, tkinter.ttk.Style: A felület elemei.  
tkinter.messagebox: Felugró ablakok (információs, figyelmeztető, kérdés) kezelésére.  
showinfo(), showwarning(), askyesno()
sqlite3: Az SQLite adatbázis kezeléséhez használt modul.  
connect(): Kapcsolódás az adatbázisfájlhoz.
cursor(): Kurzor objektum létrehozása SQL parancsok futtatásához.  
execute(): SQL parancs futtatása.  
fetchall(): A lekérdezés eredményének beolvasása.  
commit(): Tranzakció véglegesítése.  
close(): Kapcsolat bezárása.

3. Bemutatandó modul  
datetime: Dátum- és időkezelési feladatokhoz.  
datetime.now(): Az aktuális dátum és idő lekérdezése.  
datetime.combine(): Dátum és idő objektumok összefűzése.  
timedelta: Időtartamok reprezentálására és időponthoz való hozzáadásra (pl. egy szolgáltatás hosszának hozzáadása a kezdési időponthoz).

5. Saját modul  
db_handler_jt: Saját készítésű modul, ami az adatbázis-kezelési logikát foglalja magába.  
adatbazis_beallitasa(): Létrehozza az adatbázist és a táblát, ha nem léteznek.  
foglalasok_lekerdezese(): Lekérdezi egy adott nap foglalásait.  
foglalas_hozzaadasa(): Új foglalást ad az adatbázishoz.  
foglalas_torlese(): Töröl egy foglalást azonosító alapján.  
config: A program beállításait (szolgáltatások, munkaidő) tartalmazó modul.

Osztály(ok)  
FoglaloAppJT: A program fő osztálya, amely a tkinter.Tk-ból öröklődik. Ez az osztály felelős a teljes grafikus felület felépítéséért, az eseménykezelésért (gombnyomások, kiválasztások), és a program logikájának összefogásáért.  

Saját függvény
format_nev_jt(vezeteknev, keresztnev): A main.py fájlban definiált önálló függvény. A feladata, hogy a bemenetként kapott vezeték- és keresztnevet formázza: eltávolítja a felesleges szóközöket és nagy kezdőbetűssé alakítja őket.  
