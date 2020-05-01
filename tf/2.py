# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# ##### 참고자료
# 
# https://cyc1am3n.github.io/2018/09/13/how-to-use-dataset-in-tensorflow.html
# https://m.blog.naver.com/PostView.nhn?blogId=atelierjpro&logNo=221595798266&proxyReferer=https:%2F%2Fwww.google.com%2F
# 
# 

# %%
import tensorflow as tf
import numpy as np

print( f'tensor versio : {tf.__version__}')


# %%
# https://m.blog.naver.com/PostView.nhn?blogId=atelierjpro&logNo=221595798266&proxyReferer=https:%2F%2Fwww.google.com%2F

input = np.array([[0,0],[0,1],[1,0],[1,1]]).astype(np.float)
output = np.array([[0],[1],[1],[0]]).astype(np.float)

train_dataset = tf.data.Dataset.from_tensor_slices((input,output))
test_dataset = tf.data.Dataset.from_tensor_slices((input,output))


# %%
print(train_dataset)


# %%
BATCH_SIZE=1
SHUFFLE_BUFFER_SIZE = 4
train_dataset = train_dataset.shuffle(SHUFFLE_BUFFER_SIZE).batch(BATCH_SIZE)
test_dataset = test_dataset.batch(BATCH_SIZE)

# %% [markdown]
# 데이터셋 이터레이숀 예제 

# %%
for element in train_dataset: 
  print(element[0].numpy() )


# %%


