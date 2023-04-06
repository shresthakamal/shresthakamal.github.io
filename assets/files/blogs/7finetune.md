
# Fine Tuning a pre-trained model

-   Till now we learned how to use tokenizers and pretrained models to make predictions
-   But till now we have not talked about using our own dataset.

    -   How do we work with a large dataset from hub?
    -   How to use TrainerAPI to finetune the model?
    -   How to use a custom training loop?

    ```
    from transformers import AutoTokenizer, AutoModelForSequenceClassification

    checkpoint = "bert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    model = AutoModelForSequenceClassification.from_pretrained(checkpoint)  
    ```


    -   Some points to remember here:
    ```
        checkpoint = "bert-base-uncased"
        tokenizer = AutoTokenizer.from_pretrained(checkpoint)
        model = AutoModelForSequenceClassification.from_pretrained(checkpoint)
    ```
        -   `AutoTokenizer` will pick up details that say how the model was preprocessed

        -   We are using the checkpoint of `bert-base-uncased`
            -   It contains the pre-trained weights for the `MODEL`

        -   But `AutoModelForSequenceClassification` includes: `MODEL` + `CLASSIFICATION HEAD`
            -   So we only have pre-trained weights for the MODEL
        
    Hence, we receive a warning message as:

        ```
            Some weights of the model checkpoint at bert-base-uncased were not used when initializing BertForSequenceClassification: ['cls.predictions.transform.dense.bias', 'cls.predictions.bias', 'cls.predictions.decoder.weight', 'cls.seq_relationship.weight', 'cls.predictions.transform.dense.weight', 'cls.predictions.transform.LayerNorm.bias', 'cls.seq_relationship.bias', 'cls.predictions.transform.LayerNorm.weight']
            - This IS expected if you are initializing BertForSequenceClassification from the checkpoint of a model trained on another task or with another architecture (e.g. initializing a BertForSequenceClassification model from a BertForPreTraining model).
            - This IS NOT expected if you are initializing BertForSequenceClassification from the checkpoint of a model that you expect to be exactly identical (initializing a BertForSequenceClassification model from a BertForSequenceClassification model).
            Some weights of BertForSequenceClassification were not initialized from the model checkpoint at bert-base-uncased and are newly initialized: ['classifier.bias', 'classifier.weight']
            You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
        ```
        -   clearly says that the model we are loading has an additional head that needs to be trained on a downstream task


### Fine-Tuning

-   We take a sequence (or a number of sequences), pass it through a tokenizer and get the input_ids, attention_mask
    
    ```
        sequences = [
            "I've been waiting for a HuggingFace course my whole life.",
            "This course is amazing!",
        ]

        batch = tokenizer(sequences, padding=True, truncation=True, return_tensors="pt")
        ---

        {
            'input_ids': tensor([
                [  101,  1045,  1005,  2310,  2042,  3403,  2005,  1037, 17662, 12172,
                2607,  2026,  2878,  2166,  1012,   102],
                [  101,  2023,  2607,  2003,  6429,   999,   102,     0,     0,     0,
                    0,     0,     0,     0,     0,     0]]), 
            'token_type_ids': tensor([
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]), 
                
            'attention_mask': tensor([
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]])}
        ```


-   If we now pass the `batch` to the model, then we will get the predictions but we dont want that now, we now want to pretrain the model.
-   So, we add another key:value pair to the variable `batch`

    ```
    batch["labels"] = torch.tensor([1, 1])
    ```

-   And then we train the model based on the labels we provided.
    ```
    optimizer = AdamW(model.parameters())
    loss = model(**batch).loss
    loss.backward()
    optimizer.step()
    ```
So, here we have used two sentences to fine tune the `base-base-uncased` model.


