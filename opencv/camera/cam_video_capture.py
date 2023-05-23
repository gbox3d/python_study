#%%
import cv2 as cv

#%%
cap = cv.VideoCapture(0)
if cap.isOpened():
    # print(cap)
    print(f'cam ok')
else :
    print('connect failed')

#%%
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('output.avi',fourcc,20.0,(640,480))

##%%
while True :
    ret,frame = cap.read()
    
    #write video file
    out.write(frame)
    
    #show video
    cv.imshow('frame',frame)
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
#%%
cap.release()
out.release()
cv.destroyAllWindows()