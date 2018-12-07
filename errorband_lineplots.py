"""
Timeseries plot with error bands
================================

_thumb: .48, .45

"""
import seaborn as sns
import pandas as pd
import matplotlib.pylab as plt
df=pd.read_csv("Chrom1_TAD_dist.txt",sep='\t',index_col=0)
# df=df[df["TAD"]=="1710000_1840000"]
print(df)
sns.set(style="darkgrid")

# Load an example dataset with long-form data
# fmri = sns.load_dataset("fmri")

# Plot the responses for different events and regions
sns.lineplot(x="distance", y="values",
             data=df)

plt.show()
