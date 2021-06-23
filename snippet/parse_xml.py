#%%
from xml.etree.ElementTree import parse

print('init paerser');
# %%

tree = parse('sample.xml')

rootNode = tree.getroot()

print(rootNode.find('student'))

print(rootNode.find('student').find("name").text)
print(rootNode.find('student').find("age").text)

# %%
#parsing 
tree = parse('sheet_tanks.xml')
rootNode = tree.getroot()

#%%
#ierator sample 

_iter = rootNode.iter(tag="SubTexture")
for _txdata in _iter :
    print(_txdata.attrib['name'],_txdata.attrib['x'],_txdata.attrib['y'])


# %%
#findall exaample

_sub_txes = rootNode.findall('SubTexture')
for x in _sub_txes:
    print(x.attrib['name'])

# %%
