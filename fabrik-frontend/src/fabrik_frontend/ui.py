import tkinter as tk
from tkinter import ttk, messagebox
import fabrik_frontend.api as api

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Fabrik Demo - THGA Bochum")
        self.root.geometry("900x650")
        nb = ttk.Notebook(root)
        nb.pack(fill="both", expand=True, padx=10, pady=10)
        t1 = ttk.Frame(nb)
        nb.add(t1, text="Teile")
        ttk.Button(t1, text="Aktualisieren", command=self.teile_laden).pack(pady=5)
        self.tree_teile = ttk.Treeview(t1, columns=("ID","Name","Einheit","Bestand","Mindest","Status"), show="headings")
        for col in ("ID","Name","Einheit","Bestand","Mindest","Status"):
            self.tree_teile.heading(col, text=col)
            self.tree_teile.column(col, width=130)
        self.tree_teile.pack(fill="both", expand=True, padx=5, pady=5)
        t2 = ttk.Frame(nb)
        nb.add(t2, text="Produkte")
        ttk.Button(t2, text="Aktualisieren", command=self.produkte_laden).pack(pady=5)
        self.tree_prod = ttk.Treeview(t2, columns=("ID","Name","Bestand","Produziert","Ausgecheckt"), show="headings")
        for col in ("ID","Name","Bestand","Produziert","Ausgecheckt"):
            self.tree_prod.heading(col, text=col)
            self.tree_prod.column(col, width=160)
        self.tree_prod.pack(fill="both", expand=True, padx=5, pady=5)
        t3 = ttk.Frame(nb)
        nb.add(t3, text="Wareneingang")
        ttk.Label(t3, text="Teil-ID:").pack(pady=2)
        self.e_teil = ttk.Entry(t3)
        self.e_teil.pack()
        ttk.Label(t3, text="Menge:").pack(pady=2)
        self.e_menge = ttk.Entry(t3)
        self.e_menge.pack()
        ttk.Button(t3, text="Buchen", command=self.wareneingang).pack(pady=10)
        t4 = ttk.Frame(nb)
        nb.add(t4, text="Produktion")
        ttk.Label(t4, text="Produkt-ID:").pack(pady=2)
        self.e_prod = ttk.Entry(t4)
        self.e_prod.pack()
        ttk.Label(t4, text="Menge:").pack(pady=2)
        self.e_prod_menge = ttk.Entry(t4)
        self.e_prod_menge.pack()
        ttk.Button(t4, text="Produzieren", command=self.produktion).pack(pady=10)
        t5 = ttk.Frame(nb)
        nb.add(t5, text="Lagerausgang")
        ttk.Label(t5, text="Produkt-ID:").pack(pady=2)
        self.e_lager = ttk.Entry(t5)
        self.e_lager.pack()
        ttk.Label(t5, text="Menge:").pack(pady=2)
        self.e_lager_menge = ttk.Entry(t5)
        self.e_lager_menge.pack()
        ttk.Button(t5, text="Ausbuchen", command=self.lagerausgang).pack(pady=10)
        ts = ttk.Frame(nb)
        nb.add(ts, text="Stueckliste")
        ttk.Label(ts, text="Produkt-ID:").pack(pady=2)
        self.e_stueck = ttk.Entry(ts)
        self.e_stueck.pack()
        ttk.Button(ts, text="Laden", command=self.stueckliste_laden).pack(pady=5)
        self.tree_stueck = ttk.Treeview(ts, columns=("Teil","Menge","Einheit"), show="headings")
        for col in ("Teil","Menge","Einheit"):
            self.tree_stueck.heading(col, text=col)
            self.tree_stueck.column(col, width=200)
        self.tree_stueck.pack(fill="both", expand=True, padx=5, pady=5)
        t6 = ttk.Frame(nb)
        nb.add(t6, text="Bestellwarnungen")
        ttk.Button(t6, text="Aktualisieren", command=self.warnungen_laden).pack(pady=5)
        self.tree_warn = ttk.Treeview(t6, columns=("ID","Teil","Bestand","Mindest","Zeitstempel"), show="headings")
        for col in ("ID","Teil","Bestand","Mindest","Zeitstempel"):
            self.tree_warn.heading(col, text=col)
            self.tree_warn.column(col, width=160)
        self.tree_warn.pack(fill="both", expand=True, padx=5, pady=5)
        self.teile_laden()
        self.produkte_laden()

    def teile_laden(self):
        for r in self.tree_teile.get_children(): self.tree_teile.delete(r)
        for t in api.get_teile():
            self.tree_teile.insert("","end",values=(t["id"],t["name"],t["einheit"],t["bestand"],t["mindestbestand"],"!" if t["unter_mindestbestand"] else "OK"))

    def produkte_laden(self):
        for r in self.tree_prod.get_children(): self.tree_prod.delete(r)
        for p in api.get_produkte():
            self.tree_prod.insert("","end",values=(p["id"],p["name"],p["bestand"],p["gesamt_produziert"],p["gesamt_ausgecheckt"]))

    def stueckliste_laden(self):
        pid = self.e_stueck.get()
        if not pid: messagebox.showerror("Fehler","Bitte Produkt-ID angeben"); return
        for r in self.tree_stueck.get_children(): self.tree_stueck.delete(r)
        for s in api.get_stueckliste(int(pid)):
            self.tree_stueck.insert("","end",values=(s["teil_name"],s["menge"],s["einheit"]))

    def warnungen_laden(self):
        for r in self.tree_warn.get_children(): self.tree_warn.delete(r)
        for w in api.get_bestellwarnungen():
            self.tree_warn.insert("","end",values=(w["id"],w["teil_name"],w["bestand"],w["mindestbestand"],w["zeitstempel"]))

    def wareneingang(self):
        tid,m = self.e_teil.get(),self.e_menge.get()
        if not tid or not m: messagebox.showerror("Fehler","Bitte Teil-ID und Menge angeben"); return
        r = api.wareneingang(int(tid),int(m))
        if r.status_code==200: messagebox.showinfo("Erfolg","Wareneingang gebucht!"); self.teile_laden()
        else: messagebox.showerror("Fehler",r.text)

    def produktion(self):
        pid,m = self.e_prod.get(),self.e_prod_menge.get()
        if not pid or not m: messagebox.showerror("Fehler","Bitte Produkt-ID und Menge angeben"); return
        r = api.produktion(int(pid),int(m))
        if r.status_code==200: messagebox.showinfo("Erfolg","Produktion gebucht!"); self.teile_laden(); self.produkte_laden()
        else: messagebox.showerror("Fehler",r.text)

    def lagerausgang(self):
        pid,m = self.e_lager.get(),self.e_lager_menge.get()
        if not pid or not m: messagebox.showerror("Fehler","Bitte Produkt-ID und Menge angeben"); return
        r = api.lagerausgang(int(pid),int(m))
        if r.status_code==200: messagebox.showinfo("Erfolg","Lagerausgang gebucht!"); self.produkte_laden()
        else: messagebox.showerror("Fehler",r.text)
