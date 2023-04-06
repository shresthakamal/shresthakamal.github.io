
# Whhat happens inside a tokenizer?

-   Models can process raw text => numerical values
-   A tokenizer needs to:
    -   Split the input sentences into words, subwords or symbols (like punctuations) which will be called as tokens
    -   Map each token into an integer based on the vocabulary
    -   Add additional information that might be useful to the models (like separation tokens [SEP], [CLS])
-   Each of the processing steps needs to be done the exact same way the model was trained, so how do we know how the model was preprocessed?
    -   We get the information about the tokenizer from the model checkpoint:
    
## Loading a tokenizer from a checkpoint

- We will use `AutoTokenizer` class with its `from_pretraied()` method to get the information of the checkpoint for a pre-trained model
- We will use the pre-trained model `distilbert-base-uncased-finetuned-sst-2-english` for the same.  [modelcard](https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english)

```python
from transformers import AutoTokenizer

checkpoint = "distilbert-base-uncased-finetuned-sst-2-english"

tokenizer = AutoTokenizer.from_pretraied(checkpoint)

```
-   From this we can directly pass our sentence to our tokenizer and get the numerical values(called the input ids)
```
raw_inputs = [
    "I've been waiting for a HuggingFace course my whole life.",
    "I hate this so much!",
]
inputs = tokenizer(raw_inputs, padding=True, truncation=True, return_tensors="pt")
```
```
{
    'input_ids': tensor([
        [  101,  1045,  1005,  2310,  2042,  3403,  2005,  1037, 17662, 12172, 2607,  2026,  2878,  2166,  1012,   102],
        [  101,  1045,  5223,  2023,  2061,  2172,   999,   102,     0,     0,     0,     0,     0,     0,     0,     0]
    ]), 
    'attention_mask': tensor([
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
}
```


-   Download the tokenizer and cache it

-   One thing to understand here is that the transformers models only take tensors as input. So we need to convert our numerical values to tensors
-   To ensure we get tensors we specify `return_tensors = "pt` where `pt = pytorch`
- **The main thing to remember here is that: you can pass one or a list of sentences at once.** 

-   So, we saw here how to load a tokenizer from a checkpoint. We will now do thhe same for the model as well.

## Loading the model through the checkpoint

-   As we can see in the previously, we loaded tokenizer through the checkpoint

-   Loading the model is the same as tokenizer simply we use `AutoModel` class with `from_pretrained` method.


```python
from transformers import AutoModel

checkpoint = "distilbert-base-uncased-finetuned-sst-2-english"

model = AutoModel.from_pretrained(checkpoint)

```


-   Now that we have the tokenizer and the model setup, we can give the model the inputs and get the hiddenstate representations from the transformers model.=> This representations is suppsed to be the high dimensional contextual representation of the input text.
-   Also, such hiddenstates are usually inputs to the classification head.


**A high dimensional vector** : What do we men by this?

-   `Batch Size`: The number of sequence processed at one time
-   `sequence lenght`: The length of numerical representations of the sequence [no of transformers used]
-   `hidden size`:  The vector dimension for each model input [BERT = 768]

Now, 

```
outputs = model(**inputs)
print(outputs.last_hidden_state.shape)

---

torch.Size([2, 16, 768])

```
So, we have provided `2` inputs to the model, and are getting `16` representations of the inputs where each representation is of `768` dimension..


## Passing the model ouputs to the classification head

-   Now that we have a representation of the input sequences we can pass them through a classification head to carry out a downstream task

![Pipeline](https://huggingface.co/datasets/huggingface-course/documentation-images/resolve/main/en/chapter2/transformer_and_head.svg)

-   So, there are many architectures in transformers that are designed to tackle many tasks

- Lets say we want to do sentiment classification (text classification) with binary output:
    -   We can load a model with `AutoModel` class and add a classification head on top of in
    -   OR we can load a model that already has a [model + classification head] in it 
        -   So, to load a model that is already designed for classification task we use: `AutoModelForSequenceClassification`

        ```
        from transformers import AutoModelForSequenceClassification

        checkpoint = "distilbert-base-uncased-finetuned-sst-2-english"
        model = AutoModelForSequenceClassification.from_pretrained(checkpoint)
        outputs = model(**inputs)

        print(outputs.logits.shape)
        ---

        torch.Size([2, 2])

        ```
    -   As we can see the the `outputs` shape is different this time as we already have a classification head on top of it
        -   Since we have `2` sentences as our input, we are getting 2 * 2 output, where each sequence has [logits1, logits2]
         ```
         print(outputs.logits)
         ---
        tensor([[-1.5607,  1.6123],
        [ 4.1692, -3.3464]], grad_fn=<AddmmBackward>)
         ```

## Post processing the ouputs

-   Now that we have the output logits, we need to post-process it to make a sense out of it
-   For that we will use `Softmax` function from pytorch to get probability predictions [normalized probability scores]

```
import torch

predictions = torch.nn.functional.softmax (outputs.logits, dim = -1)
print(predictions)
---
tensor([[4.0195e-02, 9.5980e-01],
        [9.9946e-01, 5.4418e-04]], grad_fn=<SoftmaxBackward>)
```

-   Now we have softmax probabilities
-   here, for  `dim = -1`: [Referencee](https://i.stack.imgur.com/UTmK7.png)
    -   The dimension of our logits is `[2 X 2]` or `[R X C]`, 
        -   so `dim=0` means R wise or Row wise meaning the elements are selected rowise
        -   so `dim=1` means C wise or Column wise meaning the elements are selected columns wise
        -   so `dim=-1` mean last dimension == C == Column wise
        -   eg:
            ```
                [[1., 2.],
                [3., 4.]]
            ```
            -   `dim=0` == Rowise = means get the softmax between (1 and 3) and (2 and 4)
            -   `dim=1` == Column wise = means get the softmax between (1,2) and (3 and 4)
            -   `dim=-1` = `dim=1`
        
        -   So the logits we had gave:
            ```
                tensor([[-1.5607,  1.6123],
                [ 4.1692, -3.3464]], grad_fn=<AddmmBackward>)
                ---
                tensor([[4.0195e-02, 9.5980e-01],
                [9.9946e-01, 5.4418e-04]], grad_fn=<SoftmaxBackward>)
                ```
            -   (e^-1.5607)  / (e^-1.5607 + e^1.6123) = 0.04019


-   Now that we have [0.0402, 0.9598] for the first sentence and [0.9995, 0.0005] for second.
-   So is the first label positive or negative?
    -   We look at the model `id2label` property 
    
    ```
    model.confid.id2label
    ---
    {0: 'NEGATIVE', 1: 'POSITIVE'}
    ```
    -  So, we can conclude that the model predicted 0.0402 for negative and 0.95 for positive for the first sentence.


That is how a Pipeline function works in trannsformers annd how inputs are processed through model and post processed.
     
## License

[Hugging Face](https://huggingface.co/course/chapter2/2?fw=pt)

