#!/usr/bin/env python3
# coding=utf-8
import optparse
import time
import numpy as np
import os
import math
from scipy import sparse

__author__ = 'Guoliang Lin'
Softwarename = 'gethicdatatonpy'
version = '0.0.1'
bugfixs = ''
__date__ = '2018/11/22'


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
    parser.add_option('-j',
                      '--hic', dest='hic', type='string',
                      help='.hic file!')
    parser.add_option('-b',
                      '--binsize', dest='binsize', type='int',default=100000,
                      help='bin size')
    #    parser.add_option('-f','--fpkm',dest='fpkm_file',type='string',help='input fpkm file')
    #    parser.add_option('-v','--variation', dest='variation', type='string', help='input variation information file')
    #    parser.add_option('-g', '--gff3', dest='gff', help='gff3 file')
    parser.add_option('-o', '--output', dest='output', type='string', help='output file')
    options, args = parser.parse_args()
    # positional arguments are ignored
    return options


# define your functions here!


# define your functions here!
chromosomeDict={}
chromosomeMaxtrix={}
list_row_data=[]


if __name__ == '__main__':
    printinformations()
    options = _parse_args()
    # your code here!
    binsize=options.binsize
    with open(options.input) as infile:
        for item in infile:
            item=item.strip()
            chrom,size=item.split('\t')
            chrom=chrom.replace("chr",'')
            chromosomeDict[chrom]=int(size)
            chromosomeMaxtrix[chrom]=math.ceil(int(size)/binsize)
    prechromosomes=[]
    for i in chromosomeDict:
        for j in chromosomeDict:
            os.system('straw VC {2} {0} {1} BP {3} > {0}_{1}.txt'.format(i,j,options.hic,binsize))
            data=np.zeros((chromosomeMaxtrix[i],chromosomeMaxtrix[j]))
            # print(data.shape)
            with open('{0}_{1}.txt'.format(i,j)) as datafile:
                for item in datafile:
                    item=item.strip()
                    itemlist=item.split('\t')
                    if i==j:
                        data[int(itemlist[0])//binsize,int(itemlist[1])//binsize]=float(itemlist[2])
                        data[int(itemlist[1])//binsize,int(itemlist[0])//binsize]=float(itemlist[2])
                    elif j in prechromosomes:
                        data[int(itemlist[1])//binsize,int(itemlist[0])//binsize]=float(itemlist[2])
                    else:
                        data[int(itemlist[0])//binsize,int(itemlist[1])//binsize]=float(itemlist[2])
            sparse_data=sparse.bsr_matrix(data)
            sparse.save_npz('{0}_{1}.npz'.format(i,j),sparse_data)
            # np.save('{0}_{1}.npy'.format(i,j),data)
            # if j==1:
            #     list_row_data.append(data)
            # else:
            #     list_row_data[i-1]=np.hstack((list_row_data[i-1],data))
        prechromosomes.append(i)
    # dataall=list_row_data[0]
    # for i in range(1,50):
    #     dataall=np.vstack((dataall,list_row_data[i]))
    # sns.heatmap(dataall,vmax=10000)
    # plt.show()
    # np.save("1M.npy",dataall)
    programends()