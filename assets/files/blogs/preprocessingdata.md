
# Data Preprocessig with Dataset


### Loading the Dataset

```
data_files= {"train":"data/ijcnlp_dailydialog/train/dialogues_train.txt", 
            "test":"data/ijcnlp_dailydialog/test/dialogues_test.txt"}
```

We can load train and test files at once using the `load_dataset` function.

```
data = load_dataset("text", data_files = data_files)
---

DatasetDict({
    train: Dataset({
        features: ['text'],
        num_rows: 11118
    })
    test: Dataset({
        features: ['text'],
        num_rows: 1000
    })
})

```
-   Here `train` and `test` are keys and contains a dataset with a column `text` and specified number of rows
-   Selecting a specific sample of data from the dataset

```
sample = data.shuffle(seed=1234).select(range(1000))
```

-   Mapping the Dataset to a function

```
new_dataset = dataset.map(function_name)

```

-   What this does is it send each row one by one to the function like in pandas so, we can write a function that is lie:

```

row = an entire row like pandas dataframe


---
def function_name(row): # We will get rows
    // Manipulate row values
    // row["column_name] for a column values

    return {"column_name": manupulated_row}
```

-   We can do the same in batches as well by doing:

```
new_data = data.map(function, batched = True)
```
-   When you specify batched=True the function receives a dictionary with the fields of the dataset, but each value is now a list of values, and not just a single value. 
-   This will send a list of rows at once for a column like:
```
{
    "column1":[row1, row2...],
    "column2": [row1, row2, row3]...
    .
    .
    .
}

```

-   so we can process our dataset like:

```
def function_name(rows):
    return {"newcolumn: [row.split("__eou__) for row in rows["column1"]]}
```
-   Idea here is to return a list as well using list comprehension


## Swtiching to pandas dataframe and back

```
data.set_format("pandas")

```

-   Pandas to Dataset

```
data = Dataset.from_pandas(dataframe)
```




-   Saving the Dataset
```
dataset.save_to_disk("filename")

or

dataset = load_from_disk("filename")

```

