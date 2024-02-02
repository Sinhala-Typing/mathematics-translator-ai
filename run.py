#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import typing as t

import html
import gradio as gr
from dotenv import load_dotenv
from googletrans import Translator
from openai import OpenAI

# Parse a .env file and then load all the variables found as environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# -----
# OpenAI API Key, get yours here: https://platform.openai.com/api-keys
# -----
openai_api_key: t.Optional[str] = os.getenv("API_KEY")

# -----
# Support Functions
# -----
def load_data() -> t.Dict[str, str]:
    """
    Load data for the program.

    This function should be replaced by the user to suit their needs.
    According to the default config, this function should not take in any parameters.
    This function must return a dictionary data type for the program to work.

    Returns:
        dict: A dictionary containing data for the program.
            Keys are Sinhala phrases and values are their corresponding English translations.
    """
    data: t.Dict[str, str] = {
            "දීර්ග බෙදීම": "long division",
            "මගින්": "using it",
            "බහුපද": "polynomials",
            "ප්‍රකාශනයන්": "expressions",
            "ශේෂය": "remainder",
            "ලබ්ධිය": "quotient",
        }
    return data


def load_prompt_custom_algorithm() -> str:
    """
    Generate a prompt for the AI model.

    This function generates a prompt to be used by the AI model for correcting math questions.
    The prompt includes instructions for correcting the question, as well as placeholders for the original and corrected questions.
    The functionality of this function may be replaced by the user if needed to customize the prompt.

    Returns:
        str: A string containing the prompt for the AI model.    
    """
    txt: str = "**Math Question Correction:**\n\n " 
    txt += "Please correct the following math question. "
    txt += "The question is originally in Sinhala but has been translated into English. "
    txt += "Ensure the grammar, syntax, and clarity of the question. "
    txt += "Also, make sure the question has proper meaning. "
    txt += "If there are any mathematical errors, correct them as well. "
    txt += "Your response should be a properly formatted math question. "
    txt += "(This is for Sri Lankan GCE Andvanced Level High School Examination). "
    txt += "Dont add anything additional. "
    txt += "This prompt might not include the questions, and it may be a part of a question, so, just keep that in mind. "
    txt += "These are questions. Make sure the question makes sense. "
    txt += "You may swap its order or order of words if needed."
    txt +=  "\n\n**Original Question (Translated from Sinhala):**\n\n"
    txt += "\"{prompt}\""
    txt += "\n\n**Corrected Question:**\n\n"
    return txt


def load_prompt_full_ai() -> str:
    global data
    txt: str = "**Math Question Translation from Sinhala to English:**\n\n " 
    txt += "Please translate the following math question. Dont refer to the chat history. Treat this as a completely new question. "
    txt += "These are the special translations to remember when translating:\n"
    for k,v in data.items():
        txt += f"{k} means: {v}"
    txt += "\n\n"
    txt += "Ensure the grammar, syntax, and clarity of the question. "
    txt += "Also, make sure the question has proper meaning. "
    txt += "If there are any mathematical errors, correct them as well. "
    txt += "Your response should be a properly formatted math question. "
    txt += "(This is for Sri Lankan GCE Andvanced Level High School Examination). "
    txt += "Dont add anything additional. "
    txt += "This prompt might not include the questions, and it may be a part of a question, so, just keep that in mind. "
    txt += "These are questions. Make sure the question makes sense. "
    txt += "You may swap its order or order of words if needed."
    txt +=  "\n\n**Original Question (Translated from Sinhala):**\n\n"
    txt += "\"{prompt}\""
    txt += "\n\n**Corrected Question:**\n\n"
    return txt

# -----
# Program Code
# -----
client: OpenAI = OpenAI(api_key=openai_api_key)

data: t.Dict[str, str] = load_data()


def reload_data():
    global data
    data = load_data()
    
    
def replace_words(text: str) -> t.Optional[str]:
    """
    Stage 1 of Translation: Replace Sinhala words in the given text with their corresponding English translations.
    Used only in "Custom Algorithm" approach.
    
    Args:
        text (str): The input text containing Sinhala words to be replaced.

    Returns:
        Optional[str]: The input text with Sinhala words replaced by their English translations, or None if an error occurs.

    Raises:
        Any Exception: If an error occurs during the replacement process.

    Notes:
        - This function iterates through the items in the `data` dictionary, where keys are Sinhala phrases and values are their English translations.
        - Each Sinhala phrase found in the input `text` is replaced with its corresponding English translation.
    """
    try:
        for k, v in data.items():
            text = text.replace(k, v)
        return text
    except Exception as e:
        logging.error(f"Word replacement failed: {e}")
        return None
    
    
def translate_words(text: str) -> t.Optional[str]:
    """
    Stage 2 of Translation: Translate Sinhala text to English using Google Translate.
    Used only in "Custom Algorithm" approach.

    Args:
        text (str): The input Sinhala text to be translated.

    Returns:
        Optional[str]: The translated English text, or None if an error occurs.

    Raises:
        Any Exception: If an error occurs during the translation process.

    Notes:
        - This function uses the Google Translate API through the `googletrans-py` library.
        - The input `text` is translated from Sinhala (`src='si'`) to English (`dest='en'`).
        - The translated text is returned.
    """
    try:
        translator = Translator()
        translation = translator.translate(text, src='si', dest='en')
        return translation.text
    except Exception as e:
        logging.error(f"Translation failed: {e}")
        return None
 

def ai(prompt: str, mode: t.Literal["full_ai", "custom_algorithm"] = "full_ai") -> t.Optional[str]:
    """
    Perform AI-based correction of a math question.

    Args:
        prompt (str): The input math question in Sinhala Unicode.
        mode (Literal["full_ai", "custom_algorithm"], optional): The mode of operation.
            Either "full_ai" or "custom_algorithm". Defaults to "full_ai".

    Returns:
        Optional[str]: The corrected math question in English, or None if an error occurs.

    Raises:
        ValueError: If the mode is not one of "full_ai" or "custom_algorithm".
        Any Exception: If an error occurs during the AI completion process.

    Notes:
        - This function uses the OpenAI API to generate a corrected version of the input math question.
        - The input `prompt` is included in a formatted string to create a prompt for the AI model.
        - The completion generated by the AI model is returned as the corrected math question in English.
    """
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content":  load_prompt_full_ai().format(prompt=prompt) if mode == "full_ai" else  load_prompt_custom_algorithm().format(prompt=prompt)
                }
            ],
            # model="gpt-4-0125-preview",
            model="gpt-3.5-turbo-0125",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        logging.error(f"AI completion failed: {e}")
        return None


def custom_approach(prompt: str) -> str:
    try:
        reload_data()

        sanitized_prompt: str = html.escape(prompt)
        
        replaced: t.Optional[str] = replace_words(text=sanitized_prompt)
        if replaced is None:
            return "Error occurred during word replacement."
        
        translated: t.Optional[str] = translate_words(replaced)
        if translated is None:
            return "Error occurred during translation."
        
        fixed: t.Optional[str] = ai(translated, mode="custom_algorithm")
        if fixed is None:
            return "Error occurred during AI completion."
        
        return fixed
    
    except Exception as e:
        logging.error(f"Custom Approach failed: {e}")
        return "An error occurred."


def full_ai_approach(prompt) -> str:
    try:
        reload_data()

        sanitized_prompt: str = html.escape(prompt)
        fixed: t.Optional[str] = ai(sanitized_prompt, mode="full_ai")
        if fixed is None:
            return "Error occurred during AI completion."
        
        return fixed
    
    except Exception as e:
        logging.error(f"Custom Approach failed: {e}")
        return "An error occurred."


def main(prompt: str, algorithm: str) -> t.Optional[str]:
    """
    Translate a math question from Sinhala to English using the selected algorithm.

    Args:
        prompt (str): The original math question in Sinhala.
        algorithm (str): The selected algorithm ('Custom Algorithm' or 'Full AI Translation').

    Returns:
        Optional[str]: The corrected math question in English, or None if an error occurs.
    """
    if algorithm == "Custom Algorithm":
        return custom_approach(prompt)
    elif algorithm == "Full AI Translation":
        return full_ai_approach(prompt)
    else:
        return None

iface: gr.Interface = gr.Interface(
    fn=main, 
    inputs=["text", gr.Radio(["Custom Algorithm", "Full AI Translation"], label="Select Algorithm")],
    outputs="text",
    title="Sinhala Math Question to English Translator",
    description="Translate Sinhala math questions from Sinhala to English for Sri Lankan GCE Advanced Level Examination.",
    examples=[
        ["දීර්ග බෙදීම මගින් පහත බහුපද ප්‍රකාශනයන් බෙදූ විට ලැබෙන ශේෂය හා ලබ්ධිය සොයන්න"]
    ],
    # allow_flagging=True,
    flagging_dir="flagged",
    api_name="translate",
)
iface.launch()
