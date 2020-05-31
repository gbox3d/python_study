import serial

import argparse

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()

ap.add_argument("-p", "--port", required=True, help="device port")

args = vars(ap.parse_args())


print(args['port'])

ser = serial.Serial(port=args['port'],baudrate=115200)

ser.write(b'd')
ser.flush()

print(f'{ser.readline()}')
print(f'{ser.readline()}')

# while True:
#     print(f'{ser.readline()} \n')


ser.close()

