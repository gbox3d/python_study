
# -*- coding: utf-8 -*- 한글 주석 사용하기 위하여 
# 태스트  : http://localhost:8000/hello?name=gbox
# 참고자료 : https://m.blog.naver.com/PostView.nhn?blogId=wideeyed&logNo=221350669178&proxyReferer=https%3A%2F%2Fwww.google.com%2F
# pip install flask

from datetime import datetime
import sys
from flask import Flask, escape, request

print(sys.version)

_port=8000
if len(sys.argv) > 1 : 
    print(sys.argv[1])
    _port = int(sys.argv[1])

app = Flask(__name__)

@app.route('/hello')
def hello():
    name  = request.args.get("name")
    return {"msg" : 'hello' + name}

@app.route('/getTime')
def getTime():
    return {"time" : datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

if __name__ == '__main__':
    print('start port : ' + str(_port) )
    app.run(host='0.0.0.0', port=_port, debug=True)

