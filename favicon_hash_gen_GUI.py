import tkinter as tk
import mmh3, base64, time, sys
from pathlib import Path

class FaviconOsintTool:
    def __init__(self, root):
        self.root = root
        self.root.title("OSINT_FAVICON_GENERATOR_v1.0")
        self.root.geometry("1150x700")
        self.root.configure(bg="#0a0a0a")
        
        self.running = True  

        self.output = tk.Text(
            root, bg="#0a0a0a", fg="#ffffff", 
            font=("Consolas", 12), padx=45, pady=45, 
            bd=0, highlightthickness=0, selectbackground="#333333"
        )
        self.output.pack(expand=True, fill="both")

        self.output.tag_config("bracket", foreground="#ffffff")    
        self.output.tag_config("divider", foreground="#ffffff")    
        self.output.tag_config("time", foreground="#888888")       
        self.output.tag_config("inner", foreground="#a020f0")      
        self.output.tag_config("info", foreground="#00ff41")       
        self.output.tag_config("val", foreground="#ffd700")        
        self.output.tag_config("error", foreground="#ff3131")      

        self.menu = tk.Menu(self.root, tearoff=0, bg="#1a1a1a", fg="#ffd700", activebackground="#333333")
        self.menu.add_command(label="[ COPY SELECTED ]", command=self.copy_selection)

        self.root.bind("<Control-c>", self.exit_gracefully) 
        self.output.bind("<Button-3>", self.show_menu)             
        self.root.bind("<Button-1>", lambda e: self.menu.unpost()) 

        self.start_process()

    def exit_gracefully(self, event=None):
        self.running = False
        try:
            self.root.destroy()
        except:
            pass

    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def copy_selection(self):
        try:
            selected = self.output.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.root.clipboard_clear()
            self.root.clipboard_append(selected)
        except tk.TclError:
            pass 

    def log(self, status_text, message, msg_tag="info"):
        if not self.running: return
        ts = time.strftime("%H:%M:%S")
        self.output.insert(tk.END, "[ ", "bracket")
        self.output.insert(tk.END, ts, "time")
        self.output.insert(tk.END, " ] [ ", "bracket")
        self.output.insert(tk.END, status_text, "inner")
        self.output.insert(tk.END, " ] ", "bracket")
        self.output.insert(tk.END, message, msg_tag)
        self.output.insert(tk.END, "\n")
        self.root.update()

    def sleep_check(self, duration):
        start = time.time()
        while time.time() - start < duration:
            if not self.running: break
            try:
                self.root.update()
            except:
                break
            time.sleep(0.001)

    def start_process(self):
        self.output.insert(tk.END, ">>> Initializing OSINT Scanner Core...\n", "bracket")
        self.sleep_check(0.3)
        
        path = Path('favicon.ico')
        if not path.exists():
            self.log("FAIL", f"Source file '{path.name}' not found.", "error")
            return

        self.log("INIT", f"Target identified: {path.name}", "info")
        
        self.output.insert(tk.END, "[ ", "bracket")
        self.output.insert(tk.END, "ANALYZING", "inner")
        self.output.insert(tk.END, " ] ", "bracket")
        
        for _ in range(35):
            if not self.running: return
            self.sleep_check(0.01)
            self.output.insert(tk.END, "■", "val")
            try:
                self.root.update()
            except:
                break
        self.output.insert(tk.END, " 100% OK\n\n", "info")

        try:
            raw = path.read_bytes()
            b64 = base64.encodebytes(raw)
            f_hash = mmh3.hash(b64)
            h_str = str(f_hash)

            self.output.insert(tk.END, ">>> MMH3_ID", "info")
            self.output.insert(tk.END, ": ", "divider")
            self.output.insert(tk.END, f"{h_str}\n\n", "val")

            dorks = [
                ("SHODAN", "http.favicon.hash", ":"),
                ("CENSYS", "web.endpoints.http.favicons.hash_shodan", "="),
                ("FOFA", "icon_hash", "=")
            ]

            for engine, query, sep in dorks:
                if not self.running: return
                val = f'"{h_str}"' if engine == "FOFA" else h_str
                self.output.insert(tk.END, "[ ", "bracket")
                self.output.insert(tk.END, engine, "inner")
                self.output.insert(tk.END, " ] ", "bracket")
                self.output.insert(tk.END, query, "val")
                self.output.insert(tk.END, sep, "divider") 
                self.output.insert(tk.END, f"{val}\n", "val")

        except Exception as e:
            self.log("ERROR", str(e), "error")

        if self.running:
            self.output.insert(tk.END, "\n" + "-"*65 + "\n", "bracket")
            self.output.insert(tk.END, ">>> Session complete. CTRL+C to Exit.\n", "bracket")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        root.attributes('-alpha', 0.98)
        app = FaviconOsintTool(root)
        root.mainloop()
    except (KeyboardInterrupt, tk.TclError, SystemExit):
        pass
    finally:
        print("\n[!] Программа завершила свою работу.")
        os_exit_code = 0
        sys.exit(os_exit_code)
