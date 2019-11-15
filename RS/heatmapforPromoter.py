#!/usr/bin/env python3
# coding=utf-8
import optparse
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math

__author__ = 'Guoliang Lin'
Softwarename = 'heatmapforPromoter.py'
version = '0.0.1'
bugfixs = ''
__date__ = '2019/01/06'


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

RSdata=pd.read_excel("hg19genedata_final.xlsx")

TAD=pd.read_csv("../GSE63525_GM12878_primary+replicate_Arrowhead_domainlist.txt",sep='\t')
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
# print(RSdata["pattern"])
# heatmaps=
# RSdata['chain']=RSdata["accepter"]<RSdata['donor']
Rarray=np.array([])
for x in RSdata.values:
    if len(Rarray)==0:
        tmparray=np.array([Alldata[x[2]]])
        if x[-4]=='-':
            tmparray=tmparray[:,::-1]
        Rarray=tmparray
        print(Rarray[:,::-1])
    else:
        # print(Rarray)
        tmparray=np.array([Alldata[x[2]]])
        if x[-4]=='-':
            tmparray=tmparray[:,::-1]
        Rarray=np.concatenate((Rarray,tmparray),axis=0)
Rarray=Rarray[:,1000:2000]
print(Rarray.shape)
# print(Alldata)
Rarray=np.log10(Rarray+0.01)
print(Rarray)
m=sns.light_palette('red',as_cmap=True)

fig=sns.heatmap(Rarray,vmin=-1,vmax=1,cmap="RdBu_r")
j=0
for i in RSdata.values:
    plt.axhline(y=j+0.3,color='#0077b4',xmin=0,xmax=min(1,(i[-4]/(1000))/1000))
    plt.axhline(y=j,color='#00ff58',xmin=0,xmax=min(1,(i[-3]/(1000))/1000))
    plt.axhline(y=j+0.7,color='#0000ff',xmin=0,xmax=min(1,(i[-5]/(1000))/1000))
    j=j+1
plt.show()

# for x in Alldata.axes[1].values:

#     for pattern in CRSdata.values:
#         print(pattern)
#         print(array)
#         TADS=array[(array[:,0]<pattern[3])&(array[:,1]>pattern[3])]
#         for TAD in TADS:
#             print("Hello")
#
#             intron=df[pattern[2]]
#             intronarr=np.array(intron)
#             xa=(x-1000+pattern[3]//1000)*1000
#             m=(pattern[4]-pattern[3])//(abs(pattern[4]-pattern[3]))
#             end=(abs(pattern[4]-pattern[3])//1000)*3*m
#             start=start*m
#             if end<start:
#                 start,end=end,start
#             TADbgforRS=TADbg[TADbg["TAD"]==str(TAD[0])+'_'+str(TAD[1])]
#             # print(TADbg)
#             plt.axes(xlim=(xa[1000+start]-3, xa[1000+end]+3),ylim=(0,max(intronarr[1000+start:1000+end])))
#             sns.set(style="darkgrid")
#             TADbgforRS["distance"]=(TADbgforRS["distance"]*m+pattern[3]//1000)*1000
#             sns.lineplot(x="distance", y="values",data=TADbgforRS,color="r")
#             # print(xa)
#             plt.plot(xa[1000+start:1000+end],intronarr[1000+start:1000+end],color='g')
#             # plt.plot(xa[start:100],means[5:100],color='r')
#             plt.axvline(x=(pattern[4]//1000)*1000,linestyle=(0, (5, 10)),linewidth=1, color='b')
#
#             plt.savefig('_'.join([str(pattern[0]),pattern[1],pattern[2]])+".pdf",format="pdf")
#             plt.show()
#             plt.clf()

# chromosomeDict={}
# chromosomeMaxtrix={}
# blocksize=np.zeros((50))
# growblocksize=np.zeros((50))
# ticks=np.zeros((50))
# keys=np.arange(1,51)
# with open("Carassius.auratus.build.company.chr.sizes") as infile:
#     for item in infile:
#         item=item.strip()
#         chrom,size=item.split('\t')
#         chrom=chrom.replace("chr",'')
#         chromosomeDict[int(chrom)]=int(size)
#         blocksize[int(chrom)-1]=math.ceil(int(size)/1000000)
# for i in keys:
#     growblocksize[i-1]=np.sum(blocksize[0:i])
#     if i>1:
#         ticks[i-1]=np.sum(blocksize[0:i-1])+blocksize[i-1]//2
#     else:
#         ticks[i-1]=blocksize[i-1]//2
#
# data=np.load("1M.npy")
# # data1=np.sqrt(data)
# m=sns.light_palette('red',as_cmap=True)
# fig=sns.heatmap(data,vmax=2000,cmap=m,cbar=False)
# cbar_kws={"shrink": 0.5}
# color="#777777"
# for m in growblocksize:
#     print(m)
#     plt.axhline(y=m,linewidth=.5, color=color)
#     plt.axvline(x=m,linewidth=.5, color=color)
# color1="#000000"
# plt.axhline(y=0,linewidth=2, color=color1)
# plt.axvline(x=0,linewidth=2, color=color1)
# plt.axhline(y=max(growblocksize),linewidth=2, color=color1)
# plt.axvline(x=max(growblocksize),linewidth=2, color=color1)
# plt.yticks(ticks,keys)
# plt.xticks(ticks,keys)
# plt.yticks([])
# plt.xticks([])
# plt.savefig("test_final.png",dpi=300,quality=95)
# # ax = plt.gca()
# # ax.spines['top'].set_visible(True)
# # ax.spines['bottom'].set_visible(True)
# # ax.spines['left'].set_visible(True)
# # ax.spines['right'].set_visible(True)
# plt.show()
#
#
# if __name__ == '__main__':
#     printinformations()
#     options = _parse_args()
#     # your code here!
#
#     programends()