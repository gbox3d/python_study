# __init__.py 가하는 역활은 패키지파일들의 경로와 네임스페이스의 기준을 잡아주는 역활을 한다.
from .test import hello
from .test import sayDog as uSayDog # 별명으로 이름 바뀌기
from .rect import Rect