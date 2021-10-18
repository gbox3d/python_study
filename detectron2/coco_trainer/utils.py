#%%
import os
from detectron2.data.datasets import register_coco_instances

#%%
def loadCocoDataset(dataset_path,dataset_name,anno_file_name='_annotations.coco.json') :

    # dataset_path = '../../../../datasets'
    # dataset_name = 'AmericanMushromms'

    for d in ["train","test","valid"]:
        register_coco_instances(
            f"{dataset_name}_{d}", 
            {},
            os.path.join(dataset_path,dataset_name,d,anno_file_name),
            # f"{}/{d}.json",
            os.path.join(dataset_path,dataset_name,d)
        )
        print(f"{dataset_name}_{d}",os.path.join(dataset_path,dataset_name,d))

# %%
