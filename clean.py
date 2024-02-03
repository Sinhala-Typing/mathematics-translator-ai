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

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
openai_api_key: t.Optional[str] = os.getenv("API_KEY")

def load_data() -> t.Dict[str, str]:
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



client: OpenAI = OpenAI(api_key=openai_api_key)
data: t.Dict[str, str] = load_data()


def reload_data():
    global data
    data = load_data()
    
    
def replace_words(text: str) -> t.Optional[str]:
    try:
        for k, v in data.items():
            text = text.replace(k, v)
        return text
    except Exception as e:
        logging.error(f"Word replacement failed: {e}")
        return None
    
    
def translate_words(text: str) -> t.Optional[str]:
    try:
        translator = Translator()
        translation = translator.translate(text, src='si', dest='en')
        return translation.text
    except Exception as e:
        logging.error(f"Translation failed: {e}")
        return None
 

def ai(prompt: str, mode: t.Literal["full_ai", "custom_algorithm"] = "full_ai", model: str = "gpt-3.5-turbo-0125") -> t.Optional[str]:
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content":  load_prompt_full_ai().format(prompt=prompt) if mode == "full_ai" else  load_prompt_custom_algorithm().format(prompt=prompt)
                }
            ],
            model=model,
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


def main(prompt: str, algorithm: str, model: str) -> t.Optional[str]:
    if algorithm == "Custom Algorithm":
        return custom_approach(prompt)
    elif algorithm == "Full AI Translation":
        return full_ai_approach(prompt)
    else:
        return None


iface: gr.Interface = gr.Interface(
    fn=main, 
    inputs=["text", gr.Radio(["Custom Algorithm", "Full AI Translation"], label="Select Algorithm"), gr.Radio(["gpt-3.5-turbo-0125", "gpt-4-0125-preview"], label="Select Model")],
    outputs="text",
    title="Sinhala Math Question to English Translator",
    description="Translate Sinhala math questions from Sinhala to English for Sri Lankan GCE Advanced Level Examination.",
    examples=[
        ["දීර්ග බෙදීම මගින් පහත බහුපද ප්‍රකාශනයන් බෙදූ විට ලැබෙන ශේෂය හා ලබ්ධිය සොයන්න"]
    ],
    flagging_dir="flagged",
    api_name="translate",
)
iface.launch()
