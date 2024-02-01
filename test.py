from openai import OpenAI
import os
from dotenv import load_dotenv
import requests

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
    for k,v in data.items():
        text = text.replace(k, v)
    return text


def ai(prompt:str):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"**Math Question Correction:**\n\nPlease correct the following math question. The question is originally in Sinhala but has been translated into English. Ensure the grammar, syntax, and clarity of the question. If there are any mathematical errors, correct them as well. Your response should be a properly formatted math question.\n\n**Original Question (Translated from Sinhala):**\n\n\"{prompt}\"\n\n**Corrected Question:**\n\n",
            }
        ],
        model="gpt-3.5-turbo",
    )

    print(chat_completion.choices[0].message.content)

def main():
    prompt = "දීර්ග බෙදීම මගින් පහත බහුපද ඉදිරියෙන් දැක්වෙන ප්‍රකාශනයන් බෙදූ විට ලැබෙන ශේෂය හා ලබ්ධිය සොයන්න"
    print(prompt)
    replaced = replace_words(text=prompt)
    print(replaced)
    translated = translate_words(replaced)
    print(translated)
    fixed = ai(translated)

if __name__ == "__main__":
    main()
