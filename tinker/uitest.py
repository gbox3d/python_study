import tkinter as tk
import pygubu

class MyApplication:
    def __init__(self):
        self.builder = pygubu.Builder()
        self.builder.add_from_file('ex01.ui')
        self.mainwindow = self.builder.get_object('tk1')
        self.builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    app = MyApplication()
    app.run()