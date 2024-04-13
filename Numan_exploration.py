import google.generativeai as genai
from dotenv import load_dotenv
import os
import logging
import pandas as pd
import openai

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

def setup_genai():
    # Retrieve your API key from environment variables
    google_api_key = os.getenv('GOOGLE_API_KEY')
    if not google_api_key:
        logging.error("Google API key is not set.")
        raise ValueError("Google API key is not set.")
    genai.configure(api_key=google_api_key)
    return genai

def get_user_input():
    company_name = input("What is your company name and what does it do? ")
    product_details = input("What is the product you are selling and what does it do? ")
    organization_size = input("How large is your organization? ")
    product_differentiator = input("What is one differentiator for your product compared to the marketplace? ")
    
    return {
        "company_name": company_name,
        "product_details": product_details,
        "organization_size": organization_size,
        "product_differentiator": product_differentiator
    }

def analyze_audio_ads(audio_ad_paths, genai_client):
    analysis_results = []
    model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
    for path in audio_ad_paths:
        try:
            file_handle = genai_client.upload_file(path=path)
            prompt_summary = "Listen carefully to the following audio file. Provide a brief summary."
            prompt_sentiment = "Listen carefully to the following audio file. Analyze the sentiment."
            summary = model.generate_content([prompt_summary, file_handle])
            sentiment = model.generate_content([prompt_sentiment, file_handle])
            analysis_results.append((file_handle, summary.text, sentiment.text))
            logging.info(f"Audio analysis completed for: {path}")
        except Exception as e:
            logging.error(f"Error in audio ad analysis: {e}")
    return analysis_results

def generate_ad_script(analysis_results, context):
    genai_client = setup_genai()
    model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
    try:
        combined_context = "\n".join(
            f"Context: {context}, Summary: {summary}, Sentiment: {sentiment}"
            for _, summary, sentiment in analysis_results
        )
        prompt = f"Generate an engaging audio ad script based on the provided context and audio analysis: '{combined_context}'. Provide only the narrator script, do not not\
        include any reference to music or sounds, I only what what will be spoken."
        response = model.generate_content([prompt])
        return response.text
    except Exception as e:
        logging.error(f"Error generating ad script: {e}")
        raise

def save_ad_script(ad_script, output_path):
    try:
        with open(output_path, 'w') as f:
            f.write(ad_script)
        logging.info(f"Ad script saved successfully: {output_path}")
    except Exception as e:
        logging.error(f"Error saving ad script: {e}")
        raise

def text_to_speech(text, output_file):
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            logging.error("OpenAI API key is not set.")
            raise ValueError("OpenAI API key is not set.")
        
        speech_file_path = Path(__file__).parent / output_file
        response = openai.Audio.create(
            model="tts-1-hd",  # Ensure you have access to this model or change as necessary
            voice="alloy",
            input=text,
            output_format="mp3"
        )
        with open(speech_file_path, 'wb') as f:
            f.write(response.data)
        logging.info(f"Audio file generated and saved successfully: {speech_file_path}")
    except Exception as e:
        logging.error(f"Error generating audio file: {e}")
        raise


if __name__ == "__main__":
    user_responses = get_user_input()
    context = (
        f"Introducing a new product from {user_responses['company_name']}, "
        f"designed for {user_responses['product_details']}. Our company size is "
        f"{user_responses['organization_size']} and we stand out by {user_responses['product_differentiator']}."
    )

    audio_ad_paths = ["/Users/numan/Library/CloudStorage/OneDrive-Personal/Google x MHacks/mhacks-google-hackthon/Apple_Ad_1.mp3", "/Users/numan/Library/CloudStorage/OneDrive-Personal/Google x MHacks/mhacks-google-hackthon/Apple_Ad_2.mp3", "/Users/numan/Library/CloudStorage/OneDrive-Personal/Google x MHacks/mhacks-google-hackthon/Radio_Shack_ad.mp3"]
    genai_client = setup_genai()
    analysis_results = analyze_audio_ads(audio_ad_paths, genai_client)
    
    ad_script = generate_ad_script(analysis_results, context)
    print("Generated Ad Script:")
    print(ad_script)
    
    output_path = "generated_ad_script.txt"
    save_ad_script(ad_script, output_path)
    
    tts_output_path = "ad_script_audio.mp3"
    text_to_speech(ad_script, tts_output_path)