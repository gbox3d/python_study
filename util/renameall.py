
#%%
import os
import argparse

target_path = './test'

#%%
parser = argparse.ArgumentParser(description="rename all psd file")
parser.add_argument(
    '-t','--target-dir', type=str, 
    help='help : target dir')


#%%
def rename_all(target_path):
    filelist = os.listdir(target_path)
    target_file_list = [_file for _file in filelist if _file.endswith('.psd')]
    target_dir_list = [_dir for _dir in filelist if  os.path.isdir( os.path.join(target_path,_dir))]

    print(target_dir_list)
    
    for _dir in target_dir_list:
        _path = os.path.join(target_path,_dir)
        rename_all(_path)
    
    # rename_all(target_file_list, target_path)
    for _target_file in target_file_list:
        _name = os.path.splitext(_target_file)[0]
        _ext = os.path.splitext(_target_file)[1]

        print(_name.split('_v')[0] + _ext)

        os.rename(
            os.path.join(target_path,_target_file) ,
            os.path.join(target_path,_name.split('_v')[0] + _ext)
            ) 

# pathlib(target_file_list[0])


# %%
rename_all(target_path)
