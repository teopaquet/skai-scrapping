
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os

class ScraperApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LinkedIn Airline Scraper")
        self.geometry("400x400")
        self.create_widgets()

    def create_widgets(self):
        # Fleet size
        ttk.Label(self, text="Min Fleet Size:").pack(pady=5)
        self.min_fleet = tk.IntVar(value=2)
        ttk.Entry(self, textvariable=self.min_fleet).pack()

        ttk.Label(self, text="Max Fleet Size:").pack(pady=5)
        self.max_fleet = tk.IntVar(value=25)
        ttk.Entry(self, textvariable=self.max_fleet).pack()

        # Tranche index
        ttk.Label(self, text="Start Index (for 50):").pack(pady=5)
        self.start_index = tk.IntVar(value=0)
        ttk.Entry(self, textvariable=self.start_index).pack()

        ttk.Label(self, text="End Index (for 50):").pack(pady=5)
        self.end_index = tk.IntVar(value=50)
        ttk.Entry(self, textvariable=self.end_index).pack()

        # Nombre de requêtes
        ttk.Label(self, text="Nombre de requêtes (1/5/10/50/100/0):").pack(pady=5)
        self.nb_requetes = tk.IntVar(value=10)
        ttk.Entry(self, textvariable=self.nb_requetes).pack()

        # Rôle
        ttk.Label(self, text="Rôle à rechercher:").pack(pady=5)
        self.role = tk.StringVar(value="Crew Planner")
        ttk.Entry(self, textvariable=self.role).pack()

        # Bouton lancer
        ttk.Button(self, text="Lancer le scraping", command=self.launch_scraping).pack(pady=20)


    def launch_scraping(self):
        # Récupérer les valeurs
        params = {
            'min_fleet_size': self.min_fleet.get(),
            'max_fleet_size': self.max_fleet.get(),
            'start_index': self.start_index.get(),
            'end_index': self.end_index.get(),
            'nb_requetes': self.nb_requetes.get(),
            'role': self.role.get(),
        }
        # messagebox.showinfo("Paramètres", f"Lancement avec :\n{params}")

        # Appeler le script linkedin_scraper.py avec les paramètres en arguments
        script_path = os.path.join(os.path.dirname(__file__), 'linkedin_scraper.py')
        cmd = [sys.executable, script_path,
               str(params['min_fleet_size']),
               str(params['max_fleet_size']),
               str(params['start_index']),
               str(params['end_index']),
               str(params['nb_requetes']),
               params['role']]
        try:
            subprocess.run(cmd, check=True)
            messagebox.showinfo("Succès", "Scraping terminé !")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Erreur", f"Erreur lors du scraping : {e}")

if __name__ == "__main__":
    app = ScraperApp()
    app.mainloop()
