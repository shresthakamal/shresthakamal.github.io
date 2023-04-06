# PERSONA-CHAT DATASET

- [bavard/personachat_truecased](https://huggingface.co/datasets/bavard/personachat_truecased) = True Cased Version of the original persona-chat dataset by Zhang et al.(2018).
- The original PersonaChat dataset is all lower case, and has extra space around each clause/sentence separating punctuation mark. This version of the dataset has more of a natural language look, with sentence capitalization, proper noun capitalization, and normalized whitespace.
- Each dialogue turn includes a pool of distractor candidate responses, which can be used by a muliple choice regularisaion loss during training.

```
Original: "i really like celine dion . what about you ?"
true-cased: "I really like Celine Dion. What about you?"

```

- Data Fields:

  - Each instance of the data represents a conversational utterance that a crowdworker made while pretending to ahve a certain personality.

  1.  `conv_id`: Conversation ID
  2.  `utterance_idx`: Index of the utterance in the conversation
  3.  `personality`: Sentence describing the personality of the current speaker
  4.  `history`: The conversation's utterances so far, alternating between the speaker with one utterance per speaker
  5.  `candidates`:A list of utterances including distractor utterances as well as the true utterance the speaker gave, given theier personality and the conversation history hus far. The true utterance is always the last utterance in the list.

## Citation

```
@article{zhang2018personalizing,
  title={Personalizing dialogue agents: I have a dog, do you have pets too?},
  author={Zhang, Saizheng and Dinan, Emily and Urbanek, Jack and Szlam, Arthur and Kiela, Douwe and Weston, Jason},
  journal={arXiv preprint arXiv:1801.07243},
  year={2018}
}
```
