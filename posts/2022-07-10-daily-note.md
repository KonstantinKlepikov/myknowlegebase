---
title: Some pandas tricks 1
description: Sqlalchemy to pandas, statistics, select rows, set and delet values, iterating. And some about IPython
category: post
---
## Import an [[sqlalchemy]] table to a [[pandas]] dataframe

```python
table_df = pd.read_sql(
           'SELECT * from game',
           session_remote.bind
           )
```

- [source](https://stackoverflow.com/a/65973074/15966204)
- [source to](https://stackoverflow.com/questions/29525808/sqlalchemy-orm-conversion-to-pandas-dataframe)

## [How to calculate summary statistics](https://pandas.pydata.org/docs/getting_started/intro_tutorials/06_calculate_statistics.html#how-to-calculate-summary-statistics)

### Aggregating statistics

![](../attachments/2022-07-10-15-39-13.png)

```python
titanic["Age"].mean()
Out[4]: 29.69911764705882
```

![](../attachments/2022-07-10-15-40-04.png)

```python
titanic[["Age", "Fare"]].median()
Out[5]:
Age     28.0000
Fare    14.4542
dtype: float64
```

```python
titanic[["Age", "Fare"]].describe()
Out[6]:
              Age        Fare
count  714.000000  891.000000
mean    29.699118   32.204208
std     14.526497   49.693429
min      0.420000    0.000000
25%     20.125000    7.910400
50%     28.000000   14.454200
75%     38.000000   31.000000
max     80.000000  512.329200

# or
titanic.agg(
    {
        "Age": ["min", "max", "median", "skew"],
        "Fare": ["min", "max", "median", "mean"],
    }
)

Out[7]:
              Age        Fare
min      0.420000    0.000000
max     80.000000  512.329200
median  28.000000   14.454200
skew     0.389108         NaN
mean          NaN   32.204208
```

### Aggregating statistics grouped by category

![Aggregating statistics grouped by category](../attachments/2022-07-10-15-37-28.png)

```python
titanic[["Sex", "Age"]].groupby("Sex").mean()
Out[8]:
              Age
Sex
female  27.915709
male    30.726645
```

[more about this](https://pandas.pydata.org/docs/getting_started/intro_tutorials/06_calculate_statistics.html#aggregating-statistics-grouped-by-category)

### Count number of records by category

![](../attachments/2022-07-10-15-43-20.png)

```python
titanic["Pclass"].value_counts()
Out[12]:
3    491
1    216
2    184
Name: Pclass, dtype: int64

# or
titanic.groupby("Pclass")["Pclass"].count()
Out[13]:
Pclass
1    216
2    184
3    491
Name: Pclass, dtype: int64
```

[How to calculate summary statistics](https://pandas.pydata.org/docs/getting_started/intro_tutorials/06_calculate_statistics.html#how-to-calculate-summary-statistics)

## How do I select rows from a DataFrame based on column values

```python
df.loc[df['column_name'] == some_value]

df.loc[df['column_name'].isin(some_values)]

df.loc[(df['column_name'] >= A) & (df['column_name'] <= B)]
# Note the parentheses. Due to Python's operator precedence rules, & binds more tightly than <= and >=. Thus, the parentheses in the last example are necessary. Without the parentheses

df.loc[df['column_name'] != some_value]

df.loc[~df['column_name'].isin(some_values)]
```

[source](https://stackoverflow.com/a/17071908/15966204)

## How to select rows with one or more nulls from a pandas DataFrame without listing columns explicitly

```python
In [60]: df[pd.isnull(df).any(axis=1)]
Out[60]:
   0   1   2
1  0 NaN   0
2  0   0 NaN
```

[sourse](https://stackoverflow.com/a/14247708/15966204)

## Set value of one column based on value in another column

```python
df.loc[df['c1'] == 'Value', 'c2'] = 10
```

[more examples](https://stackoverflow.com/questions/49161120/pandas-python-set-value-of-one-column-based-on-value-in-another-column)

## Replacing Rows in Pandas DataFrame with Other DataFrame Based on Index

```python
df1.update(df2)
>>> df1
       B     C
A
0  300.0   6.0
1  400.0   7.0
2  433.0  99.0
3  555.0  99.0
```

Or use `df1.combine_first(df2)`. [Source](https://stackoverflow.com/a/53727235/15966204)

## Deleting DataFrame row in Pandas based on column value

```python
df = df[df.line_race != 0]
```

[more examples](https://stackoverflow.com/questions/18172851/deleting-dataframe-row-in-pandas-based-on-column-value)

## Use [[tqdm]] Progress Bar with Pandas

```python
for index, row in tqdm(df.iterrows(), total=df.shape[0]):
   print("index",index)
   print("row",row)
```

[source](https://stackoverflow.com/a/52309010/15966204)

## Most straightforward row iteration with [[pandas]]

```python
df = sns.load_dataset('iris')
for index, row in df.iterrows():
    print(row, '\n')

# or itertuples()
species_labels = {'setosa': 0, 'versicolor': 1, 'virginica': 2}

for row in df.itertuples():
    label = species_labels[row.species]
    df['species'].at[row.Index] = label # update the row in the dataframe

# or apply()
species_labels = {'setosa': 0, 'versicolor': 1, 'virginica': 2}

df['species'] = df.apply(lambda row: species_labels[row['species']], axis=1)

# or map()
species_labels = {'setosa': 0, 'versicolor': 1, 'virginica': 2}

df['species'] = df['species'].map(species_labels)
```

[source](https://www.learndatasci.com/solutions/how-iterate-over-rows-pandas/)

## How to show PIL Image in ipython notebook

```python
from IPython.display import Image
pil_img = Image(filename='data/empire.jpg')
display(pil_img)

# or
from matplotlib.pyplot import imshow
import numpy as np
from PIL import Image

%matplotlib inline
pil_im = Image.open('data/empire.jpg', 'r')
imshow(np.asarray(pil_im))

# or
from PIL import Image               # to load images
from IPython.display import display # to display images

pil_im = Image.open('path/to/image.jpg')
display(pil_im)
```

[source](https://stackoverflow.com/questions/26649716/how-to-show-pil-image-in-ipython-notebook)

## IPython Notebook output cell is truncating contents of my list

```python
pd.options.display.max_rows = 4000
```

This can be used as context. [Source](https://stackoverflow.com/questions/23388810/ipython-notebook-output-cell-is-truncating-contents-of-my-list)

Смотри еще:

- [Pandas Getting started tutorials](https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html)
- [[pandas]]
- [[2022-07-23-daily-note]] Some tricks for creation, get values, set new columns and groupby
- [[lists/sqlalchemy]]
- [[tqdm]]
- [[PIL]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[sqlalchemy]: ../lists/sqlalchemy "Sqlalchemy"
[pandas]: ../notes/pandas "Pandas"
[tqdm]: ../notes/tqdm "Tqdm"
[2022-07-23-daily-note]: 2022-07-23-daily-note "Some pandas tricks 2"
[lists/sqlalchemy]: ../lists/sqlalchemy "Sqlalchemy"
[PIL]: ../notes/PIL "Pillow - обработка изображений"
[//end]: # "Autogenerated link references"
[//begin]: # "Autogenerated link references for markdown compatibility"
[sqlalchemy]: ../lists/sqlalchemy "Sqlalchemy"
[pandas]: ../notes/pandas "Pandas"
[tqdm]: ../notes/tqdm "Tqdm"
[pandas]: ../notes/pandas "Pandas"
[pandas]: ../notes/pandas "Pandas"
[2022-07-23-daily-note]: 2022-07-23-daily-note "Some pandas tricks 2"
[lists/sqlalchemy]: ../lists/sqlalchemy "Sqlalchemy"
[tqdm]: ../notes/tqdm "Tqdm"
[PIL]: ../notes/PIL "Pillow - обработка изображений"
[//end]: # "Autogenerated link references"