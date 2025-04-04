import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
import json

class AVSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AVS - Aizliegto Vielu Saraksts")
        self.root.geometry("1000x600")
        self.root.minsize(800, 500)
        
        # Stila konfigurācija
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Moderna tēma
        self.configure_styles()
        
        # Fona krāsas
        self.bg_colors = {
            "Noklusējuma": "#f0f0f0",
            "Gaišs": "#ffffff",
            "Tumšs": "#2d2d2d",
            "Zils": "#e6f3ff",
            "Zaļš": "#e8f5e9"
        }
        self.current_bg = "Noklusējuma"
        
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
        self.change_background(self.current_bg)  # Uzstāda noklusēto fonu
    
    def configure_styles(self):
        """Konfigurē UI elementu stilus"""
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
        self.style.configure('Treeview', font=('Arial', 10), rowheight=25)
        self.style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
        self.style.map('Treeview', background=[('selected', '#347083')])
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        self.style.configure('Status.TLabel', font=('Arial', 9), relief='sunken', padding=5)
        self.style.configure('TMenubutton', font=('Arial', 10))
    
    def create_widgets(self):
        # Galvenais konteiners
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header frame
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill="x", pady=(0, 10))
        
        self.title = ttk.Label(
            header_frame, 
            text="AIZLĪEGTO VIELU SARAKSTS (AVS)", 
            style='Header.TLabel'
        )
        self.title.pack(side='left')
        
        # Kontroles panelis
        control_frame = ttk.Frame(header_frame)
        control_frame.pack(side='right')
        
        # Fona izvēlnes pogas
        self.bg_var = tk.StringVar(value=self.current_bg)
        bg_menu = ttk.OptionMenu(
            control_frame, 
            self.bg_var, 
            self.current_bg, 
            *self.bg_colors.keys(), 
            command=self.change_background
        )
        bg_menu.pack(side='left', padx=5)
        
        # Pielāgotas krāsas poga
        custom_color_btn = ttk.Button(
            control_frame,
            text="Pielāgota krāsa",
            command=self.choose_custom_color
        )
        custom_color_btn.pack(side='left', padx=5)
        
        # Palīdzības poga
        help_btn = ttk.Button(
            control_frame,
            text="Palīdzība",
            command=self.open_help_window
        )
        help_btn.pack(side='left', padx=5)
        
        # Pamata displeja zona
        self.display_frame = ttk.Frame(self.main_frame)
        self.display_frame.pack(fill="both", expand=True)
        
        # Izveido Treeview tabulai
        self.tree = ttk.Treeview(
            self.display_frame, 
            columns=("id", "nosaukums", "apraksts", "klasifikacija", "sodamiba", "bistamiba"), 
            show="headings",
            style='Treeview'
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
        self.tree.column("nosaukums", width=150)
        self.tree.column("apraksts", width=300)
        self.tree.column("klasifikacija", width=120, anchor="center")
        self.tree.column("sodamiba", width=180)
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
            self.main_frame, 
            text="Sagatavots darbam", 
            style='Status.TLabel'
        )
        self.status.pack(fill="x", pady=(5, 0))
        
        # Poga datu atjaunināšanai
        refresh_btn = ttk.Button(
            self.main_frame,
            text="ATJAUNINĀT DATUS",
            command=self.load_data
        )
        refresh_btn.pack(pady=(10, 0))
    
    def change_background(self, bg_name):
        """Maina fona krāsu pēc izvēlētās tēmas"""
        if bg_name in self.bg_colors:
            color = self.bg_colors[bg_name]
            self.current_bg = bg_name
            self.bg_var.set(bg_name)
        else:
            color = bg_name  # Ja tas ir pielāgots krāsas kods
        
        self.main_frame.configure(style='TFrame')
        self.style.configure('TFrame', background=color)
        self.style.configure('TLabel', background=color)
        self.style.configure('Treeview', background='white', fieldbackground='white')
        
        # Pielāgo tekstu tumšam fonam
        if bg_name == "Tumšs":
            self.style.configure('Header.TLabel', background=color, foreground='white')
            self.style.configure('TLabel', background=color, foreground='white')
            self.style.configure('Status.TLabel', background='#3d3d3d', foreground='white')
            self.tree.configure(style='Treeview')
            self.style.map('Treeview', background=[('selected', '#1a5276')])
        else:
            self.style.configure('Header.TLabel', background=color, foreground='#2c3e50')
            self.style.configure('TLabel', background=color, foreground='black')
            self.style.configure('Status.TLabel', background='#e0e0e0', foreground='black')
            self.tree.configure(style='Treeview')
            self.style.map('Treeview', background=[('selected', '#347083')])
    
    def choose_custom_color(self):
        """Atver krāsu izvēlni pielāgotai krāsai"""
        color = colorchooser.askcolor(title="Izvēlieties fona krāsu")
        if color[1]:  # Ja lietotājs izvēlējās krāsu
            self.change_background(color[1])
            self.bg_var.set("Pielāgots")
    
    def open_help_window(self):
        """Atver palīdzības logu ar kontaktu informāciju"""
        help_window = tk.Toplevel(self.root)
        help_window.title("Palīdzības dienesti")
        help_window.geometry("600x400")
        help_window.resizable(False, False)
        
        # Pielāgo stilus palīdzības logam
        bg_color = self.style.lookup('TFrame', 'background')
        help_window.configure(bg=bg_color)
        
        # Galvene
        ttk.Label(
            help_window,
            text="Atkarību palīdzības dienesti",
            style='Header.TLabel'
        ).pack(pady=10)
        
        # Palīdzības dienesti
        help_services = [
            {"Nosaukums": "Narkotiku palīdzības dienests", "Tālrunis": "67037333"},
            {"Nosaukums": "Anonīmie Alkoholiķi Latvijā", "Tālrunis": "25662202"},
            {"Nosaukums": "Narkoloģiskā palīdzība Rīgā", "Tālrunis": "67506017"},
            {"Nosaukums": "Krīzes centrs", "Tālrunis": "116123"},
            {"Nosaukums": "Jauniešu konsultāciju centrs", "Tālrunis": "67222922"}
        ]
        
        # Izveido Treeview palīdzības dienestiem
        help_tree = ttk.Treeview(
            help_window,
            columns=("Nosaukums", "Tālrunis"),
            show="headings",
            style='Treeview',
            height=5
        )
        help_tree.heading("Nosaukums", text="Dienesta nosaukums")
        help_tree.heading("Tālrunis", text="Kontakttālrunis")
        help_tree.column("Nosaukums", width=350)
        help_tree.column("Tālrunis", width=150, anchor="center")
        
        for service in help_services:
            help_tree.insert("", "end", values=(service["Nosaukums"], service["Tālrunis"]))
        
        help_tree.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Paziņojuma teksts
        ttk.Label(
            help_window,
            text="Ja jūs vai kāds no jūsu tuviniekiem cīnās ar atkarību,\n"
                 "lūdzu, nevilcinieties sazināties ar speciālistiem.",
            style='TLabel',
            justify="center"
        ).pack(pady=10)
    
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
            messagebox.showerror("Kļūda", f"Datu ielādes kļūda:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AVSApp(root)
    root.mainloop()