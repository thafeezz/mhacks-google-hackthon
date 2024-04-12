import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]

genai.configure(api_key=GOOGLE_API_KEY)
dunkin_ad = genai.upload_file(path="assets/dunkin.mp3")

prompt = "Provide a summary transcript of the audio file."

model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
response = model.generate_content([prompt, dunkin_ad])

print(response.text)


"""
ideas:
    allow user to put some context for the ad to be generated
    "surprise me"

    simple UI
    maybe integrate 3rd party TTS after gemini gives us output
"""