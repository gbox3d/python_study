# PySide6 (QT for Python 공식 포트)

PySide6는 Qt for Python의 공식 포트이다.  
PySide6는 Qt 6의 최신 버전을 지원한다.  

## Library Installation



**호환성**  
6.7 버전 2024년 8월 현재 , python 3.11, 3.12 실행확임됨.  

```bash
pip install PySide6
```

## 유티리티 사용하기

**designer 실행**  
```bash
pyside6-designer
```

**리소스 컴파일러**  
```bash
pyside6-rcc assets.qrc -o _rc.py
```


## venv 환경에서 사용하기

```bash
source ../../.venv/bin/activate

```


## venv 환경 아래에서 launch.json 설정법 


lauch.json 파일은 다음과 같이 설정합니다.  

```json
{
    
    "configurations": [
        {
            "type": "debugpy",
            "request": "launch",
            "name": "Launch Current Venv",
            "python": "${workspaceFolder}/.venv/bin/python", // 가상환경을 사용하고 있다면 python 경로를 가상환경의 python 경로로 설정해야 합니다.  
            //"program": "${workspaceFolder}/${input:programPath}",
            "program": "${file}",
            "cwd": "${fileDirname}", //cwd는 현재 파일이 있는 디렉토리로 설정해야 합니다.  
            "console": "integratedTerminal",
        },
        {
            "name": "Python 디버거: 현재 파일",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal"
        }
    ],
    "inputs": [
        {
            "type": "promptString",
            "id": "programPath",
            "description": "Enter the relative path to the main Python file"
        }
    ]
}
```



## 참고자료
qt 파이썬 공식 포트는 pyside6 이다.  
https://wiki.qt.io/Qt_for_Python  
https://pypi.org/project/PySide6    

강좌
https://www.pythonguis.com/pyside6/

