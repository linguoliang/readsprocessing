#!/usr/bin/env python3
# coding=utf-8
import optparse
import time
import numpy as np
import matplotlib.pyplot as plt

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


# define your functions here!
def parserViewPoint(point,name,long=300,resolution=1000):
    point=(point//resolution)*resolution
    data=np.zeros(long)
    datax=np.arange(point,point+long*resolution,resolution)
    l=point-1
    r=point+long*resolution
    with open(name) as inputfile:
        for item in inputfile:
            item=item.strip().split('\t')
            x1=int(item[0])
            x2=int(item[1])
            concact=float(item[2])
            if x1==point:
                if l< x2 <r:
                    data[(x2-point)//resolution]=concact
            elif x2==point:
                if l< x1 <r:
                    data[(x1-point)//resolution]=concact
    print(data)
    plt.plot(datax,data)
    plt.show()


if __name__ == '__main__':
    printinformations()
    options = _parse_args()
    # your code here!
    parserViewPoint(174159657,"1_1.txt")
    programends()