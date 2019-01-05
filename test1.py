
import pandas as pd
import numpy as np
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt

# means=np.load("chrom1_bkgd.npy")
start=5
end=0
x=np.arange(0,2000)
RSdata=pd.read_excel("data.xlsx")
TAD=pd.read_csv("GSE63525_GM12878_primary+replicate_Arrowhead_domainlist.txt",sep='\t')
datacategories=pd.Categorical(RSdata["chrom"])
for c in [2,3]:
    CRSdata=RSdata[RSdata["chrom"]==c]
    print(CRSdata)
    CTAD=TAD[TAD["chr1"]==str(c)]
    array=np.array(CTAD.loc[:,['x1',"y2"]])
    TADbg=pd.read_csv("Chrom{}_TAD_dist.txt".format(c),sep='\t',index_col=0)
    df=pd.read_csv("chrom{}_RSdata.txt".format(c),sep='\t',index_col=0)
    for pattern in CRSdata.values:
        print(pattern)
        print(array)
        TADS=array[(array[:,0]<pattern[3])&(array[:,1]>pattern[3])]
        for TAD in TADS:
            print("Hello")

            intron=df[pattern[2]]
            intronarr=np.array(intron)
            xa=(x-1000+pattern[3]//1000)*1000
            m=(pattern[4]-pattern[3])//(abs(pattern[4]-pattern[3]))
            end=(abs(pattern[4]-pattern[3])//1000)*3*m
            start=start*m
            if end<start:
                start,end=end,start
            TADbgforRS=TADbg[TADbg["TAD"]==str(TAD[0])+'_'+str(TAD[1])]
            # print(TADbg)
            plt.axes(xlim=(xa[1000+start]-3, xa[1000+end]+3),ylim=(0,max(intronarr[1000+start:1000+end])))
            sns.set(style="darkgrid")
            TADbgforRS["distance"]=(TADbgforRS["distance"]*m+pattern[3]//1000)*1000
            sns.lineplot(x="distance", y="values",data=TADbgforRS,color="r")
            # print(xa)
            plt.plot(xa[1000+start:1000+end],intronarr[1000+start:1000+end],color='g')
            # plt.plot(xa[start:100],means[5:100],color='r')
            plt.axvline(x=(pattern[4]//1000)*1000,linestyle=(0, (5, 10)),linewidth=1, color='b')

            plt.savefig('_'.join([str(pattern[0]),pattern[1],pattern[2]])+".pdf",format="pdf")
            plt.show()
            plt.clf()
        # plt.axvline(x=174193000,linewidth=1, color='b')
        #     plt.show()

# Load an example dataset with long-form data
# fmri = sns.load_dataset("fmri")

# Plot the responses for different events and regions




# import numpy as np
#
#
# def finddata(points, leftmargin, rightmargin, container, x1, x2, contact, long=1000, resolution=1000):
#     x1eq = (leftmargin[points == x1] <= x2) & (rightmargin[points == x1] > x2)
#     x2eq = (leftmargin[points == x2] <= x1) & (rightmargin[points == x2] > x1)
#     if len(x1eq) > 0 and x1eq[0]:
#         n1 = np.argwhere(points == x1)
#         container[(x2 - points[points == x1]) // resolution + long,n1] = contact
#     if len(x2eq) > 0 and x2eq[0]:
#         n2 = np.argwhere(points == x2)
#         container[ (x1 - points[points == x2]) // resolution + long,n2] = contact
#     return container
#
#
# points = np.array([12, 49, 57, 58, 59, 71])
# container = np.zeros((4,len(points)))
# # print(container)
# l = points - 2
# r = points + 2
# x1 = 59
# x2 = 58
# contact = 1.5
# container = finddata(points, l, r, container, x1, x2, contact, 2, 1)
# print(container)

# x={1:np.random.randint(10,50,49).tolist(),
#    2:np.random.randint(10,50,50).tolist(),
#    3:np.random.randint(10,50,50).tolist()}
# # m=[1,2,3]
# x[1].append(None)
#
# y=pd.DataFrame(x)
# mean=y.mean()
# std=y.std()
# stderr=std/np.sqrt(50)
# print(std)
# CI=stats.norm.interval(0.95,loc=mean,scale=std)
# print(CI)
# y[2][49]=None
# y[3][49]=None
# y=y.dropna()
# n = stats.describe(y[1])
# print(n)
# print(np.array(y.mean()))
# np.save("chrom1_bkgd.npy",y.mean())
# plt.plot(m,y.mean())
# plt.show()
# y=np.load("chrom1_bkgd.npy")
# print(means)
#
# for x in range(0,1):
#     print(x)

