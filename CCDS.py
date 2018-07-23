#!/usr/bin/env python3
# coding=utf-8
import interval

'''
解析CCDS注释文件，并构建超级CCDS
'''
__author__ = 'Guoliang Lin'
__date__ = '2018/7/04'


class CCDS:
    def __init__(self, listitems):
        assert isinstance(listitems, list)
        self.chromosome = listitems[0]
        self.nc_accession = listitems[1]
        self.gene = listitems[2]
        self.gene_id = listitems[3]
        self.ccds_id = listitems[4]
        self.ccds_status = listitems[5]
        self.cds_strand = listitems[6]
        self.cds_from = int(listitems[7])
        self.cds_to = int(listitems[8])
        self.cds_locations = listitems[9]
        self.match_type = listitems[10]
        self.exonlist = self.initexon()
        self.listall = listitems
        self.length = 0
        self.exonnumber = 0
        self.update()

    def initexon(self):
        exonlist = []
        assert isinstance(self.cds_locations, str)
        tmp = self.cds_locations.replace('[', '').replace(']', '').split(', ')
        for exon in tmp:
            exon = exon.split('-')
            exontuple = (int(exon[0]), int(exon[1]))
            exonlist.append(exontuple)
        return exonlist

    def __str__(self):
        return '\t'.join(self.listall)

    def update(self):
        '''
        update parameters
        :return:
        '''
        self.length = self.cds_to - self.cds_from + 1
        self.exonnumber = len(self.exonlist)
        self.listall = [self.chromosome, self.nc_accession, self.gene, self.gene_id, self.ccds_id, self.ccds_status,
                        self.cds_strand, str(self.cds_from), str(self.cds_to), self.cds_locations, self.match_type]


class superCCDS(CCDS):
    def __init__(self, listitems):
        CCDS.__init__(self, listitems)
        self.super_ccds_id = [self.ccds_id]

    def addccds(self, ccds: CCDS):
        tmpregion = interval.interval(*ccds.exonlist)
        region = interval.interval(*self.exonlist)
        region = region | tmpregion
        tmpexonlist = list(region)
        self.exonlist = [(int(x[0]), int(x[1])) for x in tmpexonlist]
        self.cds_from = min(self.cds_from, ccds.cds_from)
        self.cds_to = max(self.cds_to, ccds.cds_to)
        self.__construct_locations()
        self.super_ccds_id.append(ccds.ccds_id)
        self.update()

    def __construct_locations(self):
        self.cds_locations = "[" + ', '.join(['-'.join((str(x[0]), str(x[1]))) for x in self.exonlist]) + ']'

    def addlist(self, listitems):
        '''
        :param listitems: CCDS list
        :return:
        '''
        ccds = CCDS(listitems)
        self.addccds(ccds)


def parsechromdict(ccds):
    ChromeDict = {}
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
                        ChromeDict[itemlist[0]][itemlist[3]] = superCCDS(itemlist)
                else:
                    ChromeDict[itemlist[0]] = {itemlist[3]: superCCDS(itemlist)}
    return ChromeDict


def parseccdsdict(ccds):
    CCDSDict = {}
    ChromeDict = parsechromdict(ccds)
    for chrom in ChromeDict:
        for gene_id in ChromeDict[chrom]:
            for ccds_id in ChromeDict[chrom][gene_id].super_ccds_id:
                CCDSDict[ccds_id] = ChromeDict[chrom][gene_id]
    return CCDSDict
