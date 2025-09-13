import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

from config import SZOLGALTATASOK, MUNKAIDO_KEZDES, MUNKAIDO_VEGE
from db_handler_jt import adatbazis_beallitasa, foglalasok_lekerdezese, foglalas_hozzaadasa, foglalas_torlese


def format_nev_jt(vezeteknev, keresztnev):
    return f"{vezeteknev.strip().capitalize()} {keresztnev.strip().capitalize()}"


class FoglaloAppJT(tk.Tk):
    def __init__(self):
        super().__init__()

        self.SZOLGALTATASOK = SZOLGALTATASOK
        self.munkaido_kezdes = MUNKAIDO_KEZDES
        self.munkaido_vege = MUNKAIDO_VEGE
        self.mai_nap = datetime.now().date()

        self.title("Fodrászat - Időpontfoglaló Rendszer")
        self.geometry("850x550")
        self.minsize(850, 550)

        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))

        self.gui_elemek_letrehozasa()
        self.foglalasok_listajanak_frissitese()

    def gui_elemek_letrehozasa(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        form_frame = ttk.LabelFrame(main_frame, text="Új foglalás rögzítése", padding="15")
        form_frame.grid(row=0, column=0, padx=(0, 20), pady=10, sticky="ns")

        ttk.Label(form_frame, text="Vezetéknév:").grid(row=0, column=0, sticky="w", pady=5)
        self.vezeteknev_entry = ttk.Entry(form_frame, width=30)
        self.vezeteknev_entry.grid(row=0, column=1, sticky="ew", pady=5)

        ttk.Label(form_frame, text="Keresztnév:").grid(row=1, column=0, sticky="w", pady=5)
        self.keresztnev_entry = ttk.Entry(form_frame, width=30)
        self.keresztnev_entry.grid(row=1, column=1, sticky="ew", pady=5)

        ttk.Label(form_frame, text="Szolgáltatás:").grid(row=2, column=0, sticky="w", pady=5)
        self.szolgaltatas_var = tk.StringVar()
        self.szolgaltatas_combo = ttk.Combobox(form_frame, textvariable=self.szolgaltatas_var,
                                               values=list(self.SZOLGALTATASOK.keys()), state="readonly")
        self.szolgaltatas_combo.grid(row=2, column=1, sticky="ew", pady=5)
        self.szolgaltatas_combo.bind("<<ComboboxSelected>>", self.szabad_idopontok_frissitese)

        ttk.Label(form_frame, text="Elérhető időpontok:").grid(row=3, column=0, sticky="w", pady=5)
        self.idopont_var = tk.StringVar()
        self.idopont_combo = ttk.Combobox(form_frame, textvariable=self.idopont_var, state="disabled")
        self.idopont_combo.grid(row=3, column=1, sticky="ew", pady=5)

        book_button = ttk.Button(form_frame, text="Időpont foglalása", command=self.foglalas_leadása)
        book_button.grid(row=4, column=0, columnspan=2, pady=20)

        bookings_frame = ttk.LabelFrame(main_frame, text=f"Mai foglalások ({self.mai_nap.strftime('%Y-%m-%d')})",
                                        padding="15")
        bookings_frame.grid(row=0, column=1, pady=10, sticky="nsew")

        columns = ("id", "nev", "szolgaltatas", "kezdes", "vege")
        self.foglalasok_fa = ttk.Treeview(bookings_frame, columns=columns, show="headings")
        self.foglalasok_fa['displaycolumns'] = ("nev", "szolgaltatas", "kezdes", "vege")

        self.foglalasok_fa.heading("nev", text="Név")
        self.foglalasok_fa.heading("szolgaltatas", text="Szolgáltatás")
        self.foglalasok_fa.heading("kezdes", text="Kezdés")
        self.foglalasok_fa.heading("vege", text="Vége")

        self.foglalasok_fa.column("id", width=0, stretch=tk.NO)
        self.foglalasok_fa.column("nev", width=120)
        self.foglalasok_fa.column("szolgaltatas", width=150)
        self.foglalasok_fa.column("kezdes", width=60, anchor="center")
        self.foglalasok_fa.column("vege", width=60, anchor="center")

        scrollbar = ttk.Scrollbar(bookings_frame, orient=tk.VERTICAL, command=self.foglalasok_fa.yview)
        self.foglalasok_fa.configure(yscroll=scrollbar.set)

        self.foglalasok_fa.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        delete_button = ttk.Button(bookings_frame, text="Kijelölt időpont törlése",
                                   command=self.kijelolt_foglalas_torlese)
        delete_button.pack(pady=10, side=tk.BOTTOM)

        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

    def szabad_idopontok_frissitese(self, event=None):
        kivalasztott_szolgaltatas = self.szolgaltatas_var.get()
        if not kivalasztott_szolgaltatas:
            self.idopont_combo.config(state="disabled", values=[])
            self.idopont_var.set("")
            return

        idotartam_perc = self.SZOLGALTATASOK[kivalasztott_szolgaltatas]

        munkaido_kezdes_ido = datetime.combine(self.mai_nap, datetime.min.time()).replace(hour=self.munkaido_kezdes)
        munkaido_vege_ido = datetime.combine(self.mai_nap, datetime.min.time()).replace(hour=self.munkaido_vege)

        foglalt_idopontok_db = foglalasok_lekerdezese(self.mai_nap)
        foglalt_intervallumok = []
        for foglalas in foglalt_idopontok_db:
            start = datetime.strptime(foglalas[4], '%Y-%m-%d %H:%M')
            end = datetime.strptime(foglalas[5], '%Y-%m-%d %H:%M')
            foglalt_intervallumok.append((start, end))

        szabad_idopontok = []
        lehetseges_kezdes = munkaido_kezdes_ido
        while lehetseges_kezdes < munkaido_vege_ido:
            lehetseges_vege = lehetseges_kezdes + timedelta(minutes=idotartam_perc)

            if lehetseges_vege > munkaido_vege_ido:
                break

            utkozes_van = False
            for foglalt_kezdes, foglalt_vege in foglalt_intervallumok:
                if lehetseges_kezdes < foglalt_vege and lehetseges_vege > foglalt_kezdes:
                    utkozes_van = True
                    break

            if not utkozes_van:
                szabad_idopontok.append(lehetseges_kezdes.strftime("%H:%M"))

            lehetseges_kezdes += timedelta(minutes=15)

        if szabad_idopontok:
            self.idopont_combo.config(state="readonly", values=szabad_idopontok)
            self.idopont_var.set(szabad_idopontok[0])
        else:
            self.idopont_combo.config(state="disabled", values=[])
            self.idopont_var.set("Nincs szabad időpont")

    def foglalas_leadása(self):
        vezeteknev = self.vezeteknev_entry.get()
        keresztnev = self.keresztnev_entry.get()
        szolgaltatas = self.szolgaltatas_var.get()
        ido_str = self.idopont_var.get()

        if not vezeteknev.strip() or not keresztnev.strip() or not szolgaltatas or not ido_str or "Nincs" in ido_str:
            messagebox.showwarning("Hiányos adatok", "Kérem, töltsön ki minden mezőt és válasszon érvényes időpontot!")
            return

        ora, perc = map(int, ido_str.split(':'))
        kezdes_ido = datetime.combine(self.mai_nap, datetime.min.time()).replace(hour=ora, minute=perc)
        idotartam = self.SZOLGALTATASOK[szolgaltatas]
        vege_ido = kezdes_ido + timedelta(minutes=idotartam)

        try:
            foglalas_hozzaadasa(vezeteknev.strip(), keresztnev.strip(), szolgaltatas, kezdes_ido, vege_ido)
            teljes_nev = format_nev_jt(vezeteknev, keresztnev)
            messagebox.showinfo("Sikeres foglalás",
                                f"A foglalás rögzítve!\n\nNév: {teljes_nev}\nIdőpont: {kezdes_ido.strftime('%H:%M')} - {vege_ido.strftime('%H:%M')}")

            self.urlap_uritese()
            self.foglalasok_listajanak_frissitese()
            self.szabad_idopontok_frissitese()

        except Exception as e:
            messagebox.showerror("Adatbázis hiba", f"Hiba történt a foglalás rögzítése során: {e}")

    def foglalasok_listajanak_frissitese(self):
        for item in self.foglalasok_fa.get_children():
            self.foglalasok_fa.delete(item)

        bookings = foglalasok_lekerdezese(self.mai_nap)
        for booking in bookings:
            booking_id = booking[0]
            teljes_nev = format_nev_jt(booking[1], booking[2])
            szolgaltatas_nev = booking[3]
            kezdes_ido_str = datetime.strptime(booking[4], '%Y-%m-%d %H:%M').strftime('%H:%M')
            vege_ido_str = datetime.strptime(booking[5], '%Y-%m-%d %H:%M').strftime('%H:%M')

            self.foglalasok_fa.insert("", tk.END,
                                      values=(booking_id, teljes_nev, szolgaltatas_nev, kezdes_ido_str, vege_ido_str))

    def kijelolt_foglalas_torlese(self):
        selected_item = self.foglalasok_fa.focus()
        if not selected_item:
            messagebox.showwarning("Nincs kijelölés",
                                   "Kérem, először válasszon ki egy időpontot a listából a törléshez!")
            return

        item_details = self.foglalasok_fa.item(selected_item)
        booking_id = item_details['values'][0]
        nev = item_details['values'][1]
        idopont = item_details['values'][3]

        valasz = messagebox.askyesno(
            "Törlés megerősítése",
            f"Biztosan törölni szeretné {nev} foglalását ({idopont})?",
            icon='warning'
        )

        if valasz:
            try:
                foglalas_torlese(booking_id)
                messagebox.showinfo("Siker", "A foglalás sikeresen törölve.")
                self.foglalasok_listajanak_frissitese()
                self.szabad_idopontok_frissitese()
            except Exception as e:
                messagebox.showerror("Hiba", f"Hiba történt a törlés során: {e}")

    def urlap_uritese(self):
        self.vezeteknev_entry.delete(0, tk.END)
        self.keresztnev_entry.delete(0, tk.END)
        self.szolgaltatas_var.set("")
        self.idopont_var.set("")
        self.idopont_combo.config(state="disabled", values=[])


if __name__ == "__main__":
    adatbazis_beallitasa()
    app = FoglaloAppJT()
    app.mainloop()
