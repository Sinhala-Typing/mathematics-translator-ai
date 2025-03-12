# Maths Jargon Sinhala to English Translator

![math-transltaor](https://github.com/user-attachments/assets/9e222702-f509-460e-8f75-31759f61d34d)


This repository contains code for a Sinhala to English translator specifically designed for translating math jargon used in Sri Lankan GCE Advanced Level Examination questions. The translator aims to provide accurate translations of math-related terms and questions from Sinhala to English, facilitating understanding and communication for students and educators.

## Features

- **Custom Algorithm and Full AI Translation**: The translator offers two modes: "Custom Algorithm" and "Full AI Translation." Users can choose between these modes based on their preferences and requirements.
- **Custom Algorithm**: This mode utilizes a custom algorithm to replace Sinhala words with their corresponding English translations and then translates the entire text using Google Translate.
- **Full AI Translation**: This mode employs advanced AI models, such as GPT-3.5 Turbo and GPT-4, for direct translation from Sinhala to English without intermediate processing.

- **Interactive Web Interface**: The translator is accessible via a user-friendly web interface powered by Gradio, allowing users to input Sinhala math questions and receive translated outputs.

## Usage

1. **Input Sinhala Math Question**: Enter a Sinhala math question into the provided text input field on the web interface.
2. **Select Translation Mode**: Choose between "Custom Algorithm" and "Full AI Translation" using the radio buttons.
3. **Select AI Model**: Optionally, select the AI model to be used for translation (e.g., GPT-3.5 Turbo or GPT-4).
4. **View Translated Output**: The translated English version of the math question will be displayed as output on the web interface.

## Installation and Setup

To set up the translator locally, follow these steps:

1. Clone the repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Ensure that you have an API key for the OpenAI platform and Google Cloud Translation API, if necessary. Set these API keys as environment variables.
4. Run the main script (`app.py`) to launch the web interface.
5. Access the translator by navigating to the provided URL in your web browser.

