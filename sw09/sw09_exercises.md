# SW09 · Exercise sheet: notebooks, numpy, pandas, matplotlib

**Sheet:** `exercises.pdf` ("Exercise Sheet SW9") · **Theory:** [SW09 notes](sw09_external_packages.md) · **Notebook:** [exercise/sw09_exercises.ipynb](exercise/sw09_exercises.ipynb)

Additional material: `airquality.csv` and `twitchdata-update.csv`, both in [`exercise/`](exercise/).

All solutions below were run on Python 3.13 with pandas 3.0.5, numpy 2.5.3. Solutions are collapsed, try the task first.

---

## Exercise 1: Jupyter / Marimo notebooks

Follow the instructions and explore jupyter / marimo notebook functionalities:

- Create a new jupyter/marimo notebook in PyCharm
- Import numpy and pandas and load the `airquality.csv` file into a dataframe
- Calculate various statistics (mean, etc.) of the temperature values. Report them as text in the jupyter notebook
- Find an outlier (one) and correct it by averaging the values before and after the outlier. Make a note to the report
- Plot the temperature series with matplotlib or seaborn and add it to the report
- Create a temperature converter function from °F to °C (formula: °F = °C × (9/5) + 32)
- Convert all temperature values from °F to °C using `map()`
- Plot both temperature graphs in one figure and add it to the report
- Declare a class `AirQualityReport` comprising object variables that store the mean values of columns where reasonable
- Add an object method to the class that calculates the max value of all object variables. The function should return a dictionary containing the original column name of the variable with the max value and the maximum value itself
- Export the report to an HTML and/or a PDF document
- Explore Pandas, Numpy and matplotlib and marimo functionalities in more detail

<details>
<summary>Solution</summary>

### Loading, and the row that is not data

```python
import numpy as np
import pandas as pd

df = pd.read_csv("airquality.csv")
print(df.shape)        # (154, 7)
```

The file ends with a line of bare commas, so pandas reads **154 rows** where the data has 153. The last one is all `NaN`:

```python
df = df.dropna(how="all")
print(df.shape)        # (153, 7)
```

`how="all"` drops only rows that are entirely empty. Plain `dropna()` would drop every row with *any* missing value, which here would throw away 42 rows, because `Ozone` and `Solar.R` have genuine gaps. This is R's classic `airquality` dataset and those `NA`s are part of it.

### Statistics

```python
t = df["Temp"]
print(f"mean   {t.mean():.3f}")
print(f"median {t.median()}")
print(f"std    {t.std():.3f}")
print(f"min    {t.min()}")
print(f"max    {t.max()}")
```

```
mean   76.124
median 79.0
std    25.228
min    -212.0
max    97.0
```

`df["Temp"].describe()` gives all of it in one call. Write the numbers into a markdown cell as the task asks for a report, not just output.

### The outlier

A standard deviation of 25 on a Fahrenheit temperature series is the giveaway, and the minimum says why:

```python
i = df["Temp"].idxmin()
print(df.loc[i])
```

```
rownames     25.0
Temp       -212.0
Month         5.0
Day          25.0
```

Row 25 reads **−212 °F**, which is below absolute zero (−459.67 °F) in no way but is clearly impossible for a weather station in New York in May. Correct it with the mean of its neighbours:

```python
before, after = df.loc[i - 1, "Temp"], df.loc[i + 1, "Temp"]
df.loc[i, "Temp"] = (before + after) / 2
```

Neighbours are 61 and 58, so the corrected value is **59.5**. Effect on the statistics:

| | before | after |
|---|---|---|
| mean | 76.124 | **77.899** |
| std | 25.228 | **9.49** |
| min | −212.0 | **56.0** |

One bad value out of 153 moved the mean by 1.8 °F and nearly tripled the standard deviation. That is the point of the exercise, so put it in the report.

Note `i` here is the **positional index 24**, not `rownames` 25, because pandas indexes from 0 while the CSV's own `rownames` column starts at 1. Using `df.loc[25]` would correct the wrong row.

### The converter, and the formula on the sheet

The sheet gives `°F = °C × (9/5) + 32` and then asks for a converter **from °F to °C**. That is the formula for the other direction, so solve it first:

```
°F = °C × 9/5 + 32
°C = (°F − 32) × 5/9
```

```python
def fahrenheit_to_celsius(f):
    return (f - 32) * 5 / 9
```

Check it on the two fixed points: 32 °F gives 0.0 and 212 °F gives 100.0. Applying the sheet's formula as written to 97 °F gives 206.6, which is obviously not a Celsius value. Same trap as the SW02 temperature exercise.

```python
df["Temp_C"] = df["Temp"].map(fahrenheit_to_celsius)
```

`Temp_C` then runs from 13.33 to 36.11 with a mean of 25.50, which are plausible summer temperatures.

`map()` is what the task asks for. `(df["Temp"] - 32) * 5 / 9` gives the same column without a function, because arithmetic on a Series is already element-wise.

### Both series in one figure

```python
import matplotlib.pyplot as plt

fig, axs = plt.subplots(1, 2, figsize=(12, 4))

axs[0].plot(df["Temp"].to_numpy())
axs[0].set_title("Temperature (°F)")
axs[0].set_xlabel("observation")
axs[0].set_ylabel("°F")

axs[1].plot(df["Temp_C"].to_numpy())
axs[1].set_title("Temperature (°C)")
axs[1].set_xlabel("observation")
axs[1].set_ylabel("°C")

plt.tight_layout()
plt.show()
```

Two panels side by side show the shape is identical and only the scale differs, which is the honest reading. Plotting both on **one** pair of axes also satisfies "both in one figure" and makes the point better, since the two lines then sit at visibly different heights. Either is defensible, say which you chose.

### The class

"Columns where reasonable" means the four measurements. A mean of `rownames`, `Month` or `Day` is meaningless.

```python
class AirQualityReport:
    def __init__(self, dataframe):
        self.ozone = dataframe["Ozone"].mean()
        self.solar = dataframe["Solar.R"].mean()
        self.wind = dataframe["Wind"].mean()
        self.temp = dataframe["Temp"].mean()

    def max_value(self):
        values = {"Ozone": self.ozone, "Solar.R": self.solar,
                  "Wind": self.wind, "Temp": self.temp}
        name = max(values, key=values.get)
        return {name: values[name]}
```

```python
report = AirQualityReport(df)
report.max_value()        # {'Solar.R': 185.93150684931507}
```

means: Ozone 42.129, Solar.R 185.932, Wind 9.958, Temp 77.899.

**The dictionary inside `max_value` is what makes the task work.** The requirement is to return "the original column name of the variable with the max value", but the object variables are called `self.solar` while the column is called `Solar.R`. The attribute name does not carry the column name, so the mapping has to be written down somewhere. Holding it in a dictionary is the straightforward way.

`max(values, key=values.get)` returns the **key** with the largest value, not the value itself. Without `key=` you would get the alphabetically largest key name.

Worth noting the answer is meaningless as a comparison: solar radiation in langleys wins over temperature in °F because the units are unrelated, not because it is "bigger". The task asks for the mechanic, so deliver it, and say in the report that comparing across units has no physical meaning. Min-max normalising first, as in [Exercise 2c](#part-c), is what would make it comparable.

### Export

```bash
jupyter nbconvert --to html --no-input sw09_exercises.ipynb
```

Two hyphens before `to` and `no-input`. The slide prints em dashes, which fail. `--no-input` hides the code and keeps the markdown and the outputs, which is what makes it read as a report. PDF export additionally needs LaTeX, so HTML is the easier route.

</details>

## Exercise 2: Numpy, Pandas and Matplotlib

Analyse the twitch data using pandas, numpy and matplotlib.

### Part a)

- Read the twitch data into a dataframe, display the columns with `df.columns`
- Create a new dataframe only containing the columns `column_selection` (below)
- Rename columns: replace spaces with underscores, remove brackets including their contents
- Use `info()` and `describe()` to figure out how many numeric columns you have and what the statistical distributions of the respective values roughly are

```python
column_selection = ['Channel', 'Watch time(Minutes)', 'Peak viewers', 'Language']

df = df[column_selection]       # selection of particular columns by list
df.columns = newnames           # rename all columns
```

<details>
<summary>Solution</summary>

```python
import re
import numpy as np
import pandas as pd

df_full = pd.read_csv("twitchdata-update.csv")
print(df_full.columns)
```

```
['Channel', 'Watch time(Minutes)', 'Stream time(minutes)', 'Peak viewers',
 'Average viewers', 'Followers', 'Followers gained', 'Views gained',
 'Partnered', 'Mature', 'Language']
```

1000 rows, 11 columns.

```python
column_selection = ['Channel', 'Watch time(Minutes)', 'Peak viewers', 'Language']
df = df_full[column_selection].copy()

newnames = [re.sub(r"\(.*?\)", "", c).strip().replace(" ", "_") for c in df.columns]
df.columns = newnames
# ['Channel', 'Watch_time', 'Peak_viewers', 'Language']
```

`re.sub(r"\(.*?\)", "", c)` removes the bracket and its contents. `.strip()` cleans up any space that is left behind, and only then are the remaining spaces turned into underscores. Doing it in the other order works for these four names too, but leaves `Watch_time(Minutes)` as an intermediate, which is harder to read.

The `.copy()` matters. `df_full[column_selection]` can be a view, and assigning to `df.columns` afterwards may raise a `SettingWithCopyWarning`. Copy when you intend the new frame to be its own thing.

```python
df.info()
df.describe()
```

```
 #   Column        Non-Null Count  Dtype
 0   Channel       1000 non-null   str
 1   Watch_time    1000 non-null   int64
 2   Peak_viewers  1000 non-null   int64
 3   Language      1000 non-null   str
```

**Two numeric columns**, `Watch_time` and `Peak_viewers`. No missing values anywhere.

```
         Watch_time    Peak_viewers
count  1.000000e+03     1000.000000
mean   4.184279e+08    37065.051000
std    5.496355e+08    60314.307686
min    1.221928e+08      496.000000
25%    1.631899e+08     9113.750000
50%    2.349908e+08    16676.000000
75%    4.337399e+08    37569.750000
max    6.196162e+09   639375.000000
```

Both distributions are heavily **right-skewed**: the mean sits well above the median and the maximum is roughly 26 times the median for `Watch_time` and 38 times for `Peak_viewers`. A handful of enormous channels drag the average up, which is exactly why part b) asks about the 99th percentile rather than the mean.

</details>

### Part b)

Answer the following questions:

- How many and which channels are above the 99 percentile of `Watch_time`?
- What are the top 10 languages measured by sum of all `Peak_viewers` in that language?

```python
value = np.percentile(data, 95)       # numpy provides a percentile function
mask = df['Watch_time'] > your_value  # masks are created by boolean expressions
res_df = df.loc[mask, "MyColumn"]     # masks select parts of dataframes
gr = df.groupby('label')              # group by column values
gr = df.groupby('label').sum()        # aggregation directly on the groupby result
```

<details>
<summary>Solution</summary>

**Channels above the 99th percentile of Watch_time**

```python
p99 = np.percentile(df["Watch_time"], 99)
mask = df["Watch_time"] > p99
print(p99, mask.sum())
print(df.loc[mask, ["Channel", "Watch_time"]])
```

99th percentile = **2,834,746,919.25**, and **10 channels** are above it:

| Channel | Watch_time |
|---|---|
| xQcOW | 6,196,161,750 |
| summit1g | 6,091,677,300 |
| Gaules | 5,644,590,915 |
| ESL_CSGO | 3,970,318,140 |
| Tfue | 3,671,000,070 |
| Asmongold | 3,668,799,075 |
| NICKMERCS | 3,360,675,195 |
| Fextralife | 3,301,867,485 |
| loltyler1 | 2,928,356,940 |
| Anomaly | 2,865,429,915 |

10 out of 1000 is exactly what "above the 99th percentile" should give, which is a useful sanity check on the mask.

**Top 10 languages by sum of Peak_viewers**

```python
top10 = df.groupby("Language")["Peak_viewers"].sum().sort_values(ascending=False).head(10)
```

| Language | Peak_viewers |
|---|---|
| English | 20,195,264 |
| Spanish | 3,616,715 |
| Russian | 3,277,461 |
| Portuguese | 2,346,272 |
| French | 2,235,117 |
| German | 1,532,462 |
| Korean | 1,434,744 |
| Turkish | 659,814 |
| Chinese | 393,131 |
| Italian | 296,227 |

English is 5.6 times the next language and more than all nine others combined, which is why part c) tells you to drop it before the heatmap.

Selecting `["Peak_viewers"]` before `.sum()` keeps the result a Series. `df.groupby("Language").sum()` on the whole frame would also try to sum `Channel`, which concatenates strings.

</details>

### Part c)

Based on the result of part b):

- Visualize the obtained sum for `Peak_viewers` for the top 10 languages as a barplot using matplotlib
- Drop English. For the remaining 9 languages, create a heatmap using seaborn
  - Use the columns `Peak_viewers`, `Watch_time`, `Followers`
  - To make them comparable, use min-max normalization on each column
- Combine both plots in one matplotlib figure using `plt.subplots(1,2)`

```python
result_df = (df - df.min()) / (df.max() - df.min())   # column wise min max normalization
```

<details>
<summary>Solution</summary>

**`Followers` is not in the part-a dataframe.** `column_selection` has four columns and `Followers` is not one of them, so the aggregation has to go back to the full frame:

```python
rename = lambda c: re.sub(r"\(.*?\)", "", c).strip().replace(" ", "_")
full = df_full.rename(columns={c: rename(c) for c in df_full.columns})

cols = ["Peak_viewers", "Watch_time", "Followers"]
agg = full.groupby("Language")[cols].sum().loc[top10.index]
```

Indexing with `.loc[top10.index]` keeps the ten languages **in the order part b) produced**, which a fresh `groupby` would not.

| Language | Peak_viewers | Watch_time | Followers |
|---|---|---|---|
| English | 20,195,264 | 228,881,005,575 | 342,257,538 |
| Spanish | 3,616,715 | 25,581,245,295 | 53,018,656 |
| Russian | 3,277,461 | 27,840,609,765 | 25,140,056 |
| Portuguese | 2,346,272 | 27,601,786,080 | 33,907,964 |
| French | 2,235,117 | 24,952,911,375 | 29,022,481 |
| German | 1,532,462 | 19,304,087,745 | 23,489,011 |
| Korean | 1,434,744 | 27,794,413,845 | 20,187,388 |
| Turkish | 659,814 | 6,263,624,295 | 15,816,592 |
| Chinese | 393,131 | 10,168,679,430 | 6,051,436 |
| Italian | 296,227 | 4,285,684,125 | 5,592,352 |

**Normalise after dropping English**, not before. Dropping first means English no longer defines the maximum, so the remaining nine spread across the full 0 to 1 range instead of being squashed into the bottom tenth:

```python
no_en = agg.drop("English")
norm = (no_en - no_en.min()) / (no_en.max() - no_en.min())
```

| Language | Peak_viewers | Watch_time | Followers |
|---|---|---|---|
| Spanish | 1.000 | 0.904 | 1.000 |
| Russian | 0.898 | 1.000 | 0.412 |
| Portuguese | 0.617 | 0.990 | 0.597 |
| French | 0.584 | 0.877 | 0.494 |
| German | 0.372 | 0.638 | 0.377 |
| Korean | 0.343 | 0.998 | 0.308 |
| Turkish | 0.109 | 0.084 | 0.216 |
| Chinese | 0.029 | 0.250 | 0.010 |
| Italian | 0.000 | 0.000 | 0.000 |

Each column now runs 0 to 1 independently, which is the whole point: the three raw columns differ by four orders of magnitude and a heatmap on them would show one colour.

The interesting row is **Korean**: near the top on `Watch_time` (0.998) but middling on `Peak_viewers` (0.343) and `Followers` (0.308). Long viewing sessions on relatively small streams. **Russian** is the mirror image on followers (0.412 against 1.000 watch time). Those contrasts are the finding, and they are only visible because of the normalisation.

**The combined figure**

```python
import matplotlib.pyplot as plt
import seaborn as sns

fig, axs = plt.subplots(1, 2, figsize=(14, 5))

axs[0].bar(top10.index, top10.to_numpy())
axs[0].set_title("Sum of Peak viewers, top 10 languages")
axs[0].set_ylabel("Peak viewers")
axs[0].tick_params(axis="x", rotation=45)

sns.heatmap(norm, annot=True, fmt=".2f", cmap="viridis", ax=axs[1])
axs[1].set_title("Min-max normalised, English dropped")

plt.tight_layout()
plt.show()
```

`ax=axs[1]` is what puts the seaborn heatmap into the second panel. Without it seaborn draws on its own current figure and you get two separate images.

On the colormap: `viridis` is the sequible default. Avoid `jet` or `rainbow` for a quantity, for the reasons in the [CSC visualization week](https://en.wikipedia.org/wiki/Jet_colormap).

</details>

---

## Notes for the exam

- `dropna(how="all")` drops only fully empty rows. Plain `dropna()` drops any row with a single gap.
- `idxmin()` returns the pandas index label, which is not the CSV's own `rownames` value.
- °C = (°F − 32) × 5/9. The sheet prints the inverse formula.
- Arithmetic on a Series is already element-wise, so `map()` is only needed when the logic is not arithmetic.
- `np.percentile(x, 99)` on 1000 rows leaves 10 above it. Check the count against the share.
- `groupby(col)[target].sum()` keeps the result a Series. Omitting the target column sums everything, strings included.
- Min-max normalise **after** filtering, so the remaining values use the full range.
- `plt.subplots(1, 2)` gives a 1-D `axs`, so index `axs[0]` and `axs[1]`. Seaborn needs `ax=` to land in a panel.
- `nbconvert` flags are two hyphens, not em dashes.
