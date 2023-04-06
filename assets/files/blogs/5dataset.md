
# Working with Dataset

[Dataset Hub](https://huggingface.co/datasets)

-   The huggingface hub doesnt not only contain model but also contains datasets to work with

```
from datasets import load_dataset

raw_datasets = load_dataset("glue", "mrpc")
---

DatasetDict({
    train: Dataset({
        features: ['sentence1', 'sentence2', 'label', 'idx'],
        num_rows: 3668
    })
    validation: Dataset({
        features: ['sentence1', 'sentence2', 'label', 'idx'],
        num_rows: 408
    })
    test: Dataset({
        features: ['sentence1', 'sentence2', 'label', 'idx'],
        num_rows: 1725
    })
})
```

-   Dataset dictionary contains train, validation and test keys as we can see above.
-   Looking at the individual row in the dataset.

```
raw_train_dataset = raw_datasets["train"]
raw_train_dataset[0]
---
{'idx': 0,
 'label': 1,
 'sentence1': 'Amrozi accused his brother , whom he called " the witness " , of deliberately distorting his evidence .',
 'sentence2': 'Referring to him as only " the witness " , Amrozi accused his brother of deliberately distorting his evidence .'}

```
-  The above data contains two sequences with a label marked by an index.

-   To check which `label = 1` means what we can do:
```
raw_train_dataset.features
---
{'sentence1': Value(dtype='string', id=None),
 'sentence2': Value(dtype='string', id=None),
 'label': ClassLabel(num_classes=2, names=['not_equivalent', 'equivalent'], names_file=None, id=None),
 'idx': Value(dtype='int32', id=None)}
```
    -   It shows that `1 = equivalent` and `0 = not_equivalent`