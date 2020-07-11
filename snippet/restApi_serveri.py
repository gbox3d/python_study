
# -*- coding: utf-8 -*- 한글 주석 사용하기 위하여 
# 태스트  : http://localhost:8000/hello?name=gbox
# 참고자료 : https://m.blog.naver.com/PostView.nhn?blogId=wideeyed&logNo=221350669178&proxyReferer=https%3A%2F%2Fwww.google.com%2F
# pip install flask
#%%
from datetime import datetime
import sys
from flask import Flask, escape, request
from pathlib import Path

print(sys.version)
# print(sys.argv[0])

#%%
_port=8086
_host = "localhost"
#쥬피터 환경일경우
if Path(sys.argv[0]).name == 'ipykernel_launcher.py' :
    print('can not run in ipykernel_launcher')
    quit()
elif len(sys.argv) > 1 : 
        print(sys.argv[1])
        _port = int(sys.argv[1])

#%%
app = Flask(__name__)

@app.route('/hello')
def hello():
    name  = request.args.get("name")
    if name :
        return {"msg" : f'hello {name}' }
    else : return {"msg" : 'just say hello , usage ?name=ur name' }

@app.route('/getTime')
def getTime():
    return {"time" : datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

if __name__ == '__main__':
    print('start port : ' + str(_port) )
    app.run(host=_host, port=_port, debug=True)

