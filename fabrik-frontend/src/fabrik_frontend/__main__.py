import tkinter as tk
from fabrik_frontend.connection_dialog import ConnectionDialog
from fabrik_frontend.ui import App

def main():
    root = tk.Tk()
    root.withdraw()
    dialog = ConnectionDialog(root)
    if not dialog.success:
        root.destroy()
        return
    root.deiconify()
    App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
