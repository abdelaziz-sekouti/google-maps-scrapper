import tkinter as tk
from tkinter import ttk, messagebox
import threading
import asyncio
import os
from main import GoogleMapsScraper, console

class ScraperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Google Maps Lead Scraper")
        self.root.geometry("700x550")
        self.root.configure(bg="#1e1e2e")  # Dark theme
        
        # Enable Ctrl+A (Select All) for all entry widgets
        self.root.bind_class("Entry", "<Control-a>", lambda e: e.widget.select_range(0, "end") or "break")
        self.root.bind_class("Entry", "<Control-A>", lambda e: e.widget.select_range(0, "end") or "break")
        
        # Style Configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure Colors
        bg_color = "#1e1e2e"
        fg_color = "#cdd6f4"
        accent_color = "#89b4fa"
        
        self.style.configure("TFrame", background=bg_color)
        self.style.configure("TLabel", background=bg_color, foreground=fg_color, font=("Segoe UI", 10))
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"))
        self.style.configure("TCheckbutton", background=bg_color, foreground=fg_color)
        
        # Header
        header_frame = tk.Frame(root, bg="#313244", height=60)
        header_frame.pack(fill="x")
        tk.Label(header_frame, text="⚡ Google Maps Scraper Pro", bg="#313244", fg="#f5e0dc", font=("Segoe UI", 16, "bold")).pack(pady=15)

        # Main Container
        main_frame = tk.Frame(root, bg=bg_color, padx=30, pady=20)
        main_frame.pack(fill="both", expand=True)

        # URL Input
        tk.Label(main_frame, text="Google Maps Search URL:", bg=bg_color, fg=accent_color, font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.url_entry = tk.Entry(main_frame, width=80, bg="#313244", fg=fg_color, insertbackground=fg_color, borderwidth=0, font=("Segoe UI", 10))
        self.url_entry.pack(fill="x", pady=(5, 15))
        self.url_entry.insert(0, "https://www.google.com/maps/search/riads+marrakech")

        # Config Row
        config_frame = tk.Frame(main_frame, bg=bg_color)
        config_frame.pack(fill="x")

        # Leads Count
        tk.Label(config_frame, text="Leads to Scrape:", bg=bg_color, fg=fg_color).grid(row=0, column=0, sticky="w")
        self.count_spin = tk.Spinbox(config_frame, from_=1, to=500, width=10, bg="#313244", fg=fg_color, buttonbackground="#45475a")
        self.count_spin.delete(0, "end")
        self.count_spin.insert(0, "100")
        self.count_spin.grid(row=0, column=1, padx=(10, 30), sticky="w")

        # Website Filter
        self.web_var = tk.BooleanVar()
        self.web_check = tk.Checkbutton(config_frame, text="Only with Website", variable=self.web_var, 
                                        bg=bg_color, fg=fg_color, selectcolor="#313244", activebackground=bg_color, activeforeground=fg_color)
        self.web_check.grid(row=0, column=2, padx=(10, 20), sticky="w")

        # Country Code
        tk.Label(config_frame, text="Indicatif (+):", bg=bg_color, fg=fg_color).grid(row=0, column=3, sticky="w")
        self.indic_entry = tk.Entry(config_frame, width=5, bg="#313244", fg=fg_color, borderwidth=0)
        self.indic_entry.insert(0, "212")
        self.indic_entry.grid(row=0, column=4, padx=5, sticky="w")

        # Exclude Prefixes
        tk.Label(main_frame, text="Exclude Prefixes (e.g. +2125, 05):", bg=bg_color, fg=fg_color).pack(anchor="w", pady=(10, 0))
        self.prefix_entry = tk.Entry(main_frame, width=80, bg="#313244", fg=fg_color, insertbackground=fg_color, borderwidth=0, font=("Segoe UI", 10))
        self.prefix_entry.pack(fill="x", pady=(5, 15))
        self.prefix_entry.insert(0, "+2125, 05")

        # City & Message Template Row
        msg_frame = tk.Frame(main_frame, bg=bg_color)
        msg_frame.pack(fill="x", pady=(10, 0))

        tk.Label(msg_frame, text="City:", bg=bg_color, fg=fg_color).grid(row=0, column=0, sticky="w")
        self.city_entry = tk.Entry(msg_frame, width=15, bg="#313244", fg=fg_color, borderwidth=0)
        self.city_entry.insert(0, "Marrakech")
        self.city_entry.grid(row=0, column=1, padx=(5, 20), sticky="w")

        tk.Label(msg_frame, text="Msg Template:", bg=bg_color, fg=fg_color).grid(row=0, column=2, sticky="w")
        self.msg_entry = tk.Entry(msg_frame, width=40, bg="#313244", fg=fg_color, borderwidth=0)
        self.msg_entry.insert(0, "Bonjour [Name], j'aime votre établissement à [City] !")
        self.msg_entry.grid(row=0, column=3, padx=5, sticky="w")

        # Progress Section
        self.progress_label = tk.Label(main_frame, text="Ready", bg=bg_color, fg="#a6adc8")
        self.progress_label.pack(pady=(15, 0))
        
        self.progress_bar = ttk.Progressbar(main_frame, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(fill="x", pady=5)

        # Log Area
        self.log_text = tk.Text(main_frame, height=8, bg="#11111b", fg="#a6e3a1", borderwidth=0, font=("Consolas", 9))
        self.log_text.pack(fill="both", expand=True, pady=10)

        # Buttons
        btn_frame = tk.Frame(main_frame, bg=bg_color)
        btn_frame.pack(fill="x", pady=10)

        # Modern Button Simulation
        self.start_btn = tk.Button(btn_frame, text="🚀 START SCRAPING", bg="#a6e3a1", fg="#11111b", 
                                   font=("Segoe UI", 10, "bold"), padx=20, borderwidth=0, cursor="hand2", 
                                   command=self.start_scraping)
        self.start_btn.pack(side="left", padx=5)

        self.open_dir_btn = tk.Button(btn_frame, text="📂 Open Folder", bg="#45475a", fg=fg_color, 
                                      font=("Segoe UI", 10), padx=15, borderwidth=0, cursor="hand2", 
                                      command=self.open_folder)
        self.open_dir_btn.pack(side="right", padx=5)

        self.scraper_thread = None

    def log(self, message):
        self.log_text.insert("end", f"> {message}\n")
        self.log_text.see("end")

    def open_folder(self):
        os.startfile('.') if os.name == 'nt' else os.system('xdg-open .')

    def progress_callback(self, message, count=None):
        def update_ui():
            self.progress_label.config(text=message)
            self.log(message)
            if count is not None:
                max_count = int(self.count_spin.get())
                progress_val = (count / max_count) * 100
                self.progress_bar["value"] = progress_val
        
        self.root.after(0, update_ui)

    def start_scraping(self):
        url = self.url_entry.get()
        if not url.startswith("http"):
            messagebox.showerror("Error", "Please enter a valid Google Maps URL")
            return

        self.start_btn.config(state="disabled", text="⌛ Scraping...", bg="#585b70")
        self.progress_bar["value"] = 0
        self.log("Initializing scraper engine...")
        
        # Run in separate thread
        self.scraper_thread = threading.Thread(target=self.run_scraper, daemon=True)
        self.scraper_thread.start()

    def run_scraper(self):
        import traceback
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            target_count = int(self.count_spin.get())
            indicatif = self.indic_entry.get().strip() or "212"
            city = self.city_entry.get().strip()
            msg_template = self.msg_entry.get().strip()
            
            filters = {
                "include_website_only": self.web_var.get(),
                "exclude_prefixes": [p.strip() for p in self.prefix_entry.get().split(",") if p.strip()]
            }
            
            scraper = GoogleMapsScraper(target_leads=target_count, headless=True, 
                                        indicatif=indicatif, city=city, message_template=msg_template)
            leads = loop.run_until_complete(scraper.scrape(self.url_entry.get(), filters, self.progress_callback))


            
            # Export data
            scraper.export_data()
            
            self.root.after(0, lambda: self.on_finished(len(leads)))
            
        except Exception as e:
            error_msg = traceback.format_exc()
            with open("log.txt", "a") as f:
                f.write(f"\nFATAL ERROR:\n{error_msg}\n")
            self.root.after(0, lambda: messagebox.showerror("Scraper Error", f"{str(e)}\n\nCheck log.txt for details."))
            self.root.after(0, lambda: self.on_finished(0))
        finally:
            loop.close()


    def on_finished(self, count):
        self.start_btn.config(state="normal", text="🚀 START SCRAPING", bg="#a6e3a1")
        if count > 0:
            self.progress_label.config(text=f"✅ Finished! Collected {count} leads.")
            messagebox.showinfo("Success", f"Scraping completed!\n{count} leads saved to leads.csv and leads.xlsx")
        else:
            self.progress_label.config(text="Ready")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScraperGUI(root)
    root.mainloop()
