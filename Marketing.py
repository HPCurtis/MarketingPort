# Import required python modules.
import stan as ps
import numpy as  np 
import pandas as  pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read in marketing Data.
df = pd.read_csv('http://goo.gl/PmPkaG')
print(df.columns)
print(df.dtypes)

# Convert email to categorical variable.
=
df["email"] = df["email"].astype("category")
print(df.dtypes)

#Plot data using scatter plot.
plt.scatter(df['store.spend'], df['online.spend'], c='black', alpha=.3)
plt.xlabel('Prior 12 months in−store sales ($)')
plt.ylabel('Prior 12 months online sales ($)')
#plt.show()


# Calculate the correlation between varaible in Dataset
cor_df = df.drop(['cust.id', 'email'], axis=1)

# Calculate parametric (Pearsons) and non-parametric (Spearmans) correlations
pearson = cor_df.corr('pearson')
spearman = cor_df.corr('spearman')

# Generate a mask for the upper triangle
maskP = np.triu(np.ones_like(pearson, dtype=bool))
maskS = np.triu(np.ones_like(spearman, dtype=bool))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(230, 20, as_cmap=True)

# Draw the heatmap for Pearson correlation results.
sns.heatmap(pearson, mask=maskP, cmap=cmap, vmax=1, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})


plt.show()

# Draw the heatmap for Spearman correlation results.
sns.heatmap(spearman, mask=maskS, cmap=cmap, vmax=1, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})

plt.show()