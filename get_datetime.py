from datetime import datetime
import time

# datetime object containing current date and time
now = datetime.now()
 
print("now =", now)


print("now time =" + now.strftime("%H%M"))

# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("date and time =", dt_string)	

print(now.timetuple())
#time stamp   변환 
print(time.mktime(now.timetuple()))

#참고 : https://inma.tistory.com/96
