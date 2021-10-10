# detectron study

## setup

**설치전 준비물**  
```sh
pip install pyyaml==5.1
pip install avro-python3 
pip install httplib2 
pip install pytz

pip install opencv-python
```

**install detectron2**
```sh
# torch 1.9 용 프리빌드 버전 설치 (리눅스)
pip3 install torch==1.9.1+cu111 torchvision==0.10.1+cu111 torchaudio==0.9.1 -f https://download.pytorch.org/whl/torch_stable.html
```

## train

ex04_make_cfg.py 로 config.yaml 파일 생성  
train_net.py로 훈련  

```sh
python train_net.py --num-gpus 2 --config-file ./configs/config.yaml
```

setup 함수 윗부분에 아래코드 추가 하여 데이터셋 등록  
```py
for d in ["train", "test"]:
        register_coco_instances(
        f"microcontroller_{d}", # 데이터셋 이름 
        {},
        f"../../datasets/Microcontroller Segmentation/{d}.json", # label
        f"../../datasets/Microcontroller Segmentation/{d}" # image
    )

```