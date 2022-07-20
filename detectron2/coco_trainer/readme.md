## conver dataset

```bash
python voc2coco.py -d=/home/ubiqos-ai2/work/datasets/bitles -n=dic_1009 -o=/home/ubiqos-ai2/work/visionApp/datasets/dic_1009/anno.json
python voc2coco.py -d=/home/ubiqos-ai2/work/visionApp/datasets/test3 -n=fruts_nuts -o=/home/ubiqos-ai2/work/visionApp/datasets/test3/fruts_nuts/anno.json
python voc2coco.py -d=/home/ubiqos-ai2/work/visionApp/datasets/test3 -n=dic_1004 -o=/home/ubiqos-ai2/work/visionApp/datasets/test3/dic_1004/anno.json

```
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

## settings 

여기서 사용되는 모든 스크립트의 실행 설정은 settings.yaml 파일에서 설정을 읽어서 사용한다.


예제파일 


```yaml
dataset:
  name: "Microcontroller Segmentation"
  train_set: 
    anno: "/home/ubiqos-ai2/work/visionApp/datasets/Microcontroller Segmentation/train.json"
    img_dir: "/home/ubiqos-ai2/work/visionApp/datasets/Microcontroller Segmentation/train"
  test_set: 
    anno: "/home/ubiqos-ai2/work/visionApp/datasets/Microcontroller Segmentation/test.json"
    img_dir: "/home/ubiqos-ai2/work/visionApp/datasets/Microcontroller Segmentation/test"
  val_set: 
    anno: "/home/ubiqos-ai2/work/visionApp/datasets/Microcontroller Segmentation/val.json"
    img_dir: "/home/ubiqos-ai2/work/visionApp/datasets/Microcontroller Segmentation/val"
eval: 
  anno: "/home/ubiqos-ai2/work/visionApp/datasets/Microcontroller Segmentation/test.json"
  img_dir: "/home/ubiqos-ai2/work/visionApp/datasets/Microcontroller Segmentation/test"
  weight: "/home/ubiqos-ai2/work/visionApp/python_study/detectron2/coco_trainer/output/model_final.pth" 
cfg:
  base_config_file: "COCO-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_3x.yaml"
  max_iter: 1000
  ims_per_batch : 2
config_dir: "./test/configs"
output_dir: "./test/output"

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
