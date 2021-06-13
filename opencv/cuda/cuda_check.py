#%%
import cv2 as cv
print(f'cv version : {cv.__version__}')
#%%
print(f'cuda devicee num : { cv.cuda.getCudaEnabledDeviceCount() }')
