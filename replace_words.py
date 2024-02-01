
data = {
    "දීර්ග බෙදීම": "long division",
    "මගින්": "using it",
    "බහුපද": "polynomials",
    "ප්‍රකාශනයන්": "expressions",
    "ශේෂය": "remainder",
    "ලබ්ධිය": "quotient",
}

def main():
    prompt = "දීර්ග බෙදීම මගින් පහත බහුපද ඉදිරියෙන් දැක්වෙන ප්‍රකාශනයන් බෙදූ විට ලැබෙන ශේෂය හා ලබ්ධිය සොයන්න"
    for k, v in data.items():
            prompt = prompt.replace(k, v)
    print(prompt)
    
if __name__ == "__main__":
    main()
