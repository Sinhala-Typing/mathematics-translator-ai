import os
import logging
from dotenv import load_dotenv
from googletrans import Translator
from openai import OpenAI
import gradio as gr
import html

load_dotenv()

class MathQuestionTranslator:
    def __init__(self, openai_api_key):
        self.client = OpenAI(api_key=openai_api_key)
        self.data = {
            "දීර්ග බෙදීම": "long division",
            "මගින්": "using it",
            "බහුපද": "polynomials",
            "ප්‍රකාශනයන්": "expressions",
            "ශේෂය": "remainder",
            "ලබ්ධිය": "quotient",
        }
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
                        "content": f"**Math Question Correction:**\n\nPlease correct the following math question. The question is originally in Sinhala but has been translated into English. Ensure the grammar, syntax, and clarity of the question. Also, make sure the question has proper meaning. If there are any mathematical errors, correct them as well. Your response should be a properly formatted math question. (This is for Sri Lankan GCE Andvanced Level High School Examination). Dont add anything additional. This prompt might not include the questions, and it may be a part of a question, so, just keep that in mind. These are questions. Make sure the question makes sense. You may swap its order or order of words if needed.\n\n**Original Question (Translated from Sinhala):**\n\n\"{prompt}\"\n\n**Corrected Question:**\n\n",
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
            sanitized_prompt = html.escape(prompt)
            replaced = self.replace_words(sanitized_prompt)
            if replaced is None:
                return "Error occurred during word replacement."

            translated = self.translate_words(replaced)
            if translated is None:
                return "Error occurred during translation."

            fixed = self.ai(translated)
            if fixed is None:
                return "Error occurred during AI completion."

            return fixed
        except Exception as e:
            logging.error(f"Translation process failed: {e}")
            return "An error occurred."

openai_api_key = os.getenv("API_KEY")
translator = MathQuestionTranslator(openai_api_key)

iface = gr.Interface(
    fn=translator.translate_question,
    inputs="text", outputs="text",
    title="Sinhala Math Question to English Translator",
    description="Translate Sinhala math questions from Sinhala to English for Sri Lankan GCE Advanced Level Examination.",
    examples=[
        ["දීර්ග බෙදීම මගින් පහත බහුපද ඉදිරියෙන් දැක්වෙන ප්‍රකාශනයන් බෙදූ විට ලැබෙන ශේෂය හා ලබ්ධිය සොයන්න"]
    ],
    allow_flagging=True,
    flagging_dir="flagged",
    api_name="translate",
)
iface.launch()
