#%%
import configparser

#%%
config = configparser.ConfigParser()
config.read('test.ini')

print(config['SERIAL']['PORT'])     
print(config['SYSTEM']['CLIENT_STATE_SEND'])



# %%

# instantiate
_config = configparser.ConfigParser()
_config.add_section('SERIAL')
_config.set('SERIAL','PORT','COM3')
# _config['SERIAL']['PORT'] = 'COM3'
with open('FILE.INI', 'w') as configfile:    # save
    _config.write(configfile)


# %%
