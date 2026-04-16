import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import threading
import asyncio
import os
import datetime
from main import GoogleMapsScraper

# Set appearance and theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Global City Mapping
CITY_MAP = {
    "marrakech": "212", "casablanca": "212", "rabat": "212", "agadir": "212", "tangier": "212", "fes": "212",
    "paris": "33", "lyon": "33", "marseille": "33", "bordeaux": "33", "nice": "33", "nantes": "33",
    "brussels": "32", "bruxelles": "32", "liege": "32", "antwerp": "32",
    "geneva": "41", "geneve": "41", "zurich": "41",
    "madrid": "34", "barcelona": "34",
    "london": "44", "manchester": "44",
    "dubai": "971", "abu dhabi": "971"
}

class ScraperGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        # ... (rest of init)


        # --- Window Configuration ---
        self.title("LeadScraper Pro Enterprise v3.0")
        self.geometry("1100x850")
        self.configure(fg_color="#11111b")

        # Global Bindings
        self.bind_class("Entry", "<Control-a>", lambda e: e.widget.select_range(0, "end") or "break")

        # --- HEADER ---
        header = ctk.CTkFrame(self, fg_color="#181825", corner_radius=0, height=80)
        header.pack(fill="x")
        ctk.CTkLabel(header, text="💎 LEAD HARVESTER PRO", 
                     font=ctk.CTkFont(size=28, weight="bold"), text_color="#f5c2e7").pack(pady=20)

        # Main Workspace (Non-scrollable as requested)
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=25, pady=20)

        # --- TOP SECTION: Search & Configuration ---
        top_section = ctk.CTkFrame(self.main_container, fg_color="#1e1e2e", corner_radius=15, border_width=1, border_color="#313244")
        top_section.pack(fill="x", pady=(0, 15))
        
        # URL Row
        u_row = ctk.CTkFrame(top_section, fg_color="transparent")
        u_row.pack(fill="x", padx=20, pady=(20, 10))
        ctk.CTkLabel(u_row, text="Target URL", font=ctk.CTkFont(weight="bold")).pack(side="left")
        self.url_entry = ctk.CTkEntry(u_row, height=45, placeholder_text="Enter Maps URL...", fg_color="#313244")
        self.url_entry.pack(side="left", fill="x", expand=True, padx=(20, 0))
        self.url_entry.insert(0, "https://www.google.com/maps/search/riads+marrakech")

        # Params Row
        p_row = ctk.CTkFrame(top_section, fg_color="transparent")
        p_row.pack(fill="x", padx=20, pady=(0, 20))
        
        # Count
        ctk.CTkLabel(p_row, text="Leads Goal:").pack(side="left")
        self.count_spin = ctk.CTkEntry(p_row, width=70, fg_color="#313244")
        self.count_spin.insert(0, "100")
        self.count_spin.pack(side="left", padx=10)

        # Indicatif
        ctk.CTkLabel(p_row, text="Indicatif (+):").pack(side="left", padx=(20, 0))
        self.indic_entry = ctk.CTkEntry(p_row, width=60, fg_color="#313244")
        self.indic_entry.insert(0, "212")
        self.indic_entry.pack(side="left", padx=10)

        # City
        ctk.CTkLabel(p_row, text="City:").pack(side="left", padx=(20, 0))
        self.city_entry = ctk.CTkEntry(p_row, width=100, fg_color="#313244")
        self.city_entry.insert(0, "Marrakech")
        self.city_entry.pack(side="left", padx=10)
        self.city_entry.bind("<KeyRelease>", self.detect_country)


        # Filters
        self.web_var = ctk.BooleanVar(value=False)
        self.web_check = ctk.CTkCheckBox(p_row, text="Only with Website", variable=self.web_var, fg_color="#a6e3a1")
        self.web_check.pack(side="right", padx=10)

        # Filters Row (New)
        f_row = ctk.CTkFrame(top_section, fg_color="transparent")
        f_row.pack(fill="x", padx=20, pady=(0, 20))

        # Include Prefixes (Whitelist)
        ctk.CTkLabel(f_row, text="Target Prefixes:", text_color="#f9e2af").pack(side="left")
        self.include_entry = ctk.CTkEntry(f_row, width=150, placeholder_text="e.g. 0524, 0525", fg_color="#313244", border_color="#f9e2af", border_width=1)
        self.include_entry.pack(side="left", padx=10)

        # Exclude Prefixes (Blacklist)
        ctk.CTkLabel(f_row, text="Exclude Prefixes:", text_color="#f38ba8").pack(side="left", padx=(20, 0))
        self.exclude_entry = ctk.CTkEntry(f_row, width=150, placeholder_text="e.g. 05, +2125", fg_color="#313244", border_color="#f38ba8", border_width=1)
        self.exclude_entry.insert(0, "05, +2125")
        self.exclude_entry.pack(side="left", padx=10)


        # --- MIDDLE SECTION: Message & Console Side-by-Side ---
        mid_section = ctk.CTkFrame(self.main_container, fg_color="transparent")
        mid_section.pack(fill="both", expand=True)
        mid_section.grid_columnconfigure(0, weight=3) # Message Editor
        mid_section.grid_columnconfigure(1, weight=2) # Live Console
        mid_section.grid_rowconfigure(0, weight=1)

        # 1. Message Editor Panel
        msg_panel = ctk.CTkFrame(mid_section, fg_color="#1e1e2e", corner_radius=15, border_width=1, border_color="#313244")
        msg_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(msg_panel, text="✍️ WhatsApp Pitch Editor", font=ctk.CTkFont(size=14, weight="bold"), text_color="#f5c2e7").pack(pady=10)
        self.msg_entry = ctk.CTkTextbox(msg_panel, fg_color="#11111b", font=("Inter", 13), border_width=1, border_color="#45475a")
        self.msg_entry.insert("1.0", "Bonjour 👋 [Name]\nJe suis tombé sur votre cabinet dentaire en ligne.\n\nPetite question — est-ce que vous recevez suffisamment de patients via Google ou WhatsApp actuellement ?\nJ’ai remarqué que votre présence en ligne (site web) n’est pas optimisée, et cela peut vous faire perdre des clients chaque jour.\n\nJ’aide des dentistes comme vous à obtenir plus de patients grâce à un système simple (site web + WhatsApp + visibilité Google).\n\nJe peux vous montrer exactement ce qui vous manque — gratuitement.\n\nÇa vous intéresse ?")
        self.msg_entry.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # 2. Live Console Panel
        console_panel = ctk.CTkFrame(mid_section, fg_color="#181825", corner_radius=15, border_width=1, border_color="#313244")
        console_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(console_panel, text="🖥️ Extraction Stream", font=ctk.CTkFont(size=14, weight="bold"), text_color="#a6e3a1").pack(pady=10)
        self.log_text = ctk.CTkTextbox(console_panel, fg_color="#0b0b11", text_color="#94e2d5", font=("Consolas", 12))
        self.log_text.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # --- BOTTOM SECTION: Stats & Progress ---
        bottom_section = ctk.CTkFrame(self, fg_color="#181825", corner_radius=0, height=100)
        bottom_section.pack(fill="x", side="bottom")

        # Stats Counter
        self.counter_label = ctk.CTkLabel(bottom_section, text="TOTAL LEADS HARVESTED: 0", 
                                          font=ctk.CTkFont(size=18, weight="bold"), text_color="#f9e2af")
        self.counter_label.pack(side="top", pady=(15, 5))

        # Buttons Center
        btn_frame = ctk.CTkFrame(bottom_section, fg_color="transparent")
        btn_frame.pack(side="top", pady=(0, 15))

        self.start_btn = ctk.CTkButton(btn_frame, text="🚀 LAUNCH SCRAPER", height=50, width=280, 
                                       font=ctk.CTkFont(size=16, weight="bold"),
                                       fg_color="#a6e3a1", text_color="#11111b", hover_color="#94e2d5",
                                       command=self.start_scraping)
        self.start_btn.pack(side="left", padx=20)

        self.open_btn = ctk.CTkButton(btn_frame, text="📂 OPEN RESULTS", height=50, width=200,
                                      fg_color="#313244", hover_color="#45475a",
                                      command=self.open_folder)
        self.open_btn.pack(side="left", padx=20)

        # Status
        self.status_label = ctk.CTkLabel(bottom_section, text="System Standby", text_color="#a6adc8")
        self.status_label.pack(side="bottom", pady=5)

    def log(self, message):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{now}] {message}\n")
        self.log_text.see("end")

    def open_folder(self):
        os.startfile('.') if os.name == 'nt' else os.system('xdg-open .')

    def progress_callback(self, message, count=None):
        def update_ui():
            self.status_label.configure(text=message)
            self.log(message)
            if count is not None:
                self.counter_label.configure(text=f"TOTAL LEADS HARVESTED: {count}", text_color="#f9e2af")
        self.after(0, update_ui)

    def start_scraping(self):
        url = self.url_entry.get()
        if not url.startswith("http"):
            messagebox.showerror("Operation Blocked", "Please verify the Google Maps Search URL.")
            return
        
        self.start_btn.configure(state="disabled", text="⚡ HARVESTING ACTIVE...", fg_color="#45475a")
        self.counter_label.configure(text="TOTAL LEADS HARVESTED: 0")
        self.log("Ignition sequence started...")
        
        threading.Thread(target=self.run_scraper, daemon=True).start()

    def run_scraper(self):
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            target_count = int(self.count_spin.get())
            indicatif = self.indic_entry.get().strip() or "212"
            city = self.city_entry.get().strip()
            msg_template = self.msg_entry.get("1.0", "end-1c").strip()
            
            filters = {
                "include_website_only": self.web_var.get(),
                "include_prefixes": [p.strip() for p in self.include_entry.get().split(",") if p.strip()],
                "exclude_prefixes": [p.strip() for p in self.exclude_entry.get().split(",") if p.strip()]
            }
            
            scraper = GoogleMapsScraper(target_leads=target_count, headless=True, 
                                        indicatif=indicatif, city=city, message_template=msg_template)
            leads = loop.run_until_complete(scraper.scrape(self.url_entry.get(), filters, self.progress_callback))
            scraper.export_data()
            self.after(0, lambda: self.on_finished(len(leads)))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("System Breach", str(e)))
            self.after(0, lambda: self.on_finished(0))
        finally:
            loop.close()

    def detect_country(self, event=None):
        """Automatically updates the indicatif based on the city typed"""
        val = self.city_entry.get().lower().strip()
        for city, code in CITY_MAP.items():
            if city in val:
                self.indic_entry.delete(0, "end")
                self.indic_entry.insert(0, code)
                break

    def on_finished(self, count):
        self.start_btn.configure(state="normal", text="🚀 LAUNCH SCRAPER", fg_color="#a6e3a1")
        self.status_label.configure(text="Extraction Complete")
        if count > 0:
            messagebox.showinfo("Success", f"Extraction successfully completed!\n\nTotal Leads Collected: {count}\n\nAll results formatted in 'leads.xlsx' with one-click WhatsApp links.")

if __name__ == "__main__":
    app = ScraperGUI()
    app.mainloop()
