# Edge TTS Web Server

A simple Flask-based web server that provides Text-to-Speech (TTS) capabilities using Microsoft Edge's neural voices via the `edge-tts` library.

## Project Structure

- `app.py`: The Flask web server and API endpoints.
- `sound.py`: Logic for interacting with the `edge-tts` library.
- `db.py`: SQLite database logic for logging TTS requests.
- `static/audio/`: Directory where generated MP3 files are stored.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the server (Development):
   ```bash
   python app.py
   ```

3. Run the server (Production with Gunicorn):
   ```bash
   gunicorn -c gunicorn.conf.py wsgi:app
   ```

## Port 80 Note
**Important**: The application is configured to run on **Port 80**, which is the standard port for HTTP traffic. Binding to port 80 typically requires root/administrator privileges on the host machine. If you encounter permission errors, you may need to run with `sudo` or change the external port mapping in `docker-compose.yml`.

## Docker

1. Build and run with Docker Compose (includes MySQL):
   ```bash
   docker-compose up --build
   ```

2. The server will be accessible at `http://localhost:80`.

## Configuration
The application uses the following environment variables (defined in `docker-compose.yml` or a `.env` file):
- `DB_HOST`: MySQL host
- `DB_USER`: MySQL user
- `DB_PASSWORD`: MySQL password
- `DB_NAME`: MySQL database name

## API Endpoints

- `GET /api/voices`: Lists all available voices and languages.
- `POST /api/tts`: Generates a TTS audio file.
  - Body: `{"text": "Hello world", "voice": "en-US-JennyNeural"}`
- `GET /audio/<filename>`: Serves the generated audio file.
- `GET /api/history`: Returns the history of TTS requests.
