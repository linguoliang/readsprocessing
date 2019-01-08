# coding=utf-8
"""
This modlue is for decoding  gtf file
modify for python3
modified in this file!
rename: isoverlab ->union, decodegff->decodegtf
2018-11-1
modified findgene functions
modification: abandon B_search function, it is not suitable for searching intervals or regions
2019-01-07
add gzip support
modfied findgenebyname and findgenebyId
"""
import sys
from functools import reduce
import copy
import gzip
import os.path

def file_extension(path):
    return os.path.splitext(path)[1]


genomeDict = {}

class GeneList:
    def __init__(self):
        self.genomeDict={}

def findgenebyname(string,chromosome=None): # 通过基因名寻找基因
    if chromosome==None:
        for listg in genomeDict.values():
            for gene in listg:
                if gene.genename == string:
                    return gene
    else:
        for gene in chromosome:
            assert isinstance(gene,GeneSubunit)
            if gene.genename == string:
                return gene
    return None

def findgenebyId(string,chromosome=None):
    if chromosome==None:
        for listg in genomeDict.values():
            for gene in listg:
                if gene.geneId == string:
                    return gene
    else:
        for gene in chromosome:
            assert isinstance(gene,GeneSubunit)
            if gene.geneId == string:
                return gene
    return None




def union(listone, listtwo):  #取并集
    if int(listone[-1]) < int(listtwo[0]) - 1:
        listone.extend(listtwo)
    elif int(listone[-1]) > int(listtwo[-1]):
        pass
    else:
        listone[-1] = listtwo[-1]

    return listone


class Isoform: # isoform 类
    def __init__(self, listitem):
        self.IsoformDict = {}  # isoform 字典
        self.IsoformDict[listitem[2]] = [listitem[3:5]] #注意string
        self.Introns = [] # int
        self.exonNum = 1

    def addmore(self, listitem):
        if listitem[2] in self.IsoformDict:
            self.IsoformDict[listitem[2]].append(listitem[3:5])
        else:
            self.IsoformDict[listitem[2]] = [listitem[3:5]]

    def builtIntron(self):
        # if self.IsoformDict.has_key("UTR"):
        #     self.Introns.extend(self.IsoformDict["UTR"])
        self.Introns.extend(copy.deepcopy(self.IsoformDict["exon"]))
        self.Introns.sort(key=lambda x: int(x[0]))

        self.Introns = reduce(union, self.Introns)
        self.Introns = [int(x) for x in self.Introns if True]
        #        self.Introns.insert(0, int(self.IsoformDict["transcript"][0][0]))
        self.Introns.insert(0, int(
            min(reduce(lambda x, y: [1000, min(int(x[0]), int(y[0]))], self.IsoformDict["transcript"]))))
        #        self.Introns.append(int(self.IsoformDict["transcript"][0][1]))
        self.Introns.append(
            int(max(reduce(lambda x, y: [0, max(int(x[1]), int(y[1]))], self.IsoformDict["transcript"]))))
        self.Introns = [[self.Introns[2 * i] + 1, self.Introns[2 * i + 1] - 1] for i in range(len(self.Introns) // 2)]
        self.Introns.pop()
        self.Introns.pop(0)

    def getexonNumber(self):
        if 'exon' in self.IsoformDict:
            self.exonNum = len(self.IsoformDict['exon'])
            return self.exonNum


class Gene:
    """
    用来存储基因的信息，包括基因名，scaffold,以及起始和终止位点
    """

    def __init__(self, listitems, genename, geneId):
        """
        init values
        """
        assert isinstance(listitems, list)
        assert isinstance(genename, str)
        self.scaffold = listitems[0]
        self.start = int(listitems[3])
        self.end = int(listitems[4])
        self.strand= listitems[6]
        self.genename =genename
        self.geneId = geneId


class GeneSubunit(Gene):
    """
    用来存储gene的亚结构，外显子，内含子，utr等结构
    """

    def __init__(self, listitems, genename, geneId):
        """
        init values
        Exon Intron
        """
        Gene.__init__(self, listitems, genename, geneId)
        self.Isoforms = []
        self.exon = []
        self.IsoformNum = 0
        self.superIsoform = []
        self.CommonIntrons = []
        self.maxExon = 1
        self.minExon = 10000
        self.extraExon = []
        self.junction={}

    def IsinCommonIntrons(self,Pos): #给出特定的位置，看位置是否位于共同的intron区域
        for x in self.CommonIntrons:
            if x[0]<=Pos <= x[1]:
                return True
        return False

    def AddextraExon(self, exon):
        self.extraExon.append(exon)

    def AddIsoform(self, listitem):
        self.IsoformNum = self.IsoformNum + 1
        self.Isoforms.append(Isoform(listitem))

    def Additems(self, listitem):
        self.Isoforms[-1].addmore(listitem)

    def builtsuperexon(self): #把所有的exon合并一起建立超级的exon
        for x in self.Isoforms:
            self.superIsoform.extend(copy.deepcopy(x.IsoformDict['exon']))
        self.superIsoform.sort(key=lambda x: int(x[0]))
        self.superIsoform = reduce(union, self.superIsoform)
        self.superIsoform = [int(x) for x in self.superIsoform if True]
        self.exon = [[self.superIsoform[2 * i], self.superIsoform[2 * i + 1]] for i in
                     range(len(self.superIsoform) // 2) if True]

    def builtsuperIsoform(self): #建立超级的

        """
        构建出CommonIntrons
        """
        superIsoform = []
        for x in self.Isoforms:
            assert isinstance(x, Isoform)
            x.getexonNumber()
            self.maxExon = max(self.maxExon, x.exonNum)
            self.minExon = min(self.minExon, x.exonNum)
            # if x.IsoformDict.has_key('UTR'):
            #     self.superIsoform.extend(x.IsoformDict["UTR"])
            superIsoform.extend(copy.deepcopy(x.IsoformDict['exon']))
        if self.extraExon != []:
            superIsoform.extend(copy.deepcopy(self.extraExon))
        superIsoform.sort(key=lambda x: int(x[0]))
        # superIsoform = map(lambda x: x[0:2], superIsoform)
        superIsoform = reduce(union, superIsoform)
        superIsoform = [int(x) for x in superIsoform if True]
        superIsoform.insert(0, self.start)
        superIsoform.append(self.end)
        self.CommonIntrons = [[superIsoform[2 * i] + 1, superIsoform[2 * i + 1] - 1] for i in
                              range(len(superIsoform) // 2) if True]
        self.CommonIntrons.pop()
        self.CommonIntrons.pop(0)

    def buildjunctions(self):  #获得以内含子为
        for isoform in self.Isoforms:
            # assert isinstance(isoform,Isoform)
            for junc in isoform.Introns:
                tmpj=",".join(junc)
                if tmpj  in self.junction:
                    pass
                else:
                    self.junction=None



global genesubunitqueue, genesubunitqueuepoplist

genesubunitqueue = [GeneSubunit(['linfake', 'linfake', 'gene', '-2', '-1','.','.'], 'NULL', 'NULL')]  # 有交集的基因队列
genesubunitqueuepoplist = []


def B_Search(pos: int, scaffold: str) -> int:  # 二分搜索法
    start, end = 0, len(genomeDict[scaffold])
    cursor = (start + end) // 2
    while start != cursor:
        if genomeDict[scaffold][cursor].start > pos:
            end = cursor
        else:
            start = cursor
        cursor = (start + end) // 2
    return cursor


def IsCoverIntron(star, end, gene): # for pattern detect
    assert isinstance(gene, GeneSubunit)
    for isoform in gene.Isoforms:
        for Intron in isoform.Introns:
            if star <= Intron[0] <= Intron[1] <= end:
                return True
    return False


def IsoverIntron(start, end, gene): # for pattern detect
    assert isinstance(gene, GeneSubunit)
    for Intron in gene.CommonIntrons:
        if not (end <= Intron[0] or Intron[1] <= start):
            return True
    return False


def GffPatternDet(start, end, gene): # for full length
    """
    IsOver的值为0 表示没有覆盖整个Intron,1表示有Intron,2表示覆盖一个全长的Intron,3表示覆盖全场
    """
    assert isinstance(gene, GeneSubunit)
    IsContinue = False
    IsOver = 0
    Overlab = False
    if end >= gene.end:
        IsContinue = True
        if start >= gene.end:  # gs<=ge<=as<=ae
            pass
        elif gene.start <= start < gene.end:  # gs<=as<=ge<=ae
            Overlab = True
            if IsoverIntron(start, end, gene):
                if IsCoverIntron(start, end, gene):
                    IsOver = 2
                else:
                    IsOver = 1
        else:  # as<=gs<=ge<=ae
            Overlab = True
            IsOver = 3
    elif end <= gene.start:  # as<=ae<=gs<=ge
        pass
    elif start <= gene.start:  # as<=gs<=ae<=ge
        Overlab = True
        if IsoverIntron(start, end, gene):
            if IsCoverIntron(start, end, gene):
                IsOver = 2
            else:
                IsOver = 1
    else:  # gs<=as<=ae<=ge
        Overlab = True
        if IsoverIntron(start, end, gene):
            if IsCoverIntron(start, end, gene):
                IsOver = 2
            else:
                IsOver = 1
    return IsContinue, Overlab, IsOver


# 如果是返回
def IsFullLength(scaffold, start, end, part=False):
    genelist = []
    fulllen = []
    IsContinue = True
    if scaffold in genomeDict:
        lens = len(genomeDict[scaffold])
        idx = B_Search(start, scaffold)
        while IsContinue and idx < lens:
            IsContinue, IsOverlap, IsOverAll = GffPatternDet(start, end, genomeDict[scaffold][idx])
            if IsOverlap:
                genelist.append(genomeDict[scaffold][idx].genename)
                fulllen.append(IsOverAll)
            idx += 1
        if len(genelist) == 0:
            genelist.append("intergenic")
            fulllen.append(0)
        return genelist, fulllen
    else:
        print("%s scaffold information not in Gff file!", scaffold)
        return None, None


def Creategene(listitems): # 创建基因实例 in decodegtf
    tmp = listitems[8].split(';')
    genename = tmp[2].split(' ')[2].replace('"', '')
    geneId = tmp[0].split(' ')[1].replace('"', '')
    return GeneSubunit(listitems[0:7], genename, geneId)


def builtoverlabexon(genesubunitqueue, tmpgene):
    for i in range(len(genesubunitqueue)):
        if genesubunitqueue[i].end < tmpgene.start:
            genesubunitqueuepoplist.append(i)
        else:
            for exon in genesubunitqueue[i].exon:  # 其他基因
                if tmpgene.start <= exon[0] <= exon[1] <= tmpgene.end or exon[0] <= tmpgene.start <= tmpgene.end <= \
                        exon[1]:
                    tmpgene.extraExon.append(exon)
                elif exon[0] <= tmpgene.start <= exon[1] <= tmpgene.end:
                    tmpgene.extraExon.append([tmpgene.start, exon[1]])
                elif tmpgene.start <= exon[0] <= tmpgene.end <= exon[1]:
                    tmpgene.extraExon.append([exon[0], tmpgene.end])
            for exon in tmpgene.exon:  # 其他基因
                if genesubunitqueue[i].start <= exon[0] <= exon[1] <= genesubunitqueue[i].end or exon[0] <= \
                        genesubunitqueue[i].start <= genesubunitqueue[i].end <= exon[1]:
                    genesubunitqueue[i].extraExon.append(exon)
                elif exon[0] <= genesubunitqueue[i].start <= exon[1] <= genesubunitqueue[i].end:
                    genesubunitqueue[i].extraExon.append([genesubunitqueue[i].start, exon[1]])
                elif genesubunitqueue[i].start <= exon[0] <= genesubunitqueue[i].end <= exon[1]:
                    genesubunitqueue[i].extraExon.append([exon[0], genesubunitqueue[i].end])


def decodegtf(gtffilename):
    global genesubunitqueue, genesubunitqueuepoplist
    """
    根据GFF文件创建gene Isoform
    :rtype: str
    """
    # add gzip support
    if file_extension(gtffilename)==".gz":
        # print('1')
        linopen=gzip.open
    else:
        # print("2")
        linopen=open
    with linopen(gtffilename,'rt') as gtffile:
        tmpgene = None
        for item in gtffile:
            if item.find("#") != 0:
                listitems = item.split("\t")
                # classifyitems(listitems)
                if listitems[2] == 'gene':
                    tmpgene = Creategene(listitems)
                break

        for item in gtffile:
            listitems = item.split("\t")
            # classifyitems(listitems)
            if listitems[2] == 'gene':
                tmpgene.builtsuperexon()
                if tmpgene.IsoformNum > 0:
                    tmpgene.Isoforms[-1].builtIntron()
                if genesubunitqueue[-1].scaffold == tmpgene.scaffold:
                    builtoverlabexon(genesubunitqueue, tmpgene)
                    while genesubunitqueuepoplist:
                        inputgene = genesubunitqueue.pop(genesubunitqueuepoplist.pop())
                        if inputgene != None and (inputgene.scaffold in genomeDict):
                            inputgene.builtsuperIsoform()
                            genomeDict[inputgene.scaffold].append(inputgene)
                        elif inputgene != None:
                            inputgene.builtsuperIsoform()
                            genomeDict[inputgene.scaffold] = [inputgene]
                    genesubunitqueue.append(tmpgene)
                else:
                    inputgene = genesubunitqueue.pop()
                    while genesubunitqueue:
                        # inputgene=genesubunitqueue.pop()
                        builtoverlabexon(genesubunitqueue, inputgene)
                        if inputgene != None and (inputgene.scaffold in genomeDict):
                            inputgene.builtsuperIsoform()
                            genomeDict[inputgene.scaffold].append(inputgene)
                        elif inputgene != None:
                            inputgene.builtsuperIsoform()
                            genomeDict[inputgene.scaffold] = [inputgene]
                        inputgene = genesubunitqueue.pop()
                    genesubunitqueue = [tmpgene]
                tmpgene = Creategene(listitems)
            elif listitems[2] == 'transcript':
                if tmpgene.IsoformNum > 0:
                    tmpgene.Isoforms[-1].builtIntron()
                tmpgene.AddIsoform(listitems)
            else:
                tmpgene.Additems(listitems)
    for key, val in genomeDict.items():
        assert isinstance(val, list)
        val.sort(key=lambda x: x.start)  # 按照起始位点排序

def classfynormaljunction(start,end,scaffold):
    """
    This function is to identify the normal junctions.and reture the results: three parameters
     one is for how many gene does the junction span,one is for is this junction a canonical one or non-canonical and

    :param start: int
    :param end: int
    :param scaffold: str
    :return: far from several gene,is in gtf file?
    """
    startr=findgene(start,scaffold)
    endr=findgene(end,scaffold)
    if endr[0]<=startr[1]:
        sidx=endr[0]
        eidx=startr[1]
        junction=1
        for x in range(sidx,eidx+1):
            for Isoform in genomeDict[scaffold][x].Isoforms:
                for junctions in Isoform.Introns:
                    if abs(start-junctions[0])<=1 and abs(end-junctions[1])<=1:
                        junction=2
                        break
                break
        return 0,junction
    else:
        sidx=startr[1]
        eidx=endr[0]
        junction=0
        return abs(eidx-sidx),junction

def findgene(Pos,scaffold):
    """
    该函数用于查找
    :param Pos:
    :param scaffold:
    :return:
    """
    listindex=[]
    long=len(genomeDict[scaffold])
    for index in range(long):
        gene=genomeDict[scaffold][index]
        assert isinstance(gene,GeneSubunit)
        if gene.start<=Pos:
            if gene.end>=Pos:
                listindex.append(index)
        else:
            break
    # idx=B_Search(Pos,scaffold)
    # ranges=len(genomeDict[scaffold])
    # idxs=idx-1
    # idxe=idx
    # while True:
    #     if idxs>=0 and genomeDict[scaffold][idxs].end>=Pos:
    #         idxs=idxs-1
    #     else:
    #         idxs=idxs+1
    #         break
    # while True:
    #     if idxe<ranges and genomeDict[scaffold][idxe].start<=Pos :
    #         idxe=idxe+1
    #     else:
    #         idxe=idxe
    #         break
    return listindex

def main():
    print("This is a Test!")


if __name__ == '__main__':
    sys.exit(main())
