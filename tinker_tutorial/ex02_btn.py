import tkinter as tk
from tkinter import messagebox

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ex02 Button Sample")
        self.geometry("320x240")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self._build_widgets()

    def _build_widgets(self):
        frame1 = tk.Frame(self,bg="#e0e0e0")
        frame1.pack(fill='x', padx=10, pady=10)
        tk.Button(frame1, text="Button 1", command=self.on_button1).pack(side='left', padx=4)
        tk.Button(frame1, text="Button 2", command=self.on_button2).pack(side='left', padx=8)
        tk.Button(frame1, text="Button 3", command=self.on_button3).pack(side='left', padx=16)

        frame2 = tk.Frame(self,bg="#c0c0c0")
        frame2.pack(fill='both', expand=True, padx=10, pady=10)

    def on_button1(self):
        messagebox.showinfo("Button 1", "Button 1 clicked")

    def on_button2(self):
        messagebox.showinfo("Button 2", "Button 2 clicked")

    def on_button3(self):
        messagebox.showinfo("Button 3", "Button 3 clicked")

    def on_close(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()