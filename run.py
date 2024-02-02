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

# -----
# OpenAI API Key, get yours here: https://platform.openai.com/api-keys
# -----
openai_api_key = os.getenv("API_KEY")

# -----
# Support Functions
# -----
def load_data() -> t.Dict[str,str]:
    """
    Load data for the program.

    This function should be replaced by the user to suit their needs.
    According to the default config, this function should not take in any parameters.
    This function must return a dictionary data type for the program to work.

    Returns:
        dict: A dictionary containing data for the program.
            Keys are Sinhala phrases and values are their corresponding English translations.
    """
    data = {
            "දීර්ග බෙදීම": "long division",
            "මගින්": "using it",
            "බහුපද": "polynomials",
            "ප්‍රකාශනයන්": "expressions",
            "ශේෂය": "remainder",
            "ලබ්ධිය": "quotient",
        }
    return data

def load_prompt() -> str:
    return "**Math Question Correction:**\n\nPlease correct the following math question. The question is originally in Sinhala but has been translated into English. Ensure the grammar, syntax, and clarity of the question. Also, make sure the question has proper meaning. If there are any mathematical errors, correct them as well. Your response should be a properly formatted math question. (This is for Sri Lankan GCE Andvanced Level High School Examination). Dont add anything additional. This prompt might not include the questions, and it may be a part of a question, so, just keep that in mind. These are questions. Make sure the question makes sense. You may swap its order or order of words if needed.\n\n**Original Question (Translated from Sinhala):**\n\n\"{prompt}\"\n\n**Corrected Question:**\n\n"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MathQuestionTranslator:
    def __init__(self, openai_api_key):
        self.client = OpenAI(api_key=openai_api_key)
        self.data = None

    def load_data(self):
        self.data = load_data()
    
    def translate_words(self, text):
        try:
            translator = Translator()
            translation = translator.translate(text, src='si', dest='en')
            return translation.text
        except Exception as e:
            logging.error(f"Translation failed: {e}")
            return None

    def replace_words(self, text):
        try:
            for k, v in self.data.items():
                text = text.replace(k, v)
            return text
        except Exception as e:
            logging.error(f"Word replacement failed: {e}")
            return None

    def ai(self, prompt):
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": load_prompt().format(prompt=prompt),
                    }
                ],
                model="gpt-4-0125-preview",
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            logging.error(f"AI completion failed: {e}")
            return None

    def translate_question(self, prompt):
        try:
            replaced = self.replace_words(prompt)
            if replaced is None:
                return "Error occurred during Stage 1: word replacement."

            translated = self.translate_words(replaced)
            if translated is None:
                return "Error occurred during Stage 2: translation."

            fixed = self.ai(translated)
            if fixed is None:
                return "Error occurred during Stage 3: AI completion."

            return fixed
        except Exception as e:
            logging.error(f"Translation process failed: {e}")
            return "An error occurred."

translator = MathQuestionTranslator(openai_api_key)

iface = gr.Interface(
    fn=translator.translate_question,
    inputs="text", outputs="text",
    title="Sinhala Math Question to English Translator",
    description="Translate Sinhala math questions from Sinhala to English for Sri Lankan GCE Advanced Level Examination.",
    examples=[
        ["දීර්ග බෙදීම මගින් පහත බහුපද ඉදිරියෙන් දැක්වෙන ප්‍රකාශනයන් බෙදූ විට ලැබෙන ශේෂය හා ලබ්ධිය සොයන්න"]
    ],
    api_name="translate",
)
iface.launch()
