import numpy as np
def consine(x,y):
    x = np.array(x)
    y = np.array(y)
    return x.dot(y)/(np.linalg.norm(x)*np.linalg.norm(y))