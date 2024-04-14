from pathlib import Path
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
import logging
import os
import openai

app = FastAPI()

load_dotenv()

# Set up CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],  # List of origins that are allowed to make requests
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Setup static files serving
app.mount(
    "/static",
    StaticFiles(directory="./mhacks/public"),
    name="static",
)

logging.basicConfig(level=logging.INFO)


class UserInput(BaseModel):
    company_name: str
    product_details: str
    organization_size: str
    product_differentiator: str


def setup_genai():
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        logging.error("Google API key is not set.")
        raise ValueError("Google API key is not set.")
    genai.configure(api_key=google_api_key)
    print("setup complete")
    return genai


def analyze_audio_ads(audio_ad_paths, genai_client):
    analysis_results = []
    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
    for path in audio_ad_paths:
        try:
            file_handle = genai_client.upload_file(path=path)
            prompt_summary = (
                "Listen carefully to the following audio file. Provide a brief summary."
            )
            prompt_sentiment = (
                "Listen carefully to the following audio file. Analyze the sentiment."
            )
            summary = model.generate_content([prompt_summary, file_handle])
            sentiment = model.generate_content([prompt_sentiment, file_handle])
            analysis_results.append((file_handle, summary.text, sentiment.text))
            logging.info(f"Audio analysis completed for: {path}")
        except Exception as e:
            logging.error(f"Error in audio ad analysis: {e}")

    return analysis_results


def generate_ad_script(analysis_results, context):
    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
    combined_context = "\n".join(
        f"Context: {context}, Summary: {summary}, Sentiment: {sentiment}"
        for _, summary, sentiment in analysis_results
    )
    prompt = f"Follow these instructions very closely: Generate an engaging audio ad script based \
on the provided context and audio analysis: '{combined_context}'. Provide only the narrator script."
    response = model.generate_content([prompt])
    return response.text


def text_to_speech(text, output_file):
    speech_file_path = Path(output_file).resolve()
    response = openai.audio.speech.create(
        model="tts-1-hd",
        voice="alloy",
        input=text,
    )
    with open(speech_file_path, "wb") as f:
        f.write(response.content)
    logging.info(f"Audio file generated and saved successfully: {speech_file_path}")


@app.post("/genad/")
async def genad(user_input: UserInput):
    try:
        audio_ad_paths = [
            "./assets/Apple_Ad_1.mp3",
            # "Apple_Ad_2.mp3",
            # "Radio_Shack_Ad.mp3",
        ]

        genai_client = setup_genai()

        context = (
            f"Introducing a new product from {user_input.company_name}, "
            f"designed for {user_input.product_details}. Our company size is "
            f"{user_input.organization_size} and we stand out by {user_input.product_differentiator}."
        )
        analysis_results = analyze_audio_ads(audio_ad_paths, genai_client)
        ad_script = generate_ad_script(analysis_results, context)

        return {"ad_script": ad_script}
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/getaudio/")
async def getaudio(ad_script: str):
    tts_output_path = "./mhacks/public/ad_script_audio.mp3"
    text_to_speech(ad_script, tts_output_path)
    return {"audio_path": "/public/ad_script_audio.mp3"}
