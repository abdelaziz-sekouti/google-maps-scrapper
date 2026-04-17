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

# Global Mapping (Comprehensive Country Codes)
COUNTRY_MAP = {
    "afghanistan": "93", "albania": "355", "algeria": "213", "algerie": "213", "andorra": "376", "angola": "244", "argentina": "54", "armenia": "374", "australia": "61", "austria": "43", "azerbaijan": "994",
    "bahrain": "973", "bangladesh": "880", "belarus": "375", "belgium": "32", "belgique": "32", "belize": "501", "benin": "229", "bhutan": "975", "bolivia": "591", "bosnia": "387", "brazil": "55", "bulgaria": "359",
    "cambodia": "855", "cameroon": "237", "canada": "1", "central african republic": "236", "chad": "235", "chile": "56", "china": "86", "colombia": "57", "congo": "242", "costa rica": "506", "croatia": "385", "cuba": "53", "cyprus": "357", "czech republic": "420",
    "denmark": "45", "djibouti": "253", "dominica": "1", "dominican republic": "1", "ecuador": "593", "egypt": "20", "egypte": "20", "el salvador": "503", "estonia": "372", "ethiopia": "251",
    "fiji": "679", "finland": "358", "france": "33", "gabon": "241", "gambia": "220", "georgia": "995", "germany": "49", "ghana": "233", "greece": "30", "guatemala": "502", "guinea": "224", "guyana": "592",
    "haiti": "509", "honduras": "504", "hong kong": "852", "hungary": "36", "iceland": "354", "india": "91", "indonesia": "62", "iran": "98", "iraq": "964", "ireland": "353", "israel": "972", "italy": "39", "ivory coast": "225",
    "jamaica": "1", "japan": "81", "jordan": "962", "kazakhstan": "7", "kenya": "254", "kuwait": "965", "kyrgyzstan": "996", "laos": "856", "latvia": "371", "lebanon": "961", "liberia": "231", "libya": "218", "lithuania": "370", "luxembourg": "352",
    "macau": "853", "macedonia": "389", "madagascar": "261", "malawi": "265", "malaysia": "60", "maldives": "960", "mali": "223", "malta": "356", "mauritania": "222", "mauritius": "230", "mexico": "52", "moldova": "373", "monaco": "377", "mongolia": "976", "montenegro": "382", "morocco": "212", "maroc": "212", "mozambique": "258", "myanmar": "95",
    "namibia": "264", "nepal": "977", "netherlands": "31", "new zealand": "64", "nicaragua": "505", "niger": "227", "nigeria": "234", "north korea": "850", "norway": "47", "oman": "968", "pakistan": "92", "palestine": "970", "panama": "507", "paraguay": "595", "peru": "51", "philippines": "63", "poland": "48", "portugal": "351",
    "qatar": "974", "romania": "40", "russia": "7", "rwanda": "250", "saudi arabia": "966", "saudi": "966", "senegal": "221", "serbia": "381", "seychelles": "248", "sierra leone": "232", "singapore": "65", "slovakia": "421", "slovenia": "386", "somalia": "252", "south africa": "27", "south korea": "82", "spain": "34", "espagne": "34", "sri lanka": "94", "sudan": "249", "suriname": "597", "swaziland": "268", "sweden": "46", "switzerland": "41", "suisse": "41", "syria": "963",
    "taiwan": "886", "tajikistan": "992", "tanzania": "255", "thailand": "66", "togo": "228", "tonga": "676", "trinidad and tobago": "1", "tunisia": "216", "turkey": "90", "turkmenistan": "993",
    "uganda": "256", "ukraine": "380", "united arab emirates": "971", "uae": "971", "united kingdom": "44", "uk": "44", "usa": "1", "uruguay": "598", "uzbekistan": "998",
    "venezuela": "58", "vietnam": "84", "yemen": "967", "zambia": "260", "zimbabwe": "263",
    # Major Cities
    "marrakech": "212", "casablanca": "212", "rabat": "212", "agadir": "212", "tangier": "212", "fes": "212",
    "paris": "33", "lyon": "33", "marseille": "33", "bordeaux": "33", "nice": "33", "nantes": "33",
    "brussels": "32", "bruxelles": "32", "dubai": "971", "london": "44", "madrid": "34", "barcelona": "34", "geneva": "41", "zurich": "41"
}

class ScraperGUI(ctk.CTk):
    def __init__(self):
        super().__init__()


        # Global Bindings
        self.bind_class("Entry", "<Control-a>", lambda e: e.widget.select_range(0, "end") or "break")
        self.bind_class("Text", "<Control-a>", lambda e: e.widget.tag_add("sel", "1.0", "end") or "break")
        self.configure(fg_color="#11111b")

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
        self.count_spin = ctk.CTkEntry(p_row, width=80, height=40, fg_color="#313244", font=ctk.CTkFont(size=14))
        self.count_spin.insert(0, "100")
        self.count_spin.pack(side="left", padx=10)

        # Indicatif
        ctk.CTkLabel(p_row, text="Indicatif (+):").pack(side="left", padx=(20, 0))
        self.indic_entry = ctk.CTkEntry(p_row, width=70, height=40, fg_color="#313244", font=ctk.CTkFont(size=14))
        self.indic_entry.insert(0, "212")
        self.indic_entry.pack(side="left", padx=10)

        # Country
        ctk.CTkLabel(p_row, text="Country/City:").pack(side="left", padx=(20, 0))
        self.country_entry = ctk.CTkEntry(p_row, width=120, height=40, fg_color="#313244", font=ctk.CTkFont(size=14))
        self.country_entry.insert(0, "Morocco")
        self.country_entry.pack(side="left", padx=10)
        self.country_entry.bind("<KeyRelease>", self.detect_country)


        # Filters
        self.web_var = ctk.BooleanVar(value=False)
        self.web_check = ctk.CTkCheckBox(p_row, text="Only with Website", variable=self.web_var, 
                                         fg_color="#313244", text_color="white", hover_color="#EEEEEE",
                                         checkbox_width=30, checkbox_height=30, checkmark_color="white",
                                         font=ctk.CTkFont(size=13, weight="bold"))
        self.web_check.pack(side="right", padx=10)

        # Filters Row (New)
        f_row = ctk.CTkFrame(top_section, fg_color="#313244")
        f_row.pack(fill="x", padx=30, pady=(0, 30))

        # Include Prefixes (Whitelist)
        ctk.CTkLabel(f_row, text="Target Prefixes:", text_color="#f9e2af").pack(side="left")
        self.include_entry = ctk.CTkEntry(f_row, width=150, height=40, placeholder_text="e.g. 0524, 0525", 
                                          fg_color="#313244", border_color="#f9e2af", border_width=1,
                                          font=ctk.CTkFont(size=14))
        self.include_entry.pack(side="left", padx=10)

        # Exclude Prefixes (Blacklist)
        ctk.CTkLabel(f_row, text="Exclude Prefixes:", text_color="#f38ba8").pack(side="left", padx=(20, 0))
        self.exclude_entry = ctk.CTkEntry(f_row, width=150, height=40, placeholder_text="e.g. 05, +2125", 
                                          fg_color="#313244", border_color="#f38ba8", border_width=1,
                                          font=ctk.CTkFont(size=14))
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

        # Apply Window Geometry at the end and with a slight delay to ensure it takes effect
        self.title("LeadHarvester Pro Enterprise v3.0")
        self.update_idletasks()
        self.geometry("700x600")
        self.after(100, lambda: self.geometry("700x600"))

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
            country = self.country_entry.get().strip()
            msg_template = self.msg_entry.get("1.0", "end-1c").strip()
            
            filters = {
                "include_website_only": self.web_var.get(),
                "include_prefixes": [p.strip() for p in self.include_entry.get().split(",") if p.strip()],
                "exclude_prefixes": [p.strip() for p in self.exclude_entry.get().split(",") if p.strip()]
            }
            
            scraper = GoogleMapsScraper(target_leads=target_count, headless=True, 
                                        indicatif=indicatif, city=country, message_template=msg_template)
            leads = loop.run_until_complete(scraper.scrape(self.url_entry.get(), filters, self.progress_callback))
            scraper.export_data()
            self.after(0, lambda: self.on_finished(len(leads)))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("System Breach", str(e)))
            self.after(0, lambda: self.on_finished(0))
        finally:
            loop.close()

    def detect_country(self, event=None):
        """Automatically updates the indicatif based on the country typed"""
        val = self.country_entry.get().lower().strip()
        for key, code in COUNTRY_MAP.items():
            if key in val:
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
