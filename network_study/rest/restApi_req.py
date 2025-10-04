# %%
import sys
import requests
import json

print(sys.version)


# %% get test
# http://redstar001.iptime.org:17390/hello?name=gbox
# url = "http://redstar001.iptime.org:17390/hello"
url = "http://localhost:10048/hello"

response = requests.get(url, params={
    "name": "gbox"
})

print("status code : ", response.status_code)
print("text : ", response.text)

print(response.json()['msg'])

# %% post sample

response = requests.post('http://localhost:8282/upload',
                         headers={'my-name': 'gbox3d'}, # headert
                         data='hello' # body
                         )

print("status code : ", response.status_code)
print("text : ", response.text)
