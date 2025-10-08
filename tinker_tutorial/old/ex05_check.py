import tkinter as tk # Tkinter
import tkinter.ttk as ttk
import pathlib

#%%
win = tk.Tk()
win.title("opencv tinker basic") # 상단제목 설정
win.geometry("320x240+50+50") # 지오메트리: 너비x높이+x좌표+y좌표
# win.resizable(False, False) # x축, y축 크기 조정 비활성화

lbl = tk.Label(win, text="Hello" ,font=("Arial Bold",50))
lbl.grid(column=0, row=0)

print(f'{pathlib.Path.cwd()}')

chk_status = tk.BooleanVar()
chk_status.set(True)

chk = ttk.Checkbutton(win,text="choose",var=chk_status)
chk.grid(column=0,row=1)

def clicked():
    print(f'{chk_status.get()}')
    # lbl.config(text=f'{combo.get()}')

btn = tk.Button(win,text='click me',command=clicked)
btn.grid(column=1,row=0)

win.mainloop()