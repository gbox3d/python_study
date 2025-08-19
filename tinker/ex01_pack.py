
import tkinter as tk
from tkinter import messagebox


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RTSP Media Server")
        self.geometry("800x600")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self._build_widgets()

    def _build_widgets(self):
        top = tk.Frame(self,bg="#e00")
        top.pack(fill='x', padx=10, pady=10)
        tk.Label(top, text="left", font=("Arial", 16)).pack(side='left')
        tk.Label(top, text="center", font=("Arial", 16)).pack(side='left', expand=True)
        tk.Label(top, text="right", font=("Arial", 16)).pack(side='right')

        body = tk.Frame(self,bg="#008")
        body.pack(fill='both', expand=True, padx=10, pady=10)
        tk.Label(body, text="left",bg="#ffd").pack(side=tk.LEFT)
        # tk.Label(body, text="center", bg="#dfd").pack(side=tk.TOP, expand=True)
        tk.Label(body, text="right", bg="#ddf").pack(side=tk.RIGHT)
        tk.Label(body, text="bottom", bg="#ddd").pack(side=tk.BOTTOM)
        tk.Label(body, text="top", bg="#ddd").pack(side=tk.TOP)

        tail = tk.Frame(self,bg="#0e0")
        
        tail.pack(fill='x', padx=10, pady=(0, 10))
        tk.Label(tail, text="left", bg="#f88").pack(side=tk.LEFT)
        tk.Label(tail, text="center", bg="#8f8").pack(side=tk.LEFT, expand=True)
        tk.Label(tail, text="right", bg="#88f").pack(side=tk.RIGHT)

    def on_close(self):
        try:
            if messagebox.askyesno("종료", "프로그램을 종료하시겠습니까?"):
                self.destroy()
        except Exception as e:
            print(f"Error occurred: {e}")
            exit()

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()
