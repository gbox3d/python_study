import sys
import requests

print(sys.version)

#url = "http://redstar001.iptime.org:21310/rest/exec?cmd=cat%20/sys/class/thermal/thermal_zone0/temp" 
url = "http://redstar001.iptime.org:21310/rest/exec" 

response = requests.get(url, params={
    "cmd" : "cat /sys/class/thermal/thermal_zone0/temp"
}) 

print("status code : ",response.status_code)
print("text : ", response.text)




