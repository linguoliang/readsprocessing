#!/usr/bin/env python3
# coding=utf-8
import optparse
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import chrom

__author__ = 'Guoliang Lin'
Softwarename = 'Vitral4C_background'
version = '0.0.1'
bugfixs = ''
__date__ = '2018/12/6'


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
    parser.add_option('-t', '--TAD', dest='TAD', type='string', help='TAD file')
    #    parser.add_option('-f','--fpkm',dest='fpkm_file',type='string',help='input fpkm file')
    #    parser.add_option('-v','--variation', dest='variation', type='string', help='input variation information file')
    #    parser.add_option('-g', '--gff3', dest='gff', help='gff3 file')
    parser.add_option('-o', '--output', dest='output', type='string', help='output file')
    options, args = parser.parse_args()
    # positional arguments are ignored
    return options


# define your functions here!
def finddata(points, leftmargin, rightmargin, container, x1, x2, contact, long=1000, resolution=1000):
    x1eq = (leftmargin[points == x1] <= x2) & (rightmargin[points == x1] > x2)
    x2eq = (leftmargin[points == x2] <= x1) & (rightmargin[points == x2] > x1)
    if len(x1eq) > 0 and x1eq[0]:
        n1 = np.argwhere(points == x1)
        container[(x2 - points[points == x1]) // resolution + long,n1] = contact
    if len(x2eq) > 0 and x2eq[0]:
        n2 = np.argwhere(points == x2)
        container[(x1 - points[points == x2]) // resolution + long,n2] = contact
    return container

def parserViewPoint(TADfile,chrom,name,long=1000,resolution=1000):
    data=pd.DataFrame({"chr":[],"TAD":[],"distance":[],"values":[]})
    TADinfo=pd.read_csv(TADfile,sep='\t')
    # TADinfo.values
    TADinfo=TADinfo.loc[TADinfo["chr1"]==chrom,["chr1",'x1','y2']]
    x1array=np.array(TADinfo['x1'])
    x2array=np.array(TADinfo['y2'])
    # datax=range(0,len(TADinfo))
    # for i in datax:
    #     data[i]=[]
    with open(name) as inputfile:
        for item in inputfile:
            item=item.strip().split('\t')
            x1=int(item[0])
            x2=int(item[1])
            if x1>x2:
                x1,x2=x2,x1
            concact=float(item[2])
            dist=abs(x1-x2)//resolution
            if dist<long:
                inTAD=TADinfo[(x1array<x1) & (x2array>x2)]
                # if len(inTAD)>0:
                #     print("haha")
                for tad in inTAD.values:
                    data.append(pd.DataFrame({"chr":[chrom],"TAD":[str(tad[1])+'_'+str(tad[2])],"distance":[dist],"values":[concact]}),ignore_index=True)
    data.to_csv('Chrom{}_TAD_distV1.txt'.format(chrom),sep="\t")

                # data[dist].append(concact)
    # maxlen=0
    # for i in datax:
    #     maxlen=max(maxlen,len(data[i]))
    # for i in datax:
    #     if len(data[i])<maxlen:
    #         for j in range(len(data[i]),maxlen):
    #             data[i].append(None)
    # df=pd.DataFrame(data)
    # means=df.mean()
    # std=df.std()
    # plt.plot(datax,means)
    # np.save("chrom1_bkgd.npy",means)



if __name__ == '__main__':
    printinformations()
    options = _parse_args()
    parserViewPoint("GSE63525_GM12878_primary+replicate_Arrowhead_domainlist.txt",chrom.Chromdict[0],"{0}_{0}.txt".format(chrom.Chromdict[0]))

    programends()