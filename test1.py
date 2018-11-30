# import numpy as np
#
#
# def finddata(points, leftmargin, rightmargin, container, x1, x2, contact, long=1000, resolution=1000):
#     x1eq = (leftmargin[points == x1] <= x2) & (rightmargin[points == x1] > x2)
#     x2eq = (leftmargin[points == x2] <= x1) & (rightmargin[points == x2] > x1)
#     if len(x1eq) > 0 and x1eq[0]:
#         n1 = np.argwhere(points == x1)
#         container[(x2 - points[points == x1]) // resolution + long,n1] = contact
#     if len(x2eq) > 0 and x2eq[0]:
#         n2 = np.argwhere(points == x2)
#         container[ (x1 - points[points == x2]) // resolution + long,n2] = contact
#     return container
#
#
# points = np.array([12, 49, 57, 58, 59, 71])
# container = np.zeros((4,len(points)))
# # print(container)
# l = points - 2
# r = points + 2
# x1 = 59
# x2 = 58
# contact = 1.5
# container = finddata(points, l, r, container, x1, x2, contact, 2, 1)
# print(container)

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

means=np.load("chrom1_bkgd.npy")
x=np.arange(0,1000)
xa=(x+174305)*1000
# x={1:np.random.randint(10,50,49).tolist(),
#    2:np.random.randint(10,50,50).tolist(),
#    3:np.random.randint(10,50,50).tolist()}
# # m=[1,2,3]
# x[1].append(None)
#
# y=pd.DataFrame(x)
# mean=y.mean()
# std=y.std()
# stderr=std/np.sqrt(50)
# print(std)
# CI=stats.norm.interval(0.95,loc=mean,scale=std)
# print(CI)
# y[2][49]=None
# y[3][49]=None
# y=y.dropna()
# n = stats.describe(y[1])
# print(n)
# print(np.array(y.mean()))
# np.save("chrom1_bkgd.npy",y.mean())
# plt.plot(m,y.mean())
# plt.show()
# y=np.load("chrom1_bkgd.npy")
df=pd.read_csv("chrom1_RSdata.txt",sep='\t',index_col=0)
# print(df)
intron=df["174305127-ex15-int15__174320502-int15"]
intronarr=np.array(intron)
# print()
print(xa)
plt.plot(xa[5:100],intronarr[1005:1100],color='g')
plt.plot(xa[5:100],means[5:100],color='r')
plt.axvline(x=174320502,linewidth=1, color='b')
# plt.axvline(x=174193000,linewidth=1, color='b')
plt.show()
# print(means)
#
# for x in range(0,1):
#     print(x)

