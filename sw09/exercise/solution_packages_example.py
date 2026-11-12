import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("twitchdata-update.csv")

# create a new dataframe with only specific columns
column_selection = ['Channel', 'Watch time(Minutes)', 'Stream time(minutes)', 'Peak viewers', 'Average viewers', 'Followers', 'Language']

cdf = df[column_selection] # or
cdf = df.loc[:,column_selection]

# rename columns: replace spaces with underscores, remove brackets
newnames = []
for name in column_selection:
    newname = name.replace(" ", "_")
    newname = newname.split("(")[0]  # alternatively, you can also use regexp
    newnames.append(newname)

cdf.columns = newnames

# Use info() / describe() to figure out how many numeric columns you have and what the statistical distribution of the respective values roughly is
print(cdf.info())
print(cdf.describe())

# How many and which channels are above the 99 percentile in Watch time? Use the numpy function percentile and a selection mask to filter your dataframe.
percentile_value = np.percentile(cdf['Watch_time'], 99)
mask = cdf['Watch_time'] > percentile_value
res_df = cdf.loc[mask, "Channel"]


# What are the top 10 languages measured by combined peak viewers?
c_selection = ["Peak_viewers", "Language", "Watch_time", "Followers"]
gr = cdf[c_selection].groupby("Language").sum().sort_values("Peak_viewers", ascending=False)
head = gr.head(10)
print(head[['Peak_viewers']])

# Create a barplot with matplotlib showing this result

fig, ax = plt.subplots(2,1, figsize = (16,10))
ax[0].bar(gr.index, gr["Peak_viewers"])
ax[0].set_xlabel("Language")
ax[0].set_ylabel("Peak Viewers")
ax[0].set_title("Sum Peak Viewers by Language")

# rotate ONLY top subplot x-ticks
ax[0].tick_params(axis='x', rotation=45)

# Create a heatmap with seaborn for these 9 leading languages without English, compare sums of peak viewers, watch time and followers. Use min_max_normalization for each column to receive values between 0 and 1. What happens if you include English in this heat map?

head = head.iloc[1:]

min_max = (head - head.min()) / (head.max() - head.min()) # column wise min max normalization
ax[1] = sns.heatmap(min_max, cmap="inferno")
ax[1].set_title("Heatmap: Sum by Language (min max normalized, without English)")
plt.tight_layout()
plt.show()
