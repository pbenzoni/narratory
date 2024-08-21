 Audio Streaming Web App

This project allows you to stream text-to-speech (TTS) generated audio from websites like Royal Road and AO3. The audio is streamed to the frontend in chunks and can be controlled using Play, Pause, and Resume buttons.

## Features

- Stream text-to-speech generated audio from Royal Road or AO3.
- Control audio playback with Play, Pause, and Resume buttons.
- Bootstrap-styled frontend for a clean and responsive user interface.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/audio-streaming-app.git
cd audio-streaming-app
```

### 2. Set Up a Python Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

Make sure you have the `piper` TTS engine installed, and download the necessary voice models to the specified directory. 

### 4. Set Up the Voice Model

Ensure you have the PiperVoice model in the specified directory:

```plaintext
~/
  └── piper/
      └── cori.onnx  # Your TTS voice model file
```

### 5. Run the Application

Run the Flask app:

```bash
python app.py
```

By default, the app will be available at `http://0.0.0.0:80`.

## Usage

### 1. Start the Application

Navigate to `http://0.0.0.0` (or `http://localhost` if using a local setup) in your web browser.

### 2. Input URL and Select Source

- Enter the URL of the text you want to convert to audio.
- Select the source (`Royal Road` or `AO3`).

### 3. Control Audio Playback

- **Start Streaming:** Click the "Start Streaming" button to begin the audio stream.
- **Pause:** Click the "Pause" button to pause the audio.
- **Resume:** Click the "Resume" button to continue playing the audio from where it was paused.

## Dependencies

- Flask
- Flask-SocketIO
- PiperVoice (and the associated voice models)
- BeautifulSoup4 (for web scraping)
- Requests
- Bootstrap (via CDN)

## Known Issues

- Ensure that the URLs provided are correct and that the source selected matches the content structure.
- Large texts may take longer to process and stream.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any features, improvements, or bug fixes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
