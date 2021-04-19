import tkinter as tk # Tkinter

#%%
_root = tk.Tk()
_root.title('after sample')
_root.geometry("320x240+50+50") # 지오메트리: 너비x높이+x좌표+y좌표

lbl = tk.Label(_root,text='',font=("Arial Bold",50))
lbl.grid(column=0, row=0)

_count = 0;
def _loop():
    global _count ,lbl
    lbl.config(text=f'{_count}')
    _count+=1
    print(_count)
    lbl.after(1000, _loop)

_loop()

_root.mainloop()
