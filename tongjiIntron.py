#!/usr/bin/env python3
# coding=utf-8
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import stats
import GTF_decoding
from plotnine import *
__author__ = 'Guoliang Lin'
Softwarename = 'tongjiIntron'
version = '0.0.1'
bugfixs = ''
__date__ = '2018/11/2'
# GTF_decoding.decodegtf("Homo_sapiens.GRCh38.92.chr.gtf")
# Allintronlength=[]
# Allintroninfo=[]
# for chrosome in GTF_decoding.genomeDict:
#     for gene in GTF_decoding.genomeDict[chrosome]:
#         assert isinstance(gene,GTF_decoding.GeneSubunit)
#         for intorn in gene.CommonIntrons:
#             if intorn[1]-intorn[0] >0:
#                 Allintronlength.append(intorn[1]-intorn[0])
#                 Allintroninfo.append((intorn[1]-intorn[0],gene.genename))
#
# Allintroninfo.sort(key=lambda x:x[0],reverse=True)
# print(Allintroninfo[0:100])
# datab=np.array(Allintronlength)
data=pd.read_csv("forR.txt",sep='\t')
dataa=np.array(data)
# with open('forR.txt','w') as output:
#     for x in dataa:
#         output.write("RS_Intron\t{0}\n".format(x[0]))
#     for x in Allintronlength:
#         output.write("All_Intron\t{0}\n".format(x))
# print(data[0])
# x=stats.ttest_ind(dataa,datab)
print(data)
a=(ggplot(data,aes(x="length",colour="Name"))+ geom_density())
a.draw()
# sns.distplot(datab,bins=100, hist=False, color="r")
# sns.distplot(dataa,bins=100 ,hist=False, color="b")
# sns.distplot(data, kde=False, color="b")
# plt.hist(dataa,bins=100,color='b',density=True,histtype='step')
plt.show()
# print(stats.describe(dataa))
# print("mdian is {}".format(np.median(dataa)))
# print(stats.describe(datab))
# print("mdian is {}".format(np.median(datab)))
