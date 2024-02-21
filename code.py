!pip install openai==0.27.0 gtts googletrans==4.0.0-rc1
!apt-get install -y python3-pyaudio
!pip install SpeechRecognition

from gtts import gTTS
from IPython.display import Audio, display
import openai
from googletrans import Translator

# Set your OpenAI API key
openai.api_key = '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'  # Insert your OpenAI API key here

# Function to translate text to English
def translate_to_english(text):
    translator = Translator()
    translated_text = translator.translate(text, dest='en')
    return translated_text.text

# Function to translate text to the desired language
def translate_to_lang(text, dest_lang):
    translator = Translator()
    translated_text = translator.translate(text, dest=dest_lang)
    return translated_text.text

# Function to generate response using GPT-3
def generate_response(prompt, input_lang, output_lang):
    translated_prompt = translate_to_lang(prompt, 'en') if input_lang != 'en' else prompt
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": translated_prompt},
        ]
    )
    generated_response = response['choices'][0]['message']['content'].strip()
    return translate_to_lang(generated_response, output_lang)

# Function to convert text to speech
def text_to_speech(text, lang):
    tts = gTTS(text, lang=lang)
    tts.save("output.mp3")
    display(Audio("output.mp3", autoplay=True))

# Function to ask for output choice
def ask_for_output_choice():
    choice = input("Do you want the output as text or speech? (text/speech): ").lower()
    while choice not in ['text', 'speech']:
        print("Invalid choice. Please choose either 'text' or 'speech'.")
        choice = input("Do you want the output as text or speech? (text/speech): ").lower()
    return choice

# Supported languages
supported_languages = {
    'en': 'English',
    'hi': 'Hindi',
    'ta': 'Tamil',
    'te': 'Telugu',
    'mr': 'Marathi',
    'bn': 'Bengali',
    'gu': 'Gujarati',
    'ur': 'Urdu',
    'pa': 'Punjabi',
    'ml': 'Malayalam',
    'or': 'Odia',
    'kn': 'Kannada',  
    'as': 'Assamese',  
    'kok': 'Konkani',  
    'ne': 'Nepali',  
    'sd': 'Sindhi',  
    'mni': 'Manipuri',  
    'doi': 'Dogri', 
    'mai': 'Maithili', 
    'bho': 'Bhojpuri', 
    'sat': 'Santali', 
    'ks': 'Kashmiri',  
    'chr': 'Chhattisgarhi',  
    'new': 'Newari',  
    'awa': 'Awadhi', 
}

# Display supported languages
print("Supported languages:")
for code, language in supported_languages.items():
    print(f"{code}: {language}")

# Ask for input language selection
input_lang = input("Choose your input language: ").lower()
while input_lang not in supported_languages:
    print("Invalid language code. Please choose from the following:")
    for code, language in supported_languages.items():
        print(f"{code}: {language}")
    input_lang = input("Choose your input language: ").lower()

# Ask for output language selection
output_lang = input("Choose your output language: ").lower()
while output_lang not in supported_languages:
    print("Invalid language code. Please choose from the following:")
    for code, language in supported_languages.items():
        print(f"{code}: {language}")
    output_lang = input("Choose your output language: ").lower()

# Main loop
while True:
    user_input = input("How can I assist you today? ")

    chatgpt_response = generate_response(user_input, input_lang, output_lang)
    output_choice = ask_for_output_choice()

    if output_choice == 'text':
        print(chatgpt_response)
    else:
        text_to_speech(chatgpt_response, output_lang)

    user_choice = input("Do you want to ask something else? (yes/no) ").lower()
    if user_choice != 'yes':
        break
