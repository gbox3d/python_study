import numpy as np

x2 = np.array([
    [[101,131]],
    [[101,237]],
    [[248,237]],
    [[248,131]]
    ])

# print(x2[:,:,0].argmin())
# print( np.amin(x2[:,:,0]))

test = []
# np.array(test)

# test.append(1)

# test.append([1])


# test.append([[101,131]])

# print(test)

for n in range(len(x2)) :
    test.append( x2[n,0] ) 

print(np.array(test))

# print(np.array(test))
# _copy = np.array([])

# print([ _x2 for _x2 in x2 if _x2[0,1] > 200])


# _copy = np.append(_copy,np.array([[1],[2],[3]]))
# print(_copy)
# _copy = np.append(_copy,[[1,2]])
# for _x2 in x2 :
#     # print(_x2)
#     _copy = np.append(_copy,[_x2])
#     # np.vstack(_copy,_x2)
#     # np.append(_copy,_x2)

# print(_copy)

# print(x2[0,0])
# print(np.vstack( [x2[0,0],x2[1,0]]  ))
# print(_copy,x2[n,0])

