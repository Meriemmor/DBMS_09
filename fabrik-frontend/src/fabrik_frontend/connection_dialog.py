import tkinter as tk
from tkinter import ttk
import fabrik_frontend.api as api

class ConnectionDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Verbindung konfigurieren")
        self.resizable(False, False)
        self.success = False
        ttk.Label(self, text="Server-URL:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.url_var = tk.StringVar(value="http://128.140.85.215:8888")
        ttk.Entry(self, textvariable=self.url_var, width=40).grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(self, text="API-Key:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.key_var = tk.StringVar(value="vorlesung2026")
        ttk.Entry(self, textvariable=self.key_var, width=40).grid(row=1, column=1, padx=10, pady=5)
        ttk.Button(self, text="Verbinden", command=self._connect).grid(row=2, column=0, columnspan=2, pady=10)
        self.grab_set()
        self.wait_window()

    def _connect(self):
        api.set_connection(self.url_var.get(), self.key_var.get())
        self.success = True
        self.destroy()
