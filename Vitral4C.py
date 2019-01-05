#!/usr/bin/env python3
# coding=utf-8
import optparse
import time
import numpy as np
import pandas as pd

__author__ = 'Guoliang Lin'
Softwarename = 'Vitral4C'
version = '0.0.1'
bugfixs = ''
__date__ = '2018/11/27'


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

# define your functions here!
def parserViewPoint(points:np.ndarray,name,long=1000,resolution=1000):
    points=np.array(points)
    points=(points//resolution)*resolution
    container=np.zeros((long*2,len(points)))
    # data=np.zeros(long)
    # datax=np.arange(points,points+long*resolution,resolution)
    # data={}
    # count=np.arange()
    # datax=range(0,long)
    # for i in datax:
    #     data[i]=[]
    l=points-long*resolution
    r=points+long*resolution
    with open(name) as inputfile:
        for item in inputfile:
            item=item.strip().split('\t')
            x1=int(item[0])
            x2=int(item[1])
            concact=float(item[2])
            # dist=(abs(x1-x2)//resolution)
            # if dist<long:
            #     data[dist].append(concact)
            container=finddata(points,l,r,container,x1,x2,concact,long,resolution)
    return container
    # print(data)
    # plt.plot(datax,data)
    # plt.show()
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
    # your code here!
    data=pd.read_excel("data.xlsx")
    datacategories=pd.Categorical(data["chrom"])
    for c in datacategories.categories:
        chrom1=data[data["chrom"]==c]
        container=parserViewPoint(np.array(chrom1["donor"]),"{0}_{0}.txt".format(c))
        datatostore=pd.DataFrame(container,columns=chrom1["pattern"])
        datatostore.to_csv("chrom{}_RSdata.txt".format(c),sep='\t')
    programends()