
import tkinter as tk
from tkinter import messagebox


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RTSP Media Server")
        self.geometry("800x600")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def on_close(self):
        if messagebox.askyesno("종료", "프로그램을 종료하시겠습니까?"):
            self.destroy()
            exit()

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()