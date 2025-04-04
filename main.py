import tkinter as tk
from tkinter import ttk
import json

class AVSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AVS - Aizliegto Vielu Saraksts")
        self.root.geometry("800x500")

        self.json_data = '''
        {
            "vielas": [
                {
                    "id": 1,
                    "nosaukums": "Heroīns",
                    "apraksts": "Ļoti stipri opioīds, izraisa ātru atkarību",
                    "klasifikacija": "I kategorija",
                    "sodamiba": "Līdz 15 gadiem ieslodzījumā",
                    "bistamiba": "Ļoti augsta"
                },
                {
                    "id": 2,
                    "nosaukums": "Kokains",
                    "apraksts": "Stipri stimulējoša viela, iegūta no kokas krūma",
                    "klasifikacija": "I kategorija",
                    "sodamiba": "Līdz 10 gadiem ieslodzījumā",
                    "bistamiba": "Augsta"
                },
                {
                    "id": 3,
                    "nosaukums": "Amfetamīns",
                    "apraksts": "Sintētisks stimulants, izraisa psihisko atkarību",
                    "klasifikacija": "II kategorija",
                    "sodamiba": "Līdz 8 gadiem ieslodzījumā",
                    "bistamiba": "Vidēja"
                },
                {
                    "id": 4,
                    "nosaukums": "MDMA (Ekstāzī)",
                    "apraksts": "Psihodēlisks stimulants, bieži lietots nakts klubos",
                    "klasifikacija": "II kategorija",
                    "sodamiba": "Līdz 6 gadiem ieslodzījumā",
                    "bistamiba": "Vidēja"
                },
                {
                    "id": 5,
                    "nosaukums": "Kanabiss (Marihuāna)",
                    "apraksts": "Vismazāk kaitīgā psihotropā viela, tomēr aizliegta",
                    "klasifikacija": "III kategorija",
                    "sodamiba": "Līdz 5 gadiem ieslodzījumā",
                    "bistamiba": "Zema"
                }
            ]
        }
        '''
        
        self.create_widgets()
        self.load_data()
    
    def create_widgets(self):
        header_frame = ttk.Frame(self.root)
        header_frame.pack(pady=10, fill="x")

        self.title = ttk.Label(
            header_frame, 
            text="AIZLIEGTO VIELU SARAKSTS (AVS)", 
            font=("Arial", 16, "bold")
        )
        self.title.pack()

        self.display_frame = ttk.Frame(self.root)
        self.display_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(
            self.display_frame, 
            columns=("id", "nosaukums", "apraksts", "klasifikacija", "sodamiba", "bistamiba"), 
            show="headings"
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("nosaukums", text="Nosaukums")
        self.tree.heading("apraksts", text="Apraksts")
        self.tree.heading("klasifikacija", text="Klasifikācija")
        self.tree.heading("sodamiba", text="Sodāmība")
        self.tree.heading("bistamiba", text="Bīstamība")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nosaukums", width=120)
        self.tree.column("apraksts", width=250)
        self.tree.column("klasifikacija", width=100, anchor="center")
        self.tree.column("sodamiba", width=150)
        self.tree.column("bistamiba", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(
            self.display_frame, 
            orient="vertical", 
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.status = ttk.Label(
            self.root, 
            text="", 
            relief="sunken", 
            anchor="w"
        )
        self.status.pack(fill="x", padx=5, pady=5)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=5)

        refresh_btn = ttk.Button(
            button_frame,
            text="ATJAUNINĀT DATUS",
            command=self.load_data
        )
        refresh_btn.pack(side="left", padx=5)

        new_window_btn = ttk.Button(
            button_frame,
            text="PALĪDZĪBA",
            command=self.open_help_window
        )
        new_window_btn.pack(side="left", padx=5)
    
    def open_help_window(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Palīdzības dienesti")
        new_window.geometry("500x300")

        ttk.Label(new_window, text="Atkarību palīdzības dienesti", font=("Arial", 14, "bold")).pack(pady=10)

        help_services = [
            {"Nosaukums": "Narkotiku palīdzības dienests", "Tālrunis": "67037333"},
            {"Nosaukums": "Anonīmie Alkoholiķi Latvijā", "Tālrunis": "25662202"},
            {"Nosaukums": "Narkoloģiskā palīdzība Rīgā", "Tālrunis": "67506017"},
            {"Nosaukums": "Krīzes centrs", "Tālrunis": "116123"},
            {"Nosaukums": "Jauniešu konsultāciju centrs", "Tālrunis": "67222922"}
        ]

        tree = ttk.Treeview(new_window, columns=("Nosaukums", "Tālrunis"), show="headings")
        tree.heading("Nosaukums", text="Nosaukums")
        tree.heading("Tālrunis", text="Tālrunis")
        tree.column("Nosaukums", width=300)
        tree.column("Tālrunis", width=150)

        for service in help_services:
            tree.insert("", "end", values=(service["Nosaukums"], service["Tālrunis"]))

        tree.pack(pady=10, padx=10, fill="both", expand=True)

    def load_data(self):
        try:
            data = json.loads(self.json_data)
            items = data.get("vielas", [])

            for row in self.tree.get_children():
                self.tree.delete(row)

            for item in items:
                self.tree.insert("", "end", values=(
                    item.get("id", ""),
                    item.get("nosaukums", ""),
                    item.get("apraksts", ""),
                    item.get("klasifikacija", ""),
                    item.get("sodamiba", ""),
                    item.get("bistamiba", "")
                ))

            self.status.config(text=f"Ielādētas {len(items)} aizliegtās vielas")

        except Exception as e:
            self.status.config(text=f"Kļūda: {str(e)}", foreground="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = AVSApp(root)
    root.mainloop()
