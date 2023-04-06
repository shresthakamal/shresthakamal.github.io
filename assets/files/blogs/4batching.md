
# Batching input sentences together


-   How do we handle multiple input sentences?
-   How do we handle multiple input sentences of varied words length?


### **Model Always expects a batch of inputs**

```
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

checkpoint = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForSequenceClassification.from_pretrained(checkpoint)

sequence = "I've been waiting for a HuggingFace course my whole life."


tokens = tokenizer.tokenize(sequence)
ids = tokenizer.convert_tokens_to_ids(tokens)
input_ids = torch.tensor(ids)


# This line will fail.
model(input_ids)

```
```
print(input_ids)
print(input_ids.shape)
---
tensor([ 1045,  1005,  2310,  2042,  3403,  2005,  1037, 17662, 12172,  2607,
         2026,  2878,  2166,  1012])
         ---
torch.Size([14])
```

-   We did exactly what we thought a tokenizer would do, still the model inputs is failing
    -   This is because the model expects the inputs to be in batch
    -   As we can see from the above output that we are only giving 1D tensor to the model which it doesnot accept

    ``` IndexError: Dimension out of range (expected to be in range of [-1, 0], but got 1)```

-   Lets see what the tokenizer does on top of it:

```
tokenized_inputs = tokenizer(sequence, return_tensors="pt")
print(tokenized_inputs["input_ids"])
---
tensor([[  101,  1045,  1005,  2310,  2042,  3403,  2005,  1037, 17662, 12172,
          2607,  2026,  2878,  2166,  1012,   102]])
---
torch.Size([1, 16])
```
_Here dont confuse with [2, 16, 768]: this is the model output where the model is giving 16 different 768 representations for 2 different sentences_

_But here we are working on how we are providing input to the model: should be in multiple sentences like [7, 29]_


## Batching
-   Sendin multiple sentences through the model
-   How will we batch the input ids?

```
    batched_ids = [
        [200, 200, 200], # First mapping of tokens
        [200, 200]       # Second mapping of tokens
    ]   
```
-   But when we are working with tokens, we need a rectangular shape
-   Working with multiple sentences, we might have different sequence length  = no of tokens = no of ids = Diffrent size tensors = Model wont take such input
-   Solution: **Use padding**: Ensures that the shape of the input tokens is the same [Rectangular]

```
    padding_id = 100

    batched_ids = [
        [200, 200, 200],
        [200, 200, padding_id],
    ]

```
-   Padding is different in all tokenizers and can be retreived as: `tokenizer.pad_token_id`
-   Padding will not affect the model and give wont give different result when and not padded.
```
model = AutoModelForSequenceClassification.from_pretrained(checkpoint)

sequence1_ids = [[200, 200, 200]]
sequence2_ids = [[200, 200]]
batched_ids = [
    [200, 200, 200],
    [200, 200, tokenizer.pad_token_id],
]

print(model(torch.tensor(sequence1_ids)).logits)
---
tensor([[ 1.5694, -1.3895]], grad_fn=<AddmmBackward0>)


print(model(torch.tensor(sequence2_ids)).logits)
---
tensor([[ 0.5803, -0.4125]], grad_fn=<AddmmBackward0>)


print(model(torch.tensor(batched_ids)).logits)
---
tensor([[ 1.5694, -1.3895],
        [ 1.3374, -1.2163]], grad_fn=<AddmmBackward0>)

```

-   As we can see from the above outputs, we are getting different logits for the second sequence (padded and not padded) => This shouldnt happen
-   Solution: **Attention Mask**: Use attention maps to tell model to ignore particular tokens

```
batched_ids = [
    [200, 200, 200],
    [200, 200, tokenizer.pad_token_id],
]

attention_mask = [
    [1, 1, 1],
    [1, 1, 0],
]

batched_ids = [
    [200, 200, 200],
    [200, 200, tokenizer.pad_token_id],
]

attention_mask = [
    [1, 1, 1],
    [1, 1, 0],
]

outputs = model(torch.tensor(batched_ids), attention_mask=torch.tensor(attention_mask))
print(outputs.logits)
---

tensor([[ 1.5694, -1.3895],
        [ 0.5803, -0.4125]], grad_fn=<AddmmBackward>)
```
-    Hence, we can see that we have received the same outputs if we had padded or not.