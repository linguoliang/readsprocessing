#!/usr/bin/env python3
# coding=utf-8
import optparse
import time
import pysam

__author__ = 'Guoliang Lin'
Softwarename = 'Pairendreads'
version = '0.0.1'
bugfixs = ''
__date__ = '18-7-18'


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

class Read:
    def __init__(self,read:pysam.libcalignedsegment.AlignedSegment):
        self.qname=read.qname
        self.is_read1=read.is_read1
        self.aln=[read]




class Pairendread:
    def __init__(self,read1,read2):
        self.read1=read1
        self.read2=read2

if __name__ == '__main__':
    printinformations()
    options = _parse_args()
    # your code here!

    programends()