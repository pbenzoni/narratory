from flask import Flask, render_template, request, Response, redirect, url_for
from flask_sse import sse
import io
import wave
import os
import requests
from bs4 import BeautifulSoup
from piper.voice import PiperVoice
import numpy as np
import sounddevice as sd
import base64

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost:6379/0"
app.register_blueprint(sse, url_prefix='/stream')

# Load the PiperVoice model
voicedir = os.path.expanduser('./')  # Where onnx model files are stored on your machine
model = voicedir + "alba.onnx"
voice = PiperVoice.load(model)

def load_text_from_royal_road(text_url):
    response = requests.get(text_url)
    text = response.text
    text = text.split('<div class="chapter-inner chapter-content">')[1]
    text = text.split('<div class="portlet')[0]
    soup = BeautifulSoup(text, "html.parser")
    return soup.text

def load_text_from_ao3(text_url):
    response = requests.get(text_url)
    text = response.text
    text = text.split('<h3 class="landmark heading" id="work">Chapter Text</h3>')[1]
    text = text.split('<div id="feedback" class="feedback">')[0]
    soup = BeautifulSoup(text, "html.parser")
    return soup.text

def clean_and_split_text(text):
    # Split text by newline and remove empty lines
    lines = text.split('\n')
    return [line.strip() for line in lines if line.strip()]

def generate_audio_in_chunks(text):
    """Generate a stream of raw audio data from the TTS model."""
    for line in clean_and_split_text(text):
            buffer = io.BytesIO()
            with wave.open(buffer, "wb") as wav_file:
                wav_file.setnchannels(1)  # Set number of channels (1 for mono, 2 for stereo)
                wav_file.setsampwidth(2)  # Set sample width in bytes (2 for 16-bit audio)
                wav_file.setframerate(24000)  # Set the frame rate (sample rate)
                voice.synthesize(line, wav_file)
            buffer.seek(0)
            
            # Encode the audio chunk in Base64
            chunk = buffer.read()
            encoded_chunk = base64.b64encode(chunk).decode('utf-8')
            
            yield encoded_chunk

        
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/audio')
def stream_audio():
    url = request.args.get('url')
    source = request.args.get('source')
    
    if 'royalroad' in source.lower():
        text = load_text_from_royal_road(url)
    elif 'ao3' in source.lower():
        text = load_text_from_ao3(url)
    else:
        text = "Invalid source selected."
    
    def stream():
        for chunk in generate_audio_in_chunks(text):
            yield f"data: {chunk}\n\n"
    
    return Response(stream(), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
