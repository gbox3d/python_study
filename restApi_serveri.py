
# -*- coding: utf-8 -*- 한글 주석 사용하기 위하여 
# 태스트  : http://localhost:8000/test?name=gbox
# 참고자료 : https://m.blog.naver.com/PostView.nhn?blogId=wideeyed&logNo=221350669178&proxyReferer=https%3A%2F%2Fwww.google.com%2F
# pip install flask

from flask import Flask, escape, request

app = Flask(__name__)

@app.route('/test')
def hello():
    name  = request.args.get("name")
    return {"name" : name}

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8000, debug=True)

