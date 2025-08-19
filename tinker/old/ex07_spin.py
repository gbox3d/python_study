import tkinter as tk # Tkinter
import tkinter.ttk as ttk
import pathlib

#%%
win = tk.Tk()
win.title("opencv tinker basic") # 상단제목 설정
win.geometry("320x240+50+50") # 지오메트리: 너비x높이+x좌표+y좌표
# win.resizable(False, False) # x축, y축 크기 조정 비활성화

lbl = tk.Label(win, text="Hello") #라벨만들기 
lbl.grid(column=0, row=0)

var = tk.IntVar()
var.set(5)
spin = ttk.Spinbox(win,from_=0,to=10,width=10,textvariable=var)
spin.grid(column=0,row=1)


def clicked():
    lbl.config(text=f'{var.get()}')

btn = tk.Button(win,text='click me',command=clicked)
btn.grid(column=1,row=0)

win.mainloop()

# %%
