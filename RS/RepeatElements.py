#!/usr/bin/env python3
# coding=utf-8
import optparse
import re
import time

import pandas as pd

"""

Description: 处理从 http://www.repeatmasker.org/species/hg.html 下载下来的 .out 文件，
目前只处理成 .bed 文件，后续会添加各种处理

"""
__author__ = 'Guoliang Lin'
Softwarename = 'RepeatElements'
version = '0.0.1'
bugfixs = ''
__date__ = '2019/6/14'


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
infile = "hg19.fa.out"
outfile = "Rep.bed"


def getRepdata(infile, outfile):
    getstring = lambda x: ((x == "+") and x) or "-"
    with open(infile) as inputfile:
        with open(outfile, 'w') as output:
            for item in inputfile:
                item = item.strip()
                itemlist = re.split(" +", item)
                beditem = [itemlist[4][3:], itemlist[5], itemlist[6], itemlist[9], "1000", getstring(itemlist[8]),
                           itemlist[10]]
                output.write("\t".join(beditem) + "\n")


def getElemnets(indata, outdata,pattern):
    data=pd.read_csv(indata,sep='\t',names=["chromosome",'start','end','description','score','strand','class'])
    datafilter=data['class'].str.contains(pattern,regex=True)
    data=data[datafilter]
    data.to_csv(outdata,sep='\t',index=False)

if __name__ == '__main__':
    printinformations()
    options = _parse_args()
    # your code here!
    getElemnets("Rep.bed",'LINE.bed','LINE')
    programends()
