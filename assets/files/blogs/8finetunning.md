
# Finetuning the Model with Trainer API


-   The most difficult part of training is the environment setup: GPU
-   What we have until now:
```
def tokenize_function(example):
    return tokenizer(example["sentence1"], example["sentence2"], truncation=True)
```

```
from datasets import load_dataset
from transformers import AutoTokenizer, DataCollatorWithPadding

checkpoint = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)

raw_datasets = load_dataset("glue", "mrpc")
tokenized_datasets = raw_datasets.map(tokenize_function, batched=True)

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
```

-   Training
    -   To instansiate the trainer we need to setup `Training Arguments`
```
from transformers import TrainingArguments

training_args = TrainingArguments("directory-to-save-checkpoints")    
```

Now lets define the training loops:

```
# MODEL
from transformers import AutoModelForSequenceClassification

model = AutoModelForSequenceClassification.from_pretrained(checkpoint, num_labels=2)
```
```
from transformers import Trainer

trainer = Trainer(
    model,
    training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
    data_collator=data_collator,
    tokenizer=tokenizer,
)


trainer.train()

```

-   This will start the training process
    -   Report Training loss every 500 steps
    -   Wont report validation metrics as we didnt setup `evaluation_strategy` to either `steps` or `epochs`
    -   We didnt provide any metrics with `compute_metrics()`, so will only report loss


-   To get the predictions from the model we can use:
```
predictions = trainer.predict(tokenized_datasets["validation"])
print(predictions.predictions.shape, predictions.label_ids.shape)
---

(408, 2) (408,)
```

-   As we can see we are getting logits `(408, 2)`, to convert them to predictions we can use: `np.argmax`
    -   This will give us predictions and we can now compare it with labels
```
import numpy as np

preds = np.argmax(predictions.predictions, axis=-1)
---
(408, )
```

-   Now we can compute the different metrics: There already are metrics to evaluate MRPC dataset so we will simply load them:

```
from datasets import load_metric

metric = load_metric("glue", "mrpc")
metric.compute(predictions=preds, references=predictions.label_ids)
---

{'accuracy': 0.8578431372549019, 'f1': 0.8996539792387542}
```

-   We can wrap the same inside a wrapper `compute_metrics()` to pass it through the trainer function so

```
def compute_metrics(eval_preds):
    metric = load_metric("glue", "mrpc")
    logits, labels = eval_preds
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)
```

So Putting it in all together:

```
training_args = TrainingArguments("test-trainer", evaluation_strategy="epoch")

model = AutoModelForSequenceClassification.from_pretrained(checkpoint, num_labels=2)

trainer = Trainer(
    model,
    training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
    data_collator=data_collator,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

trainer.train()


```