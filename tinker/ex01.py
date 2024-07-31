#%%
import tkinter as tk # Tkinter
import pathlib

#%%
win = tk.Tk()
win.title("opencv tinker basic") # 상단제목 설정
win.geometry("320x240+50+50") # 지오메트리: 너비x높이+x좌표+y좌표
# win.resizable(False, False) # x축, y축 크기 조정 비활성화

lbl = tk.Label(win, text="Hello" ,font=("Arial Bold",50))
lbl.grid(column=0, row=0)

lbl_2 = tk.Label(win, text=f'tk version: {tk.TkVersion}')
lbl_2.grid(column=0, row=1)

print(f'{pathlib.Path.cwd()}')
# lbl_2 = tk.Label(win, text=f'{pathlib.Path.cwd()}')
# lbl_2.grid(column=0, row=1)

win.mainloop()

# %%
