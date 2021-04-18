import tkinter as tk # Tkinter

#%%
win = tk.Tk()
win.title("opencv tinker basic") # 상단제목 설정
win.geometry("320x240+50+50") # 지오메트리: 너비x높이+x좌표+y좌표
# win.resizable(False, False) # x축, y축 크기 조정 비활성화

lbl = tk.Label(win, text="Hello") #라벨만들기 
lbl.grid(column=0, row=0)

def clicked2():
    lbl.config(text="hello clicked!")
    btn.config(command=clicked)

def clicked():
    lbl.config(text="world clicked!")
    btn.config(command=clicked2)

btn = tk.Button(win,text='click me',command=clicked)
btn.grid(column=1,row=0)

win.mainloop()

# %%
