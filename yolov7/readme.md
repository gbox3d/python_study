# 섳치하기

먼저 yolov7를 구현해놓은 소스를 받아옵니다.  
```
git clone https://github.com/WongKinYiu/yolov7
cd yolov7
git checkout pose

```

# 출력 결과물 포멧

```
pred = model(imgs, augment=False)[0]
```



0 ~ 6 : (bbox(4),class,conf)   

6 ~ : keypoint (x,y,0) 총 17개  

0 : "nose",  
1: "left_eye",  
2: "right_eye",  
3: "left_ear",  
4: "right_ear",  
5: "left_shoulder",
6: "right_shoulder",
7: "left_elbow" 팔꿈치  
8: "right_elbow",  
9 : "left_wrist",  
10 : "right_wrist",  
11 : "left_hip",  
12 : "right_hip",  
13 : "left_knee",  
14 : "right_knee",  
15 : "left_ankle",  
16 : "right_ankle"  