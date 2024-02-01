from openai import OpenAI
import os
from dotenv import load_dotenv
import requests
import gradio as gr

load_dotenv()

client = OpenAI(
    api_key=os.getenv("API_KEY"),
)

data = {
    "දීර්ග බෙදීම": "long division",
    "මගින්": "using it",
    "බහුපද": "polynomials",
    "ප්‍රකාශනයන්": "expressions",
    "ශේෂය": "remainder",
    "ලබ්ධිය": "quotient",
}


def translate_words(text: str):
    url = "http://127.0.0.1:5000/translate"
    payload = {"text": text}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        translated_text = response.json()["translated_text"]
        return translated_text
    else:
        print("Translation failed. Error:", response.text)
        return None


def replace_words(text: str):
    for k, v in data.items():
        text = text.replace(k, v)
    return text


def ai(prompt: str):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"**Math Question Correction:**\n\nPlease correct the following math question. The question is originally in Sinhala but has been translated into English. Ensure the grammar, syntax, and clarity of the question. Also, make sure the question has proper meaning. If there are any mathematical errors, correct them as well. Your response should be a properly formatted math question. (This is for Sri Lankan GCE Andvanced Level High School Examination). Dont add anything additional. This prompt might not include the questions, and it may be a part of a question, so, just keep that in mind. These are questions. Make sure the question makes sense. You may swap its order or order of words if needed.\n\n**Original Question (Translated from Sinhala):**\n\n\"{prompt}\"\n\n**Corrected Question:**\n\n",
            }
        ],
        model="gpt-4-0125-preview",
    )

    return chat_completion.choices[0].message.content


def main(prompt: str):
    replaced = replace_words(text=prompt)
    translated = translate_words(replaced)
    fixed = ai(translated)
    return fixed


iface = gr.Interface(
    fn=main, 
    inputs="text", outputs="text",
    title="Sinhala Math Question to English",
    theme="compact",
    description="Translate Sinhala math questions from Sinhala to English for Sri Lankan GCE Advanced Level Examination.",
    examples=[
        ["දීර්ග බෙදීම මගින් පහත බහුපද ඉදිරියෙන් දැක්වෙන ප්‍රකාශනයන් බෙදූ විට ලැබෙන ශේෂය හා ලබ්ධිය සොයන්න"]
    ]
)
iface.launch()
