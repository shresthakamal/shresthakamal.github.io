
# Using Transformers for Inference


-   say we have a sequuence, `sequences = ["Hello!", "Cool.", "Nice!"]`
-   Tokenizers converts these sequences to numerical values like:
```
encoded_sequences = [
    [101, 7592, 999, 102],
    [101, 4658, 1012, 102],
    [101, 3835, 999, 102],
]

## Matrices of Tensors = Rectangular Shape
```
-   Model needs the values to be converted to tensors and take these sequences to give some outputs

```
import torch

model_inputs = torch.tensor(encoded_sequences)
```

## Lets see how the entire process works in detail:

### Tokenizers

-   Translated Text data to the form the model can read
-   Example Text: `Jim Henson was a puppeteer`

Types of Tokenizers: (on the basis of what the sequences will be broken down into)

####    1.  Word Based Tokenizers
![WBT](https://huggingface.co/datasets/huggingface-course/documentation-images/resolve/main/en/chapter2/word_based_tokenization.svg)


-   For word based tokenizers we can simply use `split()`

    ```
    tokenized_text = "Jim Henson was a puppeteer".split()
    print(tokenized_text)
    ---
    ['Jim', 'Henson', 'was', 'a', 'puppeteer']
    ```
-   With suuch tokenizers we have a huge volcabulary [=total no of independent tokens]
-   So, a language vocabulary might contain 500, 000+ tokens.
-   Also words like `dog` and `dogs` are considered different and unrelated based on word tokenizers
-   So one way to reduce the increase in the vocabulary length is to go deeper: **character based tokens**

####    2. Character Based tokenizers
![](https://huggingface.co/datasets/huggingface-course/documentation-images/resolve/main/en/chapter2/character_based_tokenization.svg)

-   Each sequences is split into character rather than words
    -   So, vocabulary is small [number of english character = ASCII]
    -   Much fewer out of vocab items or unknnown tokens
-   Cons   
    -   Going character level on tokenization, we might argue that we are loosing all the meanings as each charaters doesnt mean anything on its own (for english language) but for other languages it might mean something and more
    -   The sequuence length is going to be very large as model has to process a ot of tokens
        -   Solution: **Sub-Word tokenization**


#### 3. Sub Word Tokenizers
![](https://huggingface.co/datasets/huggingface-course/documentation-images/resolve/main/en/chapter2/bpe_subword.svg)

-   So core intuition is: Frequenty used words shoulnt be splitted into sub-words whereas the unseen or rarely used or new words should be splitted into its sub-words to more clarify the meanings
-   For Example: `annoyingly` should be broken down into `annoying` and `ly`
    -   Provides a lot of semantic information


#### Many mores:
-   Byte Level BPE = used in GPT2
-   WordPiece  = used in BERT
-   SentencePeice or Unigram = Multilingual Models



## Loading and Saving a Tokenizer

```tokenizer.save_pretrained("directory_on_my_computer")```

-   Similar to models 
    -   `save_pretrained()`, `from_pretrained()`
        -   This will get us the BERT Tokenizer from BERT pretrained checkpoints. 
        -   Can also use `AutoTokenizer` using pretrained checkpoints to get the BERT tokenizer automatically
    ```

    from transformers import BertTokenizer

    tokenizer = BertTokenizer.from_pretrained("bert-base-cased")
    
    or

    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")

    ```
    -   My opinion: Saving tokenizers means saving the vocabulary, the pre-processing steps

-   Now we can use tokenizers:

```
tokenizer("Using a Transformer network is simple")

---
{'input_ids': [101, 7993, 170, 11303, 1200, 2443, 1110, 3014, 102],
 'token_type_ids': [0, 0, 0, 0, 0, 0, 0, 0, 0],
 'attention_mask': [1, 1, 1, 1, 1, 1, 1, 1, 1]}

```

#### Tokenization Pipeline
![](/files/blogs/tokenizationpipe.png)

-   Encoding: Text into Numbers
    -   Raw Text > Tokens > Add Special Tokens > input_ids
```
tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")

# RAW TEXT
sequence = "Using a Transformer network is simple"

# SUB-WORD TOKENS
tokens = tokenizer.tokenize(sequence)
---
['Using', 'a', 'transform', '##er', 'network', 'is', 'simple']


# INPUT IDS
ids = tokenizer.convert_tokens_to_ids(tokens)
---
[7993, 170, 11303, 1200, 2443, 1110, 3014]

```

-   Decoding
```
decoded_string = tokenizer.decode([7993, 170, 11303, 1200, 2443, 1110, 3014])
---
'Using a Transformer network is simple'
```
-   As we can see above, decoding not only converts the ids to words, it groups the sub words as well to form the words