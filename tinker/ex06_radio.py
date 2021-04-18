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

selected = tk.IntVar()

rad1 = ttk.Radiobutton(win, text="First",value=1,variable=selected)
rad2 = ttk.Radiobutton(win, text="Second",value=2,variable=selected)
rad3 = ttk.Radiobutton(win, text="Third",value=3,variable=selected)

rad1.grid(column=0,row=1)
rad2.grid(column=1,row=1)
rad3.grid(column=2,row=1)

def clicked():
    print(f'{selected.get()}')
    # lbl.config(text=f'{combo.get()}')

btn = tk.Button(win,text='click me',command=clicked)
btn.grid(column=1,row=0)

win.mainloop()