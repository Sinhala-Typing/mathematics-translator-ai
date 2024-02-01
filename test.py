from openai import OpenAI
import os
from dotenv import load_dotenv

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

def replace_words(text: str):
    for k,v in data.items():
        if k in text:
            text.replace(k, v)
    return 

def ai():
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "What is the circumference of the moon in km?",
            }
        ],
        model="gpt-3.5-turbo",
    )

    print(chat_completion)

def main():
    prompt = "දීර්ග බෙදීම මගින් පහත බහුපද ඉදිරියෙන් දැක්වෙන ප්‍රකාශනයන් බෙදූ විට ලැබෙන ශේෂය හා ලබ්ධිය සොයන්න"
    replaced = replace_words(text=prompt)
    print(replaced)

if __name__ == "__main__":
    main()
