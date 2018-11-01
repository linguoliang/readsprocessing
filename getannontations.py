#!/usr/bin/env python3
# coding=utf-8
import optparse
import time

import interval

import GTF_decoding

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
def parsebeddata(bedfilename):
    datalist = []
    with open(bedfilename) as infile:
        with open(bedfilename + '_ID', 'w') as outfile:
            Id = 1
            for item in infile:
                itemlist = item.strip().split('\t')
                datalist.append((itemlist[0], int(itemlist[1]), int(itemlist[2]), str(Id)))
                outfile.write('\t'.join([str(Id), itemlist[0], itemlist[1], itemlist[2]])+'\n')
                Id += 1
    return datalist


if __name__ == '__main__':
    printinformations()
    options = _parse_args()
    # your code here!
    GTF_decoding.decodegtf("Homo_sapiens.GRCh38.92.chr.gtf")
    datalist = parsebeddata("finalcandidate.bed")
    with open("Intronlength.txt",'w') as Intronfile:
        with open("annotaions.bed",'w') as outputfile:
            geneidlist=[]
            for data in datalist:
                regionIndex = GTF_decoding.findgene(data[1], data[0])
                dataregion = interval.interval(data[1:3])
                if len(regionIndex)>0:
                    for x in regionIndex:
                        genesubunit = GTF_decoding.genomeDict[data[0]][x]
                        assert isinstance(genesubunit, GTF_decoding.GeneSubunit)
                        if dataregion in interval.interval([genesubunit.start, genesubunit.end]):
                            IntronFlag = False
                            for intron in range(len(genesubunit.CommonIntrons)):
                                if dataregion in interval.interval(genesubunit.CommonIntrons[intron]):
                                    IntronFlag = True
                                    Intronfile.write('\t'.join(
                                        [data[3], data[0], str(data[1]), str(data[2]), genesubunit.geneId,
                                         genesubunit.genename,
                                         str(intron + 1), str(genesubunit.CommonIntrons[intron]),
                                         str(genesubunit.CommonIntrons[intron][1] - genesubunit.CommonIntrons[intron][
                                             0])])+'\n')
                            if genesubunit.geneId not in geneidlist:
                                for exon in genesubunit.exon:
                                    outputfile.write('\t'.join([data[0], str(exon[0]), str(exon[1]), genesubunit.geneId,str(len(genesubunit.exon)),genesubunit.strand])+'\n')
                                    geneidlist.append(genesubunit.geneId)
    programends()
