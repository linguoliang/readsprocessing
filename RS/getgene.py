#!/usr/bin/env python3
# coding=utf-8
import optparse
import time
import interval
import GTF_decoding
import pandas as pd


'''
for recursive splicing 
'''
__author__ = 'Guoliang Lin'
Softwarename = 'getannontations'
version = '0.0.1'
bugfixs = ''
__date__ = '18-11-1'


def printinformations():
    print("%s software version is %s in %s" % (Softwarename, version, __date__))
    print(bugfixs)
    print('Starts at :' + time.strftime('%Y-%m-%d %H:%M:%S'))


def programends():
    print('Ends at :' + time.strftime('%Y-%m-%d %H:%M:%S'))


# add your options here! 
def _parse_args():
    """Parse the command line for options."""
    usage = 'usage: %prog -i INPUT -g GTF -o OUTPUT'
    parser = optparse.OptionParser(usage)
    parser.add_option('-i',
                      '--input', dest='input', type='string',
                      help='input file!')
    #    parser.add_option('-f','--fpkm',dest='fpkm_file',type='string',help='input fpkm file')
    #    parser.add_option('-v','--variation', dest='variation', type='string', help='input variation information file')
    parser.add_option('-g', '--gtf', dest='gtf', help='gtf file')
    parser.add_option('-o', '--output', dest='output', type='string', help='output file')
    options, args = parser.parse_args()
    # positional arguments are ignored
    return options


# define your functions here!
# get data

if __name__ == '__main__':
    printinformations()
    options = _parse_args()
    # your code here!
    GTF_decoding.decodegtf("../Homo_sapiens.GRCh38.92.chr.gtf.gz")
    datalist =pd.read_excel("../hg19data.xlsx")
    liststart=[]
    listend=[]
    liststrand=[]
    listgeneid=[]
    for name in datalist["name"].values:
        print(name)
        gene=GTF_decoding.findgenebyname(name)
        if gene==None:
            liststart.append(0)
            listend.append(0)
            liststrand.append(0)
            listgeneid.append(0)
        else:
            liststart.append(gene.start)
            listend.append(gene.end)
            liststrand.append(gene.strand)
            listgeneid.append(gene.geneId)
    print(liststart)
    print(listend)
    print(liststrand)
    datalist["start"]=pd.Series(liststart)
    datalist['end']=pd.Series(listend)
    datalist["strand"]=pd.Series(liststrand)
    datalist["geneId"]=pd.Series(listgeneid)

    datalist.to_excel("hg19genedata_id.xlsx",index=False)

    programends()
