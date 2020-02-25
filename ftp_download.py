import ftplib
import os

filename = "heap1.jpg"
ftp=ftplib.FTP()

print("connecting.. ")
ftp.connect("ip address",21)
ftp.login("id","passwd")

ftp.cwd("./temp")



print("downloading...")
fd = open("./" + filename,'wb')
ftp.retrbinary("RETR " + filename, fd.write)
fd.close()

print("complete.")