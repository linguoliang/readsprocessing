#!/usr/bin/env python3
# coding=utf-8
import optparse
import time
import os
import math

__author__ = 'Guoliang Lin'
Softwarename = 'gethicmatrix'
version = '0.0.1'
bugfixs = ''
__date__ = '2019/11/15'


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
celllines=["HUVEC","NHEK","HMEC","IMR90","K562"]
hicdataprefix="GSE63525_{0}_combined.hic"

if __name__ == '__main__':
    printinformations()
    options = _parse_args()
    # your code here!
    binsize=options.binsize
    with open("/home/luoj/software/juicer/PBS/references/hg19.chrom.sizes") as infile:
        for item in infile:
            item=item.strip()
            chrom,size=item.split('\t')
            chrom=chrom.replace("chr",'')
            chromosomeDict[chrom]=int(size)
            chromosomeMaxtrix[chrom]=math.ceil(int(size)/binsize)
    prechromosomes=[]
    for cellline in celllines:
        for i in chromosomeDict:
            j=i
            print("Processing {2}:{0}_{1}".format(i,j,cellline))
            os.system('java -jar /home/luoj/data/juicer_tools.1.8.9_jcuda.0.8.jar dump oe VC {2} {1} {1} BP {3} > {0}_{1}_{3}.txt'.format(cellline,i,hicdataprefix.format(cellline),binsize))
    programends()