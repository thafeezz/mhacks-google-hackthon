import google.generativeai as genai
from dotenv import load_dotenv
import os
import logging
import pandas as pd
import openai
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter import font as tkfont
import threading
import pygame

pygame.mixer.init()

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Set the OpenAI API key globally
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    logging.error("OpenAI API key is not set.")
    raise ValueError("OpenAI API key is not set.")

def setup_genai():
    # Retrieve your API key from environment variables
    google_api_key = os.getenv('GOOGLE_API_KEY')
    if not google_api_key:
        logging.error("Google API key is not set.")
        raise ValueError("Google API key is not set.")
    genai.configure(api_key=google_api_key)
    return genai

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
        prompt = f"Follow these instructions very closely: Generate an engaging audio ad script based \
            on the provided context and audio analysis: '{combined_context}'. Provide only the narrator script, do not not\
            include any reference to music or sounds, I only what what will be spoken by the narrator. Give me one solid script and\
            no other  alternatives."
        response = model.generate_content([prompt])
        return response.text
    except Exception as e:
        logging.error(f"Error generating ad script: {e}")
        raise
def text_to_speech(text, output_file):
    try:
        # Specify the path for the output audio file
        speech_file_path = Path(output_file).resolve()

        # Generate speech using the specified TTS model and voice
        response = openai.audio.speech.create(
            model="tts-1-hd",
            voice="alloy",
            input=text,
        )
        # Write the audio data to the file
        with open(speech_file_path, 'wb') as f:
            f.write(response.content)
        logging.info(f"Audio file generated and saved successfully: {speech_file_path}")

    except Exception as e:
        logging.error(f"Error generating audio file: {e}")
        raise


class AdGeneratorApp:
    def __init__(self, master):
        self.master = master
        master.title("Ad Generator")

        # Initialize player attributes
        self.player_initialized = False
        self.is_playing = False

        # Initialize the font for the inputs and buttons
        input_font = tkfont.Font(family="Helvetica", size=10)
        button_font = tkfont.Font(family="Helvetica", size=12, weight='bold')
        label_font = tkfont.Font(family="Helvetica", size=12, slant='italic')

        # Input fields with enhanced styling
        self.company_name_entry = tk.Entry(master, width=50, bg='lightgray', fg='black', font=input_font)
        self.company_name_entry.grid(row=0, column=1)
        tk.Label(master, text="Company Name and Background:", font=label_font).grid(row=0)

        self.product_details_entry = tk.Entry(master, width=50, bg='lightgray', fg='black', font=input_font)
        self.product_details_entry.grid(row=1, column=1)
        tk.Label(master, text="Product Details:", font=label_font).grid(row=1)

        self.organization_size_entry = tk.Entry(master, width=50, bg='lightgray', fg='black', font=input_font)
        self.organization_size_entry.grid(row=2, column=1)
        tk.Label(master, text="Organization Size:", font=label_font).grid(row=2)

        self.product_differentiator_entry = tk.Entry(master, width=50, bg='lightgray', fg='black', font=input_font)
        self.product_differentiator_entry.grid(row=3, column=1)
        tk.Label(master, text="Product Differentiator:", font=label_font).grid(row=3)

        # Buttons with enhanced styling
        self.generate_button = tk.Button(master, text="Generate Ad", command=self.generate_ad, bg='white', fg='black', font=button_font, activeforeground='black', activebackground='white')
        self.generate_button.grid(row=4, columnspan=2)

        self.play_button = tk.Button(master, text="Play/Pause Audio", command=self.play_pause_audio, state=tk.DISABLED, bg='white', fg='black', font=button_font, activeforeground='black', activebackground='white')
        self.play_button.grid(row=7, columnspan=2)

        # Status label with enhanced styling
        self.status_label = tk.Label(master, text="Ready", bg='lightblue', fg='black', font=label_font)
        self.status_label.grid(row=5, columnspan=2)

        # Output text area with enhanced styling
        text_font = tkfont.Font(family="Courier", size=12)  # Define a monospaced font for better alignment
        self.output_text = ScrolledText(master, height=10, width=60, wrap="word", font=text_font, bg='black', fg='white')
        self.output_text.grid(row=6, columnspan=2)

    def collect_inputs(self):
        return {
            "company_name": self.company_name_entry.get(),
            "product_details": self.product_details_entry.get(),
            "organization_size": self.organization_size_entry.get(),
            "product_differentiator": self.product_differentiator_entry.get()
        }
    def update_status(self, text):
        self.status_label.config(text=text)
        self.master.update()

    def generate_ad(self):
        self.update_status("Generating...")
        user_inputs = self.collect_inputs()
        threading.Thread(target=self.background_ad_generation, args=(user_inputs,)).start()

    def background_ad_generation(self, inputs):
        self.update_status("Processing inputs...")
        
        # Schedule an update to the status label after 5 seconds
        self.master.after(5000, self.update_status, "Training Gemini on classic ads...")
        
        context = (
            f"Introducing a new product from {inputs['company_name']}, "
            f"designed for {inputs['product_details']}. Our company size is "
            f"{inputs['organization_size']} and we stand out by {inputs['product_differentiator']}."
        )

        # Setup Google generative AI client
        genai_client = setup_genai()

        # File paths for example, update these to where your audio files are stored or how they are generated
        audio_ad_paths = ["/Users/numan/Library/CloudStorage/OneDrive-Personal/GooglexMHacks/mhacks-google-hackthon/assets/Apple_Ad_1.mp3"]

        try:
            # Analyze the audio ads to incorporate their analysis into the ad script generation
            analysis_results = analyze_audio_ads(audio_ad_paths, genai_client)
            
            # Generate the ad script using the analysis results and the user-provided context
            ad_script = generate_ad_script(analysis_results, context)

            # Display the generated ad script in the text area
            self.output_text.insert(tk.END, ad_script)
            self.update_status("Ad script generation complete.")

            # Schedule an update to the status label before generating audio
            self.master.after(0, self.update_status, "Generating audio...")

            # Generate audio from the ad script
            tts_output_path = "/Users/numan/Library/CloudStorage/OneDrive-Personal/GooglexMHacks/mhacks-google-hackthon/ad_audio.mp3"
            text_to_speech(ad_script, tts_output_path)

            # Enable the play button and store the path to the generated audio for playback
            self.generated_audio_path = tts_output_path
            self.play_button.config(state=tk.NORMAL)
            self.update_status("Ad generation complete.")
        except Exception as e:
            self.update_status("Failed to generate ad.")
            logging.error(f"Error in ad generation process: {e}")
            messagebox.showerror("Error", "Failed to generate ad. Please check the logs for more information.")


    def play_pause_audio(self):
        if not self.player_initialized:
            pygame.mixer.music.load(self.generated_audio_path)
            pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Set an event to trigger at the end of the audio
            self.player_initialized = True

        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
            self.play_button.config(text="Play Audio")
        else:
            pygame.mixer.music.play()
            self.is_playing = True
            self.play_button.config(text="Pause Audio")
            self.monitor_audio()

    def monitor_audio(self):
        """ Monitor the state of the audio to stop it when finished. """
        if pygame.mixer.music.get_busy():  # Check if the music stream is playing
            self.master.after(100, self.monitor_audio)  # Recheck after 100ms
        else:
            self.audio_finished()

    def audio_finished(self):
        """ Handle audio finishing playback. """
        self.is_playing = False
        self.play_button.config(text="Play Audio")
        messagebox.showinfo("Playback Finished", "The audio ad has finished playing.")


# Create the main window and pass it to the AdGeneratorApp
root = tk.Tk()
app = AdGeneratorApp(root)
root.mainloop()
