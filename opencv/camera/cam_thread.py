#%%
import cv2 as cv 
import sys
import time 
import numpy as np
import threading

import PIL.Image as Image
import PIL.ImageColor as ImageColor
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

from IPython.display import display



# print(sys.argv)

print(cv.__version__)

#%%

class _theApp:
    def __init__(self):
        self.cap = cv.VideoCapture(0)
        
        self.running = True
        t = threading.Thread(target=self._appLoop)
        #주쓰레가 죽으면 같으죽는다. FALSE이면 주쓰레드와 관계없이 계속 동작한다.
        t.daemon = True
        t.start()
        self.threadObj = t

        self._critical_Section = threading.Lock()

    def _appLoop(self) :
        print('thread start')
        cap = self.cap
        
        if cap.isOpened():
            # print(cap)
            width = cap.get(cv.CAP_PROP_FRAME_WIDTH)
            height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)
            print(f'cam ok  {width}:{height}')
        else :
            print('connect failed')
        
        while self.running:
            ret = cap.grab()
            # ret, img = cap.read()
            # if ret:
            #     # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
            # else:
            #     print("cannot read frame.")
        cap.release()
        print('thread end')
    def  _getframe(self) :

        with self._critical_Section :
            while True :
                ret,frame = self.cap.read()
                if ret == True:
                    print('captture success')
                    print(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
                    print(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))


                # cv.imwrite('test.png',frame)
                    _img = cv.cvtColor(frame,cv.COLOR_BGR2RGB)

                    display(Image.fromarray(_img))
                    break;
                else:
                    print('capture failed')


#%% start thread
if __name__== '__main__':
    # app = QApplication(sys.argv)
    app = _theApp()
    # sys.exit(app.exec_())


# %%
app._getframe()
# %%
