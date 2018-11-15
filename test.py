import matplotlib.pyplot as plt
import numpy as np
# y=np.arange(1,5)
# x=np.arange(4,5,0)
# plt.plot(x,y)
# plt.show()
# def name(infile):
#     while True:
#         p=infile.tell()
#         x=infile.readline()
#         if x.find("werqwer")==-1:
#             pass
#         else:
#             print("in name is {}".format(x))
#             infile.seek(p)
#             break
# with open("test.txt") as infile:
#     name(infile)
#     m=infile.readline()
#     print("out name is {}".format(m))
# m=[[22,33],[44,55]]
# def x(x,c,v,b):
#     print([x,c,v,b])
# x(**m)
# import os
# print(os.getcwd())
# print(os.path.exists(os.getcwd()+'/'))
import itertools
# x,y='chr1'.split('dd')
import numpy as np
# m=np.zeros((2,3))
# x=np.ones((2,2))
#
# print(np.vstack((m,x)))
# x=np.array([[3,12,4],[66,5,77]])
# print (x.shape)
# x=float("0.000000232423")
# print(x)

# for i in x:
#     for j in x:
#         print(i,j)
#     print(3//2)
# print('straw VC VC inter.hic {0} {1} BP 500000 > {0}_{1}.txt'.format(*(12,23)))

import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict
from matplotlib.transforms import blended_transform_factory

linestyles = OrderedDict(
    [('solid',               (0, ())),
     ('loosely dotted',      (0, (1, 10))),
     ('dotted',              (0, (1, 5))),
     ('densely dotted',      (0, (1, 1))),

     ('loosely dashed',      (0, (5, 10))),
     ('dashed',              (0, (5, 5))),
     ('densely dashed',      (0, (5, 1))),

     ('loosely dashdotted',  (0, (3, 10, 1, 10))),
     ('dashdotted',          (0, (3, 5, 1, 5))),
     ('densely dashdotted',  (0, (3, 1, 1, 1))),

     ('loosely dashdotdotted', (0, (3, 10, 1, 10, 1, 10))),
     ('dashdotdotted',         (0, (3, 5, 1, 5, 1, 5))),
     ('densely dashdotdotted', (0, (3, 1, 1, 1, 1, 1)))])


plt.figure(figsize=(10, 6))
ax = plt.subplot(1, 1, 1)

X, Y = np.linspace(0, 100, 10), np.zeros(10)
for i, (name, linestyle) in enumerate(linestyles.items()):
    print(i,name,linestyle)
    ax.plot(X, Y+i, linestyle=linestyle, linewidth=1.5, color='black')

ax.set_ylim(-0.5, len(linestyles)-0.5)
plt.yticks(np.arange(len(linestyles)), linestyles.keys())
plt.xticks([])

# For each line style, add a text annotation with a small offset from
# the reference point (0 in Axes coords, y tick value in Data coords).
reference_transform = blended_transform_factory(ax.transAxes, ax.transData)
for i, (name, linestyle) in enumerate(linestyles.items()):
    ax.annotate(str(linestyle), xy=(0.0, i), xycoords=reference_transform,
                xytext=(-6, -12), textcoords='offset points', color="blue",
                fontsize=8, ha="right", family="monospace")

plt.tight_layout()
plt.show()


# define your functions here!
import matplotlib.pyplot as plt

t = np.arange(-1, 2, .01)
s = np.sin(2 * np.pi * t)

plt.plot(t, s)
# Draw a thick red hline at y=0 that spans the xrange
plt.axhline(linewidth=8, color='#d62728')

# Draw a default hline at y=1 that spans the xrange
plt.axhline(y=1)

# Draw a default vline at x=1 that spans the yrange
plt.axvline(x=1)

# Draw a thick blue vline at x=0 that spans the upper quadrant of the yrange
plt.axvline(x=0, ymin=0.75, linewidth=8, color='#1f77b4')

# Draw a default hline at y=.5 that spans the middle half of the axes
plt.axhline(y=.5, xmin=0.25, xmax=0.75)

plt.axhspan(0.25, 0.75, facecolor='0.5', alpha=0.5)

plt.axvspan(1.25, 1.55, facecolor='#2ca02c', alpha=0.5)

plt.axis([-1, 2, -1, 2])

plt.show()
