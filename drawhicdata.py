#!/usr/bin/env python3
# coding=utf-8
import optparse
import time
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math

__author__ = 'Guoliang Lin'
Softwarename = 'drawhicdata.py'
version = '0.0.1'
bugfixs = ''
__date__ = '2018/11/13'


def printinformations():
    print("%s software version is %s in %s" % (Softwarename, version, __date__))
    print(bugfixs)
    print('Starts at :' + time.strftime('%Y-%m-%d %H:%M:%S'))


def programends():
    print('Ends at :' + time.strftime('%Y-%m-%d %H:%M:%S'))


# add your options here! 
def _parse_args():
    """Parse the command line for options."""
    usage = 'usage: %prog -i INPUT -o OUTPUT'
    parser = optparse.OptionParser(usage)
    parser.add_option('-i',
                      '--input', dest='input', type='string',
                      help='input file!')
    #    parser.add_option('-f','--fpkm',dest='fpkm_file',type='string',help='input fpkm file')
    #    parser.add_option('-v','--variation', dest='variation', type='string', help='input variation information file')
    #    parser.add_option('-g', '--gff3', dest='gff', help='gff3 file')
    parser.add_option('-o', '--output', dest='output', type='string', help='output file')
    options, args = parser.parse_args()
    # positional arguments are ignored
    return options

chromosomeDict={}
chromosomeMaxtrix={}
blocksize=np.zeros((50))
growblocksize=np.zeros((50))
ticks=np.zeros((50))
keys=np.arange(1,51)
with open("Carassius.auratus.build.company.chr.sizes") as infile:
    for item in infile:
        item=item.strip()
        chrom,size=item.split('\t')
        chrom=chrom.replace("chr",'')
        chromosomeDict[int(chrom)]=int(size)
        blocksize[int(chrom)-1]=math.ceil(int(size)/1000000)
for i in keys:
    growblocksize[i-1]=np.sum(blocksize[0:i])
    if i>1:
        ticks[i-1]=np.sum(blocksize[0:i-1])+blocksize[i-1]//2
    else:
        ticks[i-1]=blocksize[i-1]//2

data=np.load("1M.npy")
# data1=np.sqrt(data)
m=sns.light_palette('red',as_cmap=True)
fig=sns.heatmap(data,vmax=2000,cmap=m,cbar=False)
# cbar_kws={"shrink": 0.5}
# color="#777777"
# for m in growblocksize:
#     print(m)
#     plt.axhline(y=m,linewidth=.5, color=color)
#     plt.axvline(x=m,linewidth=.5, color=color)
# color1="#000000"
# plt.axhline(y=0,linewidth=2, color=color1)
# plt.axvline(x=0,linewidth=2, color=color1)
# plt.axhline(y=max(growblocksize),linewidth=2, color=color1)
# plt.axvline(x=max(growblocksize),linewidth=2, color=color1)
# plt.yticks(ticks,keys)
# plt.xticks(ticks,keys)
plt.yticks([])
plt.xticks([])
plt.savefig("test_final.png",dpi=300,quality=95)
# ax = plt.gca()
# ax.spines['top'].set_visible(True)
# ax.spines['bottom'].set_visible(True)
# ax.spines['left'].set_visible(True)
# ax.spines['right'].set_visible(True)
plt.show()


if __name__ == '__main__':
    printinformations()
    options = _parse_args()
    # your code here!


    programends()