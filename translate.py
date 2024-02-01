from flask import Flask, request, jsonify
from googletrans import Translator

app = Flask(__name__)

def translate_text(text, target_language='en'):
    translator = Translator()
    translation = translator.translate(text, src='si', dest=target_language)
    return translation.text

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    if 'text' not in data:
        return jsonify({'error': 'Missing text parameter'}), 400
    
    text = data['text']
    translated_text = translate_text(text)
    
    return jsonify({'translated_text': translated_text})

if __name__ == '__main__':
    app.run(debug=True)
