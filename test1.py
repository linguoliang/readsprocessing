import numpy as np
import matplotlib.pyplot as plt
import math

def finddata(points,l,r,container,x1,x2,contact,long=1000,resolution=1000):
    x1eq=(l[points==x1]<x2)&(r[points==x1]>x2)
    x2eq=(points==x2)&(l<x1)&(r>x1)
    # x1data=(x2-points[x1eq])//resolution+long
    print(x1eq)
    # container[x1eq]=1
    # print(container)
    # print(x1data)
    n=np.argwhere(points==x1)
    n=n.flatten()
    print(n)
    container[n,(x2-points[points==x1])//resolution+long]=contact
    container[x2eq,(x1-points[points==x2])//resolution+long]=contact
    # print(container)
    return container

points=np.array([12,49,57,58,59,71])
container=np.zeros((len(points),4))
# print(container)
l=points-5
r=points+5
x1=58
x2=59
contact=1.5
container=finddata(points,l,r,container,x1,x2,contact,2,1)
print(container)