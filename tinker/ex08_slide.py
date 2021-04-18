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

var = tk.DoubleVar()
var.set(5)

def scalechg(_val):
    print(f'{_val}')
scale = ttk.Scale(win,variable=var,from_=0,to=10,command=scalechg)
scale.grid(column=0,row=1)


def clicked():
    lbl.config(text=f'{var.get()}')

btn = tk.Button(win,text='click me',command=clicked)
btn.grid(column=1,row=0)

win.mainloop()

# %%
