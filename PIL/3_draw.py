# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% 모듈로딩 
import numpy as np

import PIL.Image as Image
import PIL.ImageColor as ImageColor
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

from IPython.display import display

print('load module ok')


# %%
_test_img = Image.open('../res/shally.jpg')

display(_test_img)


# %% 새로운 빈이미지 만들고 거기에 잘라낸 이미지 붙이기
_img = Image.new('RGB',(800,600),(255,255,255))

drawer = ImageDraw.Draw(_img)

#잘라내기
#crop의 인자 전달수서는 시작위치xy, 끝위치xy
_crop_img = _test_img.crop((600,200,800,700))

#붙이기
_img.paste(_crop_img,(200,100))

# _img.paste(_test_img,(0,0,200,200))

#글씨 출력
drawer.text((100,100),"hello",fill="red")

#선그리기
drawer.line([(0,0),(800,0),(800,600),(0,600),(0,0)],width=8,fill=(0,255,0))

display(_img)

# %%
