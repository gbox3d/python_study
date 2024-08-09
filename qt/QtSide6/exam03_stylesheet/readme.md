## 해당 QLabel 객체에 직접 스타일시트를 설정하는 방법

Qt Designer에서 QLabel 선택:

QLabel을 선택합니다.
속성 편집기(Properties)에서 스타일시트 설정:

QLabel의 styleSheet 항목을 찾아서 다음과 같이 설정합니다.
```css 
color: red;
```
이렇게 하면 선택한 QLabel 객체에만 텍스트 색상이 빨간색으로 설정됩니다.

예시>  

QLabel 선택:  
QLabel 위젯을 선택합니다.  

속성 편집기에서 스타일시트 설정:  
styleSheet 항목에 color: red;를 입력합니다.

## 속성 샘플

**border 속성을 추가하려면 다음과 같이 설정합니다.** 
```css
color: red;
border: 2px solid blue;
```

**배경색 바꾸기** 
```css
background-color: yellow;
```

**폰트 크기 바꾸기** 
```css
font-size: 20px;
```

**모서리 둥글게 만들기** 
```css
border-radius: 10px;
```

## 리소스 파일 생성

**리소스 컴파일러**
```bash
pyside6-rcc assets.qrc -o _rc.py
```


