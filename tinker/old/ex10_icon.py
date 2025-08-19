import tkinter as tk # Tkinter

root = tk.Tk()
root.tk.call('wm','iconphoto',root._w,tk.PhotoImage(file='Lenna.png'))


# root.iconphoto(False, tk.PhotoImage(file='Lenna.png'))

root.mainloop()