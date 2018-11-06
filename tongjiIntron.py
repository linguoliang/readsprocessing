#!/usr/bin/env python3
# coding=utf-8
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import stats
import GTF_decoding
__author__ = 'Guoliang Lin'
Softwarename = 'tongjiIntron'
version = '0.0.1'
bugfixs = ''
__date__ = '2018/11/2'
GTF_decoding.decodegtf("Homo_sapiens.GRCh38.92.chr.gtf")
Allintronlength=[]
Allintroninfo=[]
for chrosome in GTF_decoding.genomeDict:
    for gene in GTF_decoding.genomeDict[chrosome]:
        assert isinstance(gene,GTF_decoding.GeneSubunit)
        for intorn in gene.CommonIntrons:
            if intorn[1]-intorn[0] >0:
                Allintronlength.append(intorn[1]-intorn[0])
                Allintroninfo.append((intorn[1]-intorn[0],gene.genename))

Allintroninfo.sort(key=lambda x:x[0],reverse=True)
print(Allintroninfo[0:100])
datab=np.array(Allintronlength)
data=pd.read_csv("Introns.txt",header=None)
dataa=np.array(data)
# print(data[0])
# x=stats.ttest_ind(dataa,datab)
# print(x)
sns.distplot(datab, hist=False, color="r")
sns.distplot(data, hist=False, color="b")
# sns.distplot(data, kde=False, color="b")
plt.show()
print(stats.describe(dataa))
print("mdian is {}".format(np.median(dataa)))
print(stats.describe(datab))
print("mdian is {}".format(np.median(datab)))
