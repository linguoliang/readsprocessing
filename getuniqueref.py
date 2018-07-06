#!/usr/bin/env python3
# coding=utf-8
import optparse
import time

from Bio import SeqIO

import CCDS

__author__ = 'Guoliang Lin'
Softwarename = 'getuniqueref'
version = '0.0.1'
bugfixs = ''
__date__ = '18-7-5'


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
    parser.add_option('-c', '--ccds', dest='ccds', type='string', help='CCDS annotation!')
    parser.add_option('-r', '--ref', dest='ref', type='string', help='whole genome reference!')
    parser.add_option('-a', '--anno', dest='anno', type='string', help='unique CCDS annotation output name!')
    #    parser.add_option('-f','--fpkm',dest='fpkm_file',type='string',help='input fpkm file')
    #    parser.add_option('-v','--variation', dest='variation', type='string', help='input variation information file')
    #    parser.add_option('-g', '--gff3', dest='gff', help='gff3 file')
    parser.add_option('-o', '--output', dest='output', type='string', help='CCDS ref output!')
    options, args = parser.parse_args()
    # positional arguments are ignored
    return options


# define your functions here!
ChromeDict = {}


def writeannotation(antationname, ccds=None):
    if ccds and len(ChromeDict) == 0:
        parsechromdict(ccds)
    with open(antationname, 'w') as annoutput:
        for chr in ChromeDict:
            for anno in ChromeDict[chr]:
                tempstr = str(ChromeDict[chr][anno])
                annoutput.write(tempstr + '\n')


def parsechromdict(ccds):
    with open(ccds) as inputfile:
        inputfile.readline()
        for item in inputfile:
            item = item.strip()
            itemlist = item.split('\t')
            if itemlist[5] == "Public":
                # tmepccds=CCDS.superCCDS(itemlist)
                if itemlist[0] in ChromeDict:
                    if itemlist[3] in ChromeDict[itemlist[0]]:
                        ChromeDict[itemlist[0]][itemlist[3]].addlist(itemlist)
                    else:
                        ChromeDict[itemlist[0]][itemlist[3]] = CCDS.superCCDS(itemlist)
                else:
                    ChromeDict[itemlist[0]] = {itemlist[3]: CCDS.superCCDS(itemlist)}


def getuniqueref(ccds: str, ref: str, output: str, anno: str = None):
    parsechromdict(ccds)
    iterator = SeqIO.parse(ref, 'fasta')
    with open(output, 'w') as outputfile:
        for seq in iterator:
            if seq.id in ChromeDict:
                temseq = seq[0:0]
                for gene_id in ChromeDict[seq.id]:
                    for resion in ChromeDict[seq.id][gene_id].exonlist:
                        temseq += seq[resion[0]-1:resion[1]]
                    temseq.id = "|".join([ChromeDict[seq.id][gene_id].ccds_id, ChromeDict[seq.id][gene_id].gene_id,
                                          ChromeDict[seq.id][gene_id].chromosome])
                    temseq.name = ""
                    temseq.description = ""
                    SeqIO.write(temseq, outputfile, 'fasta')
                    temseq = seq[0:0]
    if anno != None:
        writeannotation(anno)


if __name__ == '__main__':
    printinformations()
    options = _parse_args()
    # your code here!
    getuniqueref(options.ccds, options.ref, options.output, options.anno)
    programends()
