import ftplib
import os

filename = "./dprk2.jpg"
ftp=ftplib.FTP()

print("connecting.. ")

ftp.connect("ip address",21)
ftp.login("id","passwd")

ftp.cwd("./temp")

print("uploading...")
os.chdir("./python")
fd = open(filename,'rb')
ftp.storbinary('STOR ' +filename, fd )
fd.close()

print("complete.")