#%%
from djitellopy import Tello
import cv2

from djitellopy import Tello
import cv2

tello = Tello()
tello.connect()
print("Battery:", tello.get_battery())
# %%
