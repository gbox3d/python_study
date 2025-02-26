
from myTello import MyTello


tello = MyTello()

# 스레드 시작
tello.start()

print("Enter commands to send to Tello. Type 'quit' or 'exit' to stop.")

try:
    while True:
        cmd = input("Command > ")
        if cmd.lower() in ("quit", "exit"):
            break
        elif cmd.lower() == "status":
            tello.send_status_start()
        else:
            tello.send_command(cmd)
except KeyboardInterrupt:
    pass
finally:
    tello.close()