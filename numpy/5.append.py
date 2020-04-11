import numpy as np

x1 = np.array([
    [[101,131]],
    [[101,237]],
    [[248,237]],
    [[248,131]]
    ])

#리스트를 만든 다음 배열로 전환
_tmp=[] 
for _ in x1 : 
    _tmp.append(_)
print(np.array(_tmp) )

# [] 1단계 차원을 내려서 배열에 쌓기
_tmp = []
for _ in x1 : 
    _tmp.append(_[0])
print(np.array(_tmp) )

#단순화 시킨방법
_tmp = [_[0] for _ in x1 ]
print( np.array( _tmp ))



