import pandas as pd
import numpy as np
x={"q":(1,2,3,4),"w":(5,5,7,7),'e':(9,10,11,12)}
x=pd.DataFrame(x)
m=pd.Categorical(x["w"])
for y in m.categories:
    print(y)
# m=x[(x["q"]>0) & (x["w"]<9)]
# print(m["q"]>2)
# y=pd.DataFrame({"q":[1],'w':[3],"e":[5]})
# print(y)
# m=m.append(y,ignore_index=True)
# m=m.loc[m["q"]>1,["q","w"]]
# print(m)
# for item in m.values:
#     print("hello")
# print(m.iloc[1,])
# data=pd.DataFrame({"chr":[],"TAD":[],"distance":[],"values":[]})
# print(data)
array=np.array(x.loc[:,['q','w']])
print(array[1:3,0])

x=(4-5)//abs(4-5)
print(x)
# array=array[(array[:,1]>5)&(array[:,0]>1)]
# print("1")
# for item in array:
#     print(item)
# TADinfo=pd.read_csv("GSE63525_GM12878_primary+replicate_Arrowhead_domainlist.txt",sep='\t')
# print(TADinfo)