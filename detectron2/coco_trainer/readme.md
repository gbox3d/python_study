## dataset split


```bash
#validation dataset 은 나머지 데이터들을 가지고 계산한다.  
python coco_spliter.py --img-path=../../../../datasets/mushroom_data/yangsongyi/_image --json-path=../../../../datasets/mushroom_data/yangsongyi/_label/data.json --output-path=./output --train-ratio=0.8 --test-ratio=0.1

#validation dataset 을 10% 로 지정 
python coco_spliter.py --img-path=../../../../datasets/mushroom_data/yangsongyi/_image --json-path=../../../../datasets/mushroom_data/yangsongyi/_label/data.json --output-path=./output --train-ratio=0.8 --test-ratio=0.1 --val-ratio=0.1

#validation dataset 을 skip
python coco_spliter.py --img-path=../../../../datasets/mushroom_data/yangsongyi/_image --json-path=../../../../datasets/mushroom_data/yangsongyi/_label/data.json --output-path=./output --train-ratio=0.8 --test-ratio=0.1 --val-ratio=-1


```

## train

ex04_make_cfg.py 로 config.yaml 파일 생성  
train_net.py로 훈련  

```sh
python train_net.py --config-file ./configs/AmericanMushromms/config.yaml --num-gpus 2
python train_net.py --config-file ./configs/mushroom_data/config.yaml --num-gpus 2
```
