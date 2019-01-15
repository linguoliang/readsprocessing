#!/usr/bin/env python3
# coding=utf-8
import optparse
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


__author__ = 'Guoliang Lin'
Softwarename = 'heatmapforPromoter.py'
version = '0.0.1'
bugfixs = ''
__date__ = '2019/01/15'


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
    parser.add_option('-o', '--output', dest='output', type='string', help='output file')
    options, args = parser.parse_args()
    # positional arguments are ignored
    return options

RSdata=pd.read_excel("hg19genedata_final.xlsx")

# TAD=pd.read_csv("../GSE63525_GM12878_primary+replicate_Arrowhead_domainlist.txt",sep='\t')
datacategories=pd.Categorical(RSdata["chrom"])
# print(datacategories)
Alldata=pd.DataFrame()
for c in datacategories.categories:
    # CRSdata=RSdata[RSdata["chrom"]==c]
    # print(CRSdata)
    # CTAD=TAD[TAD["chr1"]==str(c)]
    # array=np.array(CTAD.loc[:,['x1',"y2"]])
    # TADbg=pd.read_csv("Chrom{}_TAD_dist.txt".format(c),sep='\t',index_col=0)
    df=pd.read_csv("chrom{}_RSdata_T.txt".format(c),sep='\t',index_col=0)
    if Alldata.empty:
        Alldata=df
    else:
        Alldata=pd.merge(Alldata,df,right_index=True,left_index=True)
RSdata=RSdata.sort_values(('Glen'),ascending=False)
# RSdata=RSdata[RSdata["cat"]!=2]
# print(RSdata["pattern"])
# heatmaps=
# RSdata['chain']=RSdata["accepter"]<RSdata['donor']
bins=20
index=4
Rarray=None
distributiond=None
for x in RSdata.values:
    tmparray=np.array([Alldata[x[2]]])
    if x[13]=='-':
        tmparray=tmparray[:,::-1]
    if distributiond==None:
        if abs(x[index]-x[14])//1000+bins<1000:
            distributiond=tmparray[:,abs(x[index]-x[14])//1000-bins+1000:abs(x[index]-x[14])//1000+bins+1000]
    else:
        if abs(x[index]-x[14])//1000+bins<1000:
            tmpd=tmparray[:,abs(x[index]-x[14])//1000-bins+1000:abs(x[index]-x[14])//1000+bins+1000]
            distributiond=np.concatenate((distributiond,tmpd),axis=0)

    if Rarray==None:
        Rarray=tmparray
    else:
        Rarray=np.concatenate((Rarray,tmparray),axis=0)

Randoms=None
for x in RSdata.values:
    tmparray=np.array([Alldata[x[2]]])
    if x[13]=='-':
        tmparray=tmparray[:,::-1]
    if Randoms==None:
        rand=np.random.randint(min(bins,abs(x[4]-x[14])//1000),max(bins,abs(x[4]-x[14])//1000))
        if rand+bins<1000:
            Randoms=tmparray[:,rand-bins+1000:rand+bins+1000]
        for ij in range(49):
            rand=np.random.randint(min(bins,abs(x[4]-x[14])//1000),max(bins,abs(x[4]-x[14])//1000))
            if rand+bins<1000:
                tmpd=tmparray[:,rand-bins+1000:rand+bins+1000]
                Randoms=np.concatenate((Randoms,tmpd),axis=0)
    else:
        for ij in range(50):
            rand=np.random.randint(min(bins,abs(x[4]-x[14])//1000),max(bins,abs(x[4]-x[14])//1000))
            if rand+bins<1000:
                tmpd=tmparray[:,rand-bins+1000:rand+bins+1000]
                Randoms=np.concatenate((Randoms,tmpd),axis=0)



Rarray=Rarray[:,1000:2000]

print(distributiond.mean(axis=0))
plt.plot(range(-bins,bins),distributiond.mean(axis=0),color='r',label='acceptor')
plt.plot(range(-bins,bins),Randoms.mean(axis=0),color='g',label='background')
plt.xlabel('acceptor')
plt.ylabel("Interactions frequency obs/exp")
plt.legend(loc='upper right', shadow=True, fontsize='x-large')


# distributiond=Rarray[:]
# print(Rarray.shape)
# print(Alldata)
# Rarray=np.log10(Rarray+0.01)
# # print(Rarray)
# m=sns.light_palette('red',as_cmap=True)
#
# fig=sns.heatmap(Rarray,vmin=-1,vmax=1,cmap="RdBu_r")
# j=0
# for i in RSdata.values:
#     plt.axhline(y=j+0.3,color='#0077b4',xmin=0,xmax=min(1,(i[-4]/(1000))/1000))
#     plt.axhline(y=j,color='#00ff58',xmin=0,xmax=min(1,(i[-3]/(1000))/1000))
#     plt.axhline(y=j+0.7,color='#0000ff',xmin=0,xmax=min(1,(i[-5]/(1000))/1000))
#     j=j+1
plt.show()