#!/usr/bin/env python3
# coding=utf-8
import optparse
import time
import pysam

__author__ = 'Guoliang Lin'
Softwarename = 'getspecifiedregion'
version = '0.0.1'
bugfixs = ''
__date__ = '18-7-2'


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
def getspecifiedregion(Filename,chr,start,end):
    bamfile=pysam.AlignmentFile("SRR3192396_CCDS_ref_sort.bam", "rb")
    for read in bamfile.fetch('14', 54567612, 54793315):
        print(read)

if __name__ == '__main__':
    printinformations()
    options = _parse_args()
    # your code here!
    getspecifiedregion("","",23,76)
    programends()