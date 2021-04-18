import tkinter as tk  # Tkinter
from PIL import ImageTk, Image  # Pillow
import cv2 as cv  # OpenCV
import os
import pathlib
# %%

print(f'{pathlib.Path.cwd()}')

# GUI 설계
win = tk.Tk()  # 인스턴스 생성

win.title("opencv tinker basic")  # 제목 표시줄 추가
win.geometry("920x640+50+50")  # 지오메트리: 너비x높이+x좌표+y좌표
win.resizable(False, False)  # x축, y축 크기 조정 비활성화

# 라벨1 추가
_canvas = tk.Canvas(win, bg="white", width=512, height=512)
_canvas.grid(column=0, row=0)

img = cv.imread('../../res/Lenna.png')
_img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
__img = Image.fromarray(_img)  # Image 객체로 변환
imgtk = ImageTk.PhotoImage(image=__img)  # ImageTk 객체로 변환

_canvas.create_image(0, 0, image=imgtk,
                     anchor=tk.NW  # 좌상단 기준
                     )

win.mainloop()  # GUI 시작
