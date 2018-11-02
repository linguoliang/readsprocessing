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


# default parameters
SUBLEN = 5


# define your functions here!

class Read:
    def __init__(self, read: pysam.AlignedSegment, sublen=SUBLEN):
        self.qname = read.qname
        self.is_read1 = read.is_read1
        self.aln = [read]
        self.alnnum = 1
        self.quality = read.mapping_quality
        self.reference_start = read.reference_start
        self.rname = []
        self.mapregion = []
        self.sublen = sublen
        self.getmapresion(read)

    def addaln(self, alnments: pysam.AlignedSegment):
        if self.qname == alnments.qname and self.is_read1 == alnments.is_read1:
            self.aln.append(alnments)
            self.update()
            self.getmapresion(alnments)
        else:
            raise NameError("Not the same read!")

    def update(self):
        self.alnnum = len(self.aln)

    def addrname(self, rname):
        self.rname.append(rname)

    def getmapresion(self, read: pysam.AlignedSegment):
        if read.reference_start and read.reference_end:
            if read.reference_start + self.sublen <= read.reference_end - self.sublen:
                region = [read.reference_start + self.sublen, read.reference_end - self.sublen]
                self.mapregion.append(region)


class Pairendread:
    def __init__(self, read: pysam.libcalignedsegment.AlignedSegment, sublen=SUBLEN):
        self.qname = read.qname
        self.read1 = None
        self.read2 = None
        self.sublen = sublen
        if read.is_read1:
            self.read1 = Read(read, self.sublen)
        else:
            self.read2 = Read(read, self.sublen)

    def addread(self, read):
        if self.qname == read.qname:
            if read.is_read1:
                if self.read1 is not None:
                    self.read1.addaln(read)
                else:
                    self.read1 = Read(read, self.sublen)
            else:
                if self.read2 is not None:
                    self.read2.addaln(read)
                else:
                    self.read2 = Read(read, self.sublen)
        else:
            raise NameError("Different read name!")


class CCDSPairendread(Pairendread):
    def __init__(self, read: pysam.AlignedSegment, sublen=SUBLEN):
        Pairendread.__init__(self, read, sublen)
        self.isrecussive = False

    def addCCDS(self, readsccds: pysam.AlignedSegment):
        if not readsccds.is_unmapped:
            ccds_id = str(readsccds.reference_name).split("|")[0]
            if readsccds.is_read1:
                self.read1.addrname(ccds_id)
            else:
                self.read2.addrname(ccds_id)

def parsereadnamedict(samfile, sublen=SUBLEN) -> (dict, pysam.AlignmentHeader):
    ReadNameDict = {}
    samfile = pysam.AlignmentFile(samfile, 'r')
    for item in samfile:
        assert isinstance(item, pysam.AlignedSegment)
        if item.qname in ReadNameDict:
            ReadNameDict[item.qname].addread(item)
        else:
            ReadNameDict[item.qname] = CCDSPairendread(item, sublen)
    header = samfile.header
    samfile.close()
    return ReadNameDict, header


if __name__ == '__main__':
    printinformations()
    options = _parse_args()
    # your code here!

    programends()
