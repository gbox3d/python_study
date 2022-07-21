## conver dataset

```bash
python voc2coco.py -d=/home/ubiqos-ai2/work/datasets/bitles -n=dic_1009 -o=/home/ubiqos-ai2/work/visionApp/datasets/dic_1009/anno.json
python voc2coco.py -d=/home/ubiqos-ai2/work/visionApp/datasets/test3 -n=fruts_nuts -o=/home/ubiqos-ai2/work/visionApp/datasets/test3/fruts_nuts/anno.json
python voc2coco.py -d=/home/ubiqos-ai2/work/visionApp/datasets/test3 -n=dic_1004 -o=/home/ubiqos-ai2/work/visionApp/datasets/test3/dic_1004/anno.json

python voc2coco.py -d=/home/ubiqos/work/dataset/test1/202271004 -n=dic_1004 -o=/home/ubiqos/work/visionApp/annos/dic_1004/anno.json
python voc2coco.py -d=/home/ubiqos/work/dataset/test1/dic_1009 -n=dic_1009 -o=/home/ubiqos/work/visionApp/annos/dic_1009/anno.json

python voc2coco.py -d=/home/ubiqos/work/dataset/test2/dic_1011 -n=dic_1011 -o=/home/ubiqos/work/visionApp/annos/dic_1011/anno.json
python voc2coco.py -d=/home/ubiqos/work/dataset/test2/dic_hongy15 -n=dic_hongy15 -o=/home/ubiqos/work/visionApp/annos/dic_hongy15/anno.json
python voc2coco.py -d=/home/ubiqos/work/dataset/test2/dic_sso3961 -n=dic_sso3961 -o=/home/ubiqos/work/visionApp/annos/dic_sso3961/anno.json

```


## dataset split

```bash
#validation dataset 은 나머지 데이터들을 가지고 계산한다.  
python coco_spliter.py --img-path=../../../../datasets/mushroom_data/yangsongyi/_image --json-path=../../../../datasets/mushroom_data/yangsongyi/_label/data.json --output-path=./output --train-ratio=0.8 --test-ratio=0.1

#validation dataset 을 10% 로 지정 
python coco_spliter.py --img-path=../../../../datasets/mushroom_data/yangsongyi/_image --json-path=../../../../datasets/mushroom_data/yangsongyi/_label/data.json --output-path=./output --train-ratio=0.8 --test-ratio=0.1 --val-ratio=0.1


#validation dataset 을 skip
python coco_spliter.py --img-path=/home/ubiqos-ai2/work/datasets/bitles/images --json-path=/home/ubiqos-ai2/work/visionApp/datasets/dic_1009/anno.json --output-path=/home/ubiqos-ai2/work/visionApp/datasets/dic_1009/  --train-ratio=0.8



python coco_spliter.py --img-path=/home/ubiqos-ai2/work/visionApp/datasets/test3/fruts_nuts --json-path=/home/ubiqos-ai2/work/visionApp/datasets/test3/fruts_nuts/anno.json --output-path=/home/ubiqos-ai2/work/visionApp/datasets/test3/fruts_nuts  --train-ratio=0.8

python coco_spliter.py --img-path=/home/ubiqos-ai2/work/visionApp/datasets/test3/dic_1004 --json-path=/home/ubiqos-ai2/work/visionApp/datasets/test3/dic_1004/anno.json --output-path=/home/ubiqos-ai2/work/visionApp/datasets/test3/dic_1004  --train-ratio=0.8


```

## mergy

cmd 파일 예시

```yaml
list:
  - '/home/ubiqos/work/visionApp/annos/dic_1011/anno.json'
  - '/home/ubiqos/work/visionApp/annos/dic_hongy15/anno.json'
  - '/home/ubiqos/work/visionApp/annos/dic_sso3961/anno.json'
  - /home/ubiqos/work/visionApp/annos/dic_1004/anno.json
  - /home/ubiqos/work/visionApp/annos/dic_1009/anno.json
save_name: '../../../annos/all.json'
```

예>
```bash
python coco_mergy.py -c ./settings/mergy_cmd.yaml
```

## settings 

여기서 사용되는 모든 스크립트의 실행 설정은 settings.yaml 파일에서 설정을 읽어서 사용한다.


예제파일 


```yaml
dataset:
  name: "dic_1004"
cfg:
  base_config_file: "COCO-InstanceSegmentation/mask_rcnn_R_50_C4_1x.yaml"
  max_iter: 1000
  ims_per_batch : 2
  config_dir: "./configs"
  output_dir: "./output/dic_1004/mask_rcnn_R_50_C4_1x"
train_set: 
  anno: "/home/ubiqos-ai2/work/visionApp/datasets/test3/dic_1004/train.json"
  img_dir: "/home/ubiqos-ai2/work/visionApp/datasets/test3/dic_1004/voc"
test_set: 
  anno: "/home/ubiqos-ai2/work/visionApp/datasets/test3/dic_1004/test.json"
  img_dir: "/home/ubiqos-ai2/work/visionApp/datasets/test3/dic_1004/voc"

```

make_cfg.py 로 config.yaml 파일 생성  

```
python make_cfg.py -s ./settings/cauda.yaml
```

## train


train_net.py로 훈련  

```sh
python train_net.py --config-file ./configs/AmericanMushromms/config.yaml --num-gpus 2
python train_net.py --config-file ./configs/mushroom_data/config.yaml --num-gpus 2
python train_net.py --config-file "./configs/Microcontroller Segmentation_config.yaml"  --num-gpus 1
python train_net.py --config-file ./configs/cauda_config.yaml -s ./settings/cauda.yaml  --num-gpus 1
python train_net.py --config-file ./configs/fruit_config.yaml -s ./settings/fruit.yaml  --num-gpus 1

python train_net.py --config-file ./configs/dic_1004_config.yaml -s ./settings/dic_1004.yaml  --num-gpus 1
```
