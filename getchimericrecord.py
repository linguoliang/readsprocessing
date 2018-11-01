#!/usr/bin/env python3
# coding=utf-8
import optparse
import time
import interval
import pysam

import CCDS
import Pairendreads

__author__ = 'Guoliang Lin'
Softwarename = 'getchimericrecord'
version = '0.0.1'
bugfixs = ''
__date__ = '18-7-19'


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
    parser.add_option('-r',
                      '--refaln', dest='refaln', type='string',
                      help='sam file that aligned to ref')
    parser.add_option('-c',
                      '--ccdsaln', dest='ccdsaln', type='string',
                      help='sam file that aligned to ccds')
    parser.add_option('-a',
                      '--ccdsanno', dest='ccdsanno', type='string',
                      help='ccds annotations')
    #    parser.add_option('-f','--fpkm',dest='fpkm_file',type='string',help='input fpkm file')
    #    parser.add_option('-v','--variation', dest='variation', type='string', help='input variation information file')
    #    parser.add_option('-g', '--gff3', dest='gff', help='gff3 file')
    parser.add_option('-o', '--output', dest='output', type='string', help='output file')
    options, args = parser.parse_args()
    # positional arguments are ignored
    return options


CCDSDict = {}
ReadNameDict = {}


# define your functions here!
def getchimericreadrecords(refaln, ccdsaln, ccdsanno, output):
    CCDSDict = CCDS.parseccdsdict(ccdsanno)
    ReadNameDict, header = Pairendreads.parsereadnamedict(refaln)
    samoutput = pysam.AlignmentFile(output, 'w', header=header)
    samfile = pysam.AlignmentFile(ccdsaln)
    for item in samfile:
        assert isinstance(item, pysam.AlignedSegment)
        if item.qname in ReadNameDict:
            ReadNameDict[item.qname].addCCDS(item)
    for qname in ReadNameDict:
        a = ReadNameDict[qname]
        assert isinstance(a, Pairendreads.CCDSPairendread)
        for ccds_id in a.read1.rname:
            if ccds_id in CCDSDict:
                b = CCDSDict[ccds_id]
                assert isinstance(b, CCDS.superCCDS)
                region = interval.interval(*b.exonlist)
                temp = []
                for mapregion in a.read1.mapregion:
                    temp.append(interval.interval(mapregion) in region)
                if len(temp) > sum(temp):
                    for read in a.read1.aln:
                        samoutput.write(read)
                    for read in a.read2.aln:
                        samoutput.write(read)
                    break
    samfile.close()
    samoutput.close()


if __name__ == '__main__':
    printinformations()
    options = _parse_args()
    # your code here!
    getchimericreadrecords(options.refaln, options.ccdsaln, options.ccdsanno, options.output)
    programends()
