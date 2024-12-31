import os
import torch
from transformers import AutoModelForMultipleChoice, AutoTokenizer
from ml_service.settings import get_settings

SETTINGS = get_settings()

class MCQAModel:
    def __init__(self):
        """
        loads the model and tokenizer into memory. This is done once at initialization.
        """
        self.model_path = SETTINGS.MODEL_PATH 
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = AutoModelForMultipleChoice.from_pretrained(self.model_path)
        self.model.eval()

    def predict(self, text_with_blank: str, choices: list[str]) -> (str, float):
        """
        Perform inference to determine which choice best fills in the [BLANK].

        :param text_with_blank: The text containing [BLANK].
        :param choices: List of 4 possible choices (e.g. [choice1, choice2, choice3, choice4]).
        :return: (best_choice, confidence_score)
        """



        inputs = []
        for choice in choices:
            filled_text = text_with_blank.replace("[BLANK]", choice)


            tokenized = self.tokenizer(
                filled_text,
                max_length=256,
                padding="max_length",
                truncation=True,
                return_tensors="pt"
            )
            inputs.append(tokenized)


        input_ids = torch.cat([inp["input_ids"] for inp in inputs], dim=0).unsqueeze(0)
        attention_mask = torch.cat([inp["attention_mask"] for inp in inputs], dim=0).unsqueeze(0)



        # Make predictions
        with torch.no_grad():
            outputs = self.model(
                input_ids=input_ids,
                attention_mask=attention_mask

            )
            logits = outputs.logits
            best_choice_idx = torch.argmax(logits, dim=1).item()
            probs = torch.softmax(logits, dim=1).squeeze()
            confidence = probs[best_choice_idx].item()

        return choices[best_choice_idx], confidence


#instantiate a global MCQA model object
MCQA_MODEL = MCQAModel()
