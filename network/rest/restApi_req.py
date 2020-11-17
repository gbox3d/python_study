#%%
import sys
import requests
import json

print(sys.version)


#http://redstar001.iptime.org:17390/hello?name=gbox
# url = "http://redstar001.iptime.org:17390/hello"
url = "http://localhost:10048/hello"

response = requests.get(url, params={
    "name" : "gbox"
}) 

print("status code : ",response.status_code)
print("text : ", response.text)

print(response.json()['msg'])





# %%
