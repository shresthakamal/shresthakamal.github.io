
# Preprocessing a dataset

![]{/files/blogs/glue.png}

```
from datasets import load_dataset

raw_datasets = load_dataset("glue", "mrpc")
raw_datasets
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

DataType = Dataset
```

-   A tokenizer can take one sentence or a list of sentences
-   So, we can pass the list of first sentences as a whole like:
    ```
    from transformers import AutoTokenizer

    checkpoint = "bert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    tokenized_sentences_1 = tokenizer(raw_datasets["train"]["sentence1"])
    tokenized_sentences_2 = tokenizer(raw_datasets["train"]["sentence2"])

    ```
-   But we dont want this, we want to pass the sentences as a pair, How do we do that?
    -   Fortunately, `bert-base-uncased` takes sentence pairs as inputs as well. So,

        ```
        inputs = tokenizer("This is the first sentence.", "This is the second one.")
        inputs
        ---
        { 
        'input_ids': [101, 2023, 2003, 1996, 2034, 6251, 1012, 102, 2023, 2003, 1996, 2117, 2028, 1012, 102],
        'token_type_ids': [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
        'attention_mask': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        }

        ```
    -   We can see `token_type_ids` here which signifies model, which is the first part of the input and which is the second.
    -   Such `token_type_ids` are only returned by models that know what to do with them and wont be returned for models with other checkpoint.
    
    
    -   Decoding the input_ids we get:

```
tokenizer.convert_ids_to_tokens(inputs["input_ids"])
---
['[CLS]', 'this', 'is', 'the', 'first', 'sentence', '.', '[SEP]', 'this', 'is', 'the', 'second', 'one', '.', '[SEP]']
```
-   clearly shows that the model added special tokens on top of it as well.
-   Since BERT is pretrained with Masked Language Modelling(MLM) and Next Sentence Prediction (NSP), this checkpoint returns the token_type_ids

OR


- While passing two sentences to the tokenizer: instead of passing two sentences we can pass two list of sentences:
```
inputs = tokenizer(["This is the first sentence.", "Hello"],["This is the second one.", "Hello"], padding = True, truncation = True, return_tensors = "pt")
inputs["input_ids"]
---
tensor([[ 101, 2023, 2003, 1996, 2034, 6251, 1012,  102, 2023, 2003, 1996, 2117,
         2028, 1012,  102],
        [ 101, 7592,  102, 7592,  102,    0,    0,    0,    0,    0,    0,    0,
            0,    0,    0]])
```
-   Decoding them:
    -   We can clearly see the insertion of special tokens.
```
print(tokenizer.convert_ids_to_tokens(inputs["input_ids"][0]))
---

['[CLS]', 'this', 'is', 'the', 'first', 'sentence', '.', '[SEP]', 'this', 'is', 'the', 'second', 'one', '.', '[SEP]']

```


- Finally
    ```
    tokenized_dataset = tokenizer(
        raw_datasets["train"]["sentence1"],
        raw_datasets["train"]["sentence2"],
        padding=True,
        truncation=True,
    )
    ```
-   We will get a dictionary from the above code and this will take a lot of RAM memory as there are a number of sentences and will give {input_ids, token_type_ids, attention_mask} = Huge Space Complexity

-   **Solution: Keep Dataset as dataset using `Dataset.map()`**
    -   Similar to applying a function to each row of a pandas dataframe

        ```
        def tokenize_function(example):
            return tokenizer(example["sentence1"], example["sentence2"], truncation=True)
        ```
    -   This function takes a dictionary like our dataset and returns a dictionary with input_ids, token_type_ids and more for each row of data

        ```
        tokenized_datasets = raw_datasets.map(tokenize_function, batched=True)
        tokenized_datasets
        ---

        DatasetDict({
            train: Dataset({
                features: ['attention_mask', 'idx', 'input_ids', 'label', 'sentence1', 'sentence2', 'token_type_ids'],
                num_rows: 3668
            })
            validation: Dataset({
                features: ['attention_mask', 'idx', 'input_ids', 'label', 'sentence1', 'sentence2', 'token_type_ids'],
                num_rows: 408
            })
            test: Dataset({
                features: ['attention_mask', 'idx', 'input_ids', 'label', 'sentence1', 'sentence2', 'token_type_ids'],
                num_rows: 1725
            })
        })
        ```
    -   Here, `batched = True` applies the function to multiple items at once for faster processing.


We now know how to tokenize sentences in batch using the Dataset and `.map()` function.


### Dyanamic Padding
-   When we are providing batches of inputs, we are giving multiple sequences as input which are of **varied length**.
    -   So when we are padding, if we do max_length = some value, we might be padding at the maximum length of all sentences
    -   So what we want to do is: pad the sentences based on the longest sequence for a batch using **Dyanamic Padding**

-   Looking at one batch:
    ```
    samples = tokenized_datasets["train"][:8]
    samples = {k: v for k, v in samples.items() if k not in ["idx", "sentence1", "sentence2"]}
    [len(x) for x in samples["input_ids"]]
    ---

    [50, 59, 47, 67, 59, 50, 62, 32]
    ```
    -   Looking at this batch, we can see that the toke length for each sequence is different
    -   So, the padding should be `67` to all the sentences in the batch

-   We use `DataCollatorWithPadding`

```
from transformers import DataCollatorWithPadding

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

batch = data_collator(samples)

{k: v.shape for k, v in batch.items()}

---
{
    'attention_mask': torch.Size([8, 67]),
    'input_ids': torch.Size([8, 67]),
    'token_type_ids': torch.Size([8, 67]),
    'labels': torch.Size([8])
    }


```

Now that we have been done with the tokenizer, datasets, maping a function to the dataset and dyanamic padding.

Next Step: **Fine Tuning a model**