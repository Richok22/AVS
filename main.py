import tkinter as tk
from tkinter import ttk
import json

class AVSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AVS - Aizliegto Vielu Saraksts")
        self.root.geometry("800x500")
        
        # Sample JSON data with drug-related information
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
        self.load_data()  # Automātiski ielādē datus startējot
    
    def create_widgets(self):
        # Header frame
        header_frame = ttk.Frame(self.root)
        header_frame.pack(pady=10, fill="x")
        
        self.title = ttk.Label(
            header_frame, 
            text="AIZLĪEGTO VIELU SARAKSTS (AVS)", 
            font=("Arial", 16, "bold")
        )
        self.title.pack()
        
        # Pamata displeja zona
        self.display_frame = ttk.Frame(self.root)
        self.display_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Izveido Treeview tabulai
        self.tree = ttk.Treeview(
            self.display_frame, 
            columns=("id", "nosaukums", "apraksts", "klasifikacija", "sodamiba", "bistamiba"), 
            show="headings"
        )
        
        # Konfigurē kolonnas
        self.tree.heading("id", text="ID")
        self.tree.heading("nosaukums", text="Nosaukums")
        self.tree.heading("apraksts", text="Apraksts")
        self.tree.heading("klasifikacija", text="Klasifikācija")
        self.tree.heading("sodamiba", text="Sodāmība")
        self.tree.heading("bistamiba", text="Bīstamība")
        
        # Iestata kolonnu platumus
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nosaukums", width=120)
        self.tree.column("apraksts", width=250)
        self.tree.column("klasifikacija", width=100, anchor="center")
        self.tree.column("sodamiba", width=150)
        self.tree.column("bistamiba", width=100, anchor="center")
        
        # Pievieno ritjoslu
        scrollbar = ttk.Scrollbar(
            self.display_frame, 
            orient="vertical", 
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Izvieto elementus
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Statusa josla
        self.status = ttk.Label(
            self.root, 
            text="", 
            relief="sunken", 
            anchor="w"
        )
        self.status.pack(fill="x", padx=5, pady=5)
        
        # Poga datu atjaunināšanai
        refresh_btn = ttk.Button(
            self.root,
            text="ATJAUNINĀT DATUS",
            command=self.load_data
        )
        refresh_btn.pack(pady=5)
    
    def load_data(self):
        try:
            data = json.loads(self.json_data)
            items = data.get("vielas", [])
            
            # Notīra esošos datus
            for row in self.tree.get_children():
                self.tree.delete(row)
            
            # Ievieto jaunos datus
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

# Izveido un palaiž aplikāciju
if __name__ == "__main__":
    root = tk.Tk()
    app = AVSApp(root)
    root.mainloop()