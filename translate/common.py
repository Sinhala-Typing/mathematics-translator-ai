import typing as t
import os
from openai import OpenAI
from utils import errors


class AI:
    def __init__(self, api_key: t.Optional[str] = os.getenv("API_KEY")) -> None:
        self.api_key = api_key
    
    def __init_client(self) -> None:
        try:
            self.client: OpenAI = OpenAI(api_key=self.api_key)
        except Exception as e:
            raise errors.AiError(f"An error has occured in `__init_client()`. Unable to Initialize the client. Exception: {e}")
    
    def __prompt_CustomAlgorithm(self) -> None:
        pass
    
    def translate(self, mode) -> None:
        pass
        