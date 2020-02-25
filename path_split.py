import os

# path = '../../businfo_v2/script/control_monitor.py'

_path,_file = os.path.split('../../businfo_v2/script/control_monitor.py')

print(_path)
print(_file)

_parent,_temp = os.path.split(_path)

print(_parent)
