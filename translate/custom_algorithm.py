import typing as t
import os
from utils import errors
from googletrans import Translator

class CustomAlgorithm:
    def __init__(self, 
                 question: str, 
                 translation_data: t.Dict[str,str],
                 api_key: t.Optional[str] = os.getenv("API_KEY"),
                 ) -> None:
        self.api_key = api_key
        self.question = question
        self.translation_data = translation_data
    
    def __replace_words_translation(self) -> None:
        try:
            for k, v in self.translation_data.items():
                self.question = self.question.replace(k, v)
        except Exception as e:
            raise errors.CustomApproachError(f"An error occured in `__replace_words_translation()`: {e}")
    
    def __google_translate_words(self) -> None:
        try:
            translator = Translator()
            translation = translator.translate(self.question, src='si', dest='en')
            self.question = translation.text
        except Exception as e:
            raise errors.CustomApproachError(f"An error occured in `__google_translate_words()`: {e}")
    
    def __ai(self) -> None:
        try:
            ...
        except Exception as e:
            ...