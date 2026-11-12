# SW09 · Must-have Data Science Packages

**Date:** 2026-11-12, online
**Slides:** `sw09_ext_packages.pdf` (dated 11 Nov 2026) · **Exercises:** [SW09 exercise sheet](sw09_exercises.md)

Topics: numpy, pandas, matplotlib, seaborn, Jupyter and marimo notebooks.

This is the week the semester plan calls "External Packages", and it is the first one that needs third-party libraries. See [requirements](#requirements) before starting.

## Contents

1. [Numpy](#1-numpy)
2. [Pandas](#2-pandas)
3. [map and apply](#3-map-and-apply)
4. [Matplotlib](#4-matplotlib)
5. [Seaborn](#5-seaborn)
6. [Jupyter notebooks](#6-jupyter-notebooks)
7. [Marimo notebooks](#7-marimo-notebooks)
8. [Requirements](#requirements)

---

## 1. Numpy

Data scientists deal with categorical values, names (strings) and numerical values. For numerical values, **NumPy is the standard way to go**.

> "NumPy is the fundamental package for scientific computing in Python. It is a Python library that provides a multidimensional array object, various derived objects (such as masked arrays and matrices), and an assortment of routines for fast operations on arrays, including mathematical, logical, shape manipulation, sorting, selecting, I/O, discrete Fourier transforms, basic linear algebra, basic statistical operations, random simulation and much more."

The multidimensional array object, **ndarray**, holds sequences, matrices or multidimensional matrices of numerical values.

Important differences between NumPy arrays and standard Python sequences:

| | ndarray | list |
|---|---|---|
| Size | **Fixed at creation.** Changing the size creates a new array | Grows and shrinks in place |
| Element type | All elements must be of the **same** data type | Mixed types allowed |
| Operations | Advanced mathematical operations on large numbers of data, executed more efficiently and with less code | Loop over it yourself |

### Element-wise operations

The slide's example is multiplying two equally sized lists element by element. With built-in Python you need a loop or a comprehension. With numpy it is one expression:

```python
a = np.array([1, 2, 3, 4])
b = np.array([5, 6, 7, 8])
a * b                        # array([ 5, 12, 21, 32])
```

The same `*` on two Python lists does not multiply, it is not even defined. `[1,2] * 2` **repeats** the list. That operator difference is the practical reason to put numbers in an array rather than a list.

Docs: [numpy API reference](https://numpy.org/doc/stable/reference/index.html)

## 2. Pandas

For data handling, data scientists often work with **data frames**, which bring data into a structured order that facilitates analysis and manipulation.

> pandas is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool, built on top of the Python programming language.

Features listed on the slides:

- a fast and efficient **DataFrame** object with integrated indexing
- reading and writing between in-memory structures and CSV, text, Excel, SQL databases and HDF5
- intelligent data alignment and integrated handling of **missing data**
- flexible reshaping and pivoting
- label-based slicing, fancy indexing and subsetting
- columns can be inserted and deleted for size mutability
- aggregating or transforming with a **group by** engine, allowing split-apply-combine
- high performance merging and joining
- time series functionality: date range generation, frequency conversion, moving window stats, date shifting and lagging

### The data frame

A tabular data structure commonly used in data analysis and statistical computing:

- **Columns** represent variables (features)
- **Rows** represent observations (records)
- Indexing by labels or numerical indices, `[row, col]`
- Data frames can combine **heterogeneous** data types
- **One data type per column.** Heterogeneous data in one column results in the `object` data type

```
          V1      V2       V3
    0     11    Lucerne    LU
    1    321     Bern      BE
    2     53    Valais     VS
    3      4     Zug       ZG
    4     67    Geneva     GE
```

A data frame can be created from a dictionary:

```python
df = pandas.DataFrame({"V1": [11, 321, 53, 4, 67],
                       "V2": ["Lucerne", "Bern", ...],
                       "V3": [...]})
```

A **Series** is one-dimensional data: the index plus one column of a data frame.

The one-type-per-column rule is what makes the whole thing fast, and it is the first thing to check after loading a file. A column that should be numeric but shows up as `object` means something non-numeric slipped in, and every arithmetic operation on it will then behave strangely or fail.

Docs: [pandas API reference](https://pandas.pydata.org/docs/reference/index.html#api) · [cheat sheet](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)

## 3. map and apply

Working with data frames often means applying a function to all or many observations or variables:

| Function | Scope |
|---|---|
| `map()` | element-wise operations on data frames and Series |
| `apply()` | applies a function along a particular axis of a DataFrame |

Basic mathematical operations can be applied directly to variables.

> **Instead of using for- or while-loops for iterating over a sequence, with data frames these functions do the same job.**

That last line is the real message of the week. Everything from [SW03](../sw03/loops.md) still works, but on a data frame it is both slower and harder to read than the vectorised form:

```python
df["Temp_C"] = df["Temp"].map(fahrenheit_to_celsius)   # one pass, no loop
df["Temp_C"] = (df["Temp"] - 32) * 5 / 9               # faster still, pure arithmetic
```

The second form needs no function at all, because arithmetic on a Series is already element-wise. Reach for `map` when the per-element logic is not expressible as arithmetic. [Exercise 1](sw09_exercises.md#exercise-1-jupyter--marimo-notebooks) asks for `map()` explicitly, so use it there.

## 4. Matplotlib

> **Matplotlib:** a low-level library that provides a lot of flexibility and control over the creation of plots. Offers fully customizable figures.

Three fundamental components:

**Pyplot**, a collection of functions to create figures:

```python
import matplotlib.pyplot as plt

plt.plot([1,2,3,4,5], df["V1"])
plt.title("Simple Line Plot")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.show()
```

**Figure object**, the entire figure in which you can plot one or more axes. It is like a canvas on which your plots are drawn:

```python
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)    # 1 row, 1 column, 1st subplot

ax.plot([1,2,3,4,5], df["V1"])
ax.set_title("Line Plot on Axes")
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
```

**Axes object**, a single or a set of plots within a figure. This is the area where data is plotted, and it allows complex layouts:

```python
fig, axs = plt.subplots(2, 1)    # 2 rows, 1 column

axs[0].plot([1,2,3,4,5], df["V1"])
axs[0].set_title("First Subplot")
axs[0].set_xlabel("X-axis")
axs[0].set_ylabel("Y-axis")

axs[1].scatter([1,2,3,4,5], df["V1"])
axs[1].set_title("Second Subplot (Scatter)")
axs[1].set_xlabel("X-axis")
axs[1].set_ylabel("Y-axis")

plt.tight_layout()    # Adjusts layout to prevent overlap
plt.show()
```

Note the two styles do the same thing. `plt.plot(...)` draws on whatever figure is "current", which is convenient for one quick plot and confusing as soon as there are two. `fig, axs = plt.subplots(...)` names the objects, so every call says which axes it is drawing on. Use the second for anything you will come back to, and it is required for the combined figure in [Exercise 2c](sw09_exercises.md#part-c).

`plt.subplots(1, 2)` returns `axs` as a 1-D array, so the subplots are `axs[0]` and `axs[1]`. With `plt.subplots(2, 2)` it is 2-D and you index `axs[0, 1]`.

## 5. Seaborn

> **Seaborn:** built on top of Matplotlib, a high-level library specifically designed for statistical data visualization. Offers a variety of built-in themes, color palettes and styles, and is designed to work seamlessly with Pandas DataFrames.

Since seaborn builds on matplotlib, it is **mandatory to import pyplot** in order to add titles or show the plot directly:

```python
import seaborn as sns
import matplotlib.pyplot as plt

sns.scatterplot(data=df, x=[1,2,3,4,5], y='V1', hue='V2')

plt.title('Seaborn Scatter Plot Example')
plt.show()
```

Every seaborn function takes an `ax=` argument, which is how a seaborn plot goes into one panel of a matplotlib figure. That is the mechanism behind combining the barplot and the heatmap in [Exercise 2c](sw09_exercises.md#part-c).

## 6. Jupyter notebooks

> Jupyter Notebook is an open-source web application that allows you to create and share documents that contain code, equations, visualizations, and narrative text.

Main features:

- **Interactive code execution:** write and execute code in a cell-based format, allowing iterative development and testing
- **Rich text support:** Markdown for headings, lists, links and images ([markdownguide.org](https://www.markdownguide.org/))
- **Visualizations:** create and display plots and figures inline
- **Report:** export the notebook as HTML or PDF, so a report is always ready

```bash
jupyter nbconvert --to html --no-input path/to/notebook.ipynb
```

Jupyter and pandoc must be installed. **Note the slide prints em dashes** in that command where it needs two hyphens, `--to` and `--no-input`. Copying it straight off the slide fails.

`--no-input` hides the code cells and keeps only the markdown and the outputs, which is what makes the export read as a report rather than as source. PDF export additionally needs a LaTeX installation, so HTML is the path of least resistance.

## 7. Marimo notebooks

Marimo provides a similar approach to Jupyter but differs in key points:

- **Reactive execution:** cells update automatically when inputs change
- **Included UI framework:** `marimo.ui` lets you create dashboard-like content very easily
- **File format:** marimo files are pure Python text files (`yourbook.py`), so they can be versioned like any other code file with git

That last point is the one that matters for this repo. A `.ipynb` is JSON with the outputs embedded, so every run produces a diff even when the code did not change. A marimo notebook is a `.py` file and diffs like code.

Reactive execution also removes the classic Jupyter trap, where a notebook only works because you ran the cells in an order you can no longer reconstruct. In marimo that cannot happen.

## Requirements

This week is the first that needs packages beyond the standard library. With the virtual environment activated:

```bash
pip install numpy pandas matplotlib seaborn
pip freeze > requirements.txt
```

For the notebook export in [Exercise 1](sw09_exercises.md#exercise-1-jupyter--marimo-notebooks) add `jupyter`, and `pandoc` has to come from the system package manager rather than pip.

## Further tutorials

W3Schools offers tutorial sets for both packages, from introduction through to plots:

- NumPy: [w3schools.com/python/numpy](https://www.w3schools.com/python/numpy/default.asp)
- Pandas: [w3schools.com/python/pandas](https://www.w3schools.com/python/pandas/default.asp)
