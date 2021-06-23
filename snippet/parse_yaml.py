#%%
import yaml
with open('./sample.yaml') as f :
    _config = yaml.load(f, Loader=yaml.FullLoader)
    print(_config)

#%%
print(_config['title'])
print(f'mas spped : { _config["max_speed"] } ')
# %%
print(_config['bank_objs'][0]['url'])
# %%
