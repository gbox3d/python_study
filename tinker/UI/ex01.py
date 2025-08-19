import tkinter as tk
import pygubu

from tkinter import ttk

class Application():
    def __init__(self):
        super().__init__()
        self.builder = pygubu.Builder()
        self.builder.add_from_file('ex01.ui')
        self.mainwindow = self.builder.get_object('root')
        self.builder.connect_callbacks(self)

    # .ui의 command 이름과 동일해야 함
    def callback_hello(self,event=None): 
        print("hello")
        self.builder.get_object('InfoLabel').config(text='Hello, World!')
    def callback_hi(self,event=None): 
        print("hi")
        self.builder.get_object('InfoLabel').config(text='Hi, there!')
    
    def run(self):
        self.mainwindow.mainloop()

    
if __name__ == '__main__':
    app = Application()
    app.run()