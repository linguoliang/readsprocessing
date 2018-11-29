import numpy as np
import matplotlib.pyplot as plt
import math

def finddata(points,l,r,container,x1,x2,contact,long=1000,resolution=1000):
    x1eq=(l[points==x1]<=x2)&(r[points==x1]>x2)
    x2eq=(l[points==x2]<=x1)&(r[points==x2]>x1)
    # x1data=(x2-points[x1eq])//resolution+long
    print(x2eq)
    # container[x1eq]=1
    # print(container)
    # print(x1data)
    n1=np.argwhere(points==x1)
    # n1=n1.flatten()
    n2=np.argwhere(points==x2)
    # print(n)
    if len(x1eq)>0 and x1eq[0]:
        container[n1,(x2-points[points==x1])//resolution+long]=contact
    if len(x2eq)>0 and x2eq[0]:
        container[n2,(x1-points[points==x2])//resolution+long]=contact
    # print(container)
    return container

points=np.array([12,49,57,58,59,71])
container=np.zeros((len(points),4))
# print(container)
l=points-2
r=points+2
x1=57
x2=56
contact=1.5
container=finddata(points,l,r,container,x1,x2,contact,2,1)
print(container)