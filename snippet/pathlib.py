#%%
from pathlib import Path


#%% 디랙토리 리스팅 

_path  = Path('../')

for _dir in _path.iterdir() :
    print(_dir)

# %% 전체 리스팅
_files = _path.glob('*')
for _file in _files:
    # print(_file)
    if _file.is_file() :
        print(_file)
        print(_file.resolve()) # full path 
    elif _file.is_dir() :
        print('dir : ' , _file)

# %% 멤버변수 

_p = Path('/usr/local/test.tar.gz')

print(_p.name)
print(_p.parts)
print(_p.suffix) # 확장자 구하기 
print(_p.suffixes)
print(_p.stem) # 확장자뺀 이름만 

print(_p.match('*.gz')) # 패턴 매칭 
print(_p.match('*.jpg'))

print( f'file is exist { _p.exists() } ' ) # 존재여부 


# %%텍스트 파일 생성 
_p = Path('./test2.txt')
_p.write_text('hello  pathlib')
print(_p.read_text())

# %% rename file
__p = _p.rename('./test3.txt')

# %% delete file
Path('./test3.txt').unlink()
# %%
