from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from app.config import settings
import torch


class Generator:
    def __init__(self, model_name: str = None, device: str = None):
        self.model_name = model_name or settings.generator_model
        self.device = device if device is not None else (0 if torch.cuda.is_available() else -1)
        self._pipe = None


    @property
    def pipe(self):
        if self._pipe is None:
            tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            model = AutoModelForCausalLM.from_pretrained(self.model_name, device_map='auto' if torch.cuda.is_available() else None)
            self._pipe = pipeline('text-generation', model=model, tokenizer=tokenizer, device=self.device)
        return self._pipe


    def generate(self, prompt: str, max_new_tokens: int = 200):
        out = self.pipe(prompt, max_new_tokens=max_new_tokens, do_sample=False)
        return out[0]['generated_text']


# singleton
_gen = None


def get_generator():
    global _gen
    if _gen is None:
        _gen = Generator()
    return _gen