from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import db
import sound
import os

app = Flask(__name__)
CORS(app)

# Initialize Database
db.init_db()

@app.route('/api/voices', methods=['GET'])
def get_voices():
    """Endpoint to list all available voices."""
    try:
        voices = sound.run_async(sound.SoundManager.get_all_voices())
        # Optionally filter or simplify the voice data
        formatted_voices = [
            {
                "shortName": v["ShortName"],
                "friendlyName": v["FriendlyName"],
                "locale": v["Locale"],
                "gender": v["Gender"]
            }
            for v in voices
        ]
        return jsonify(formatted_voices)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tts', methods=['POST'])
def create_tts():
    """Endpoint to generate TTS from text and voice."""
    data = request.json
    text = data.get('text')
    voice = data.get('voice')

    if not text or not voice:
        return jsonify({"error": "Missing text or voice parameter"}), 400

    try:
        file_path, filename = sound.run_async(sound.SoundManager.generate_tts(text, voice))
        
        # Log to database
        db.log_request(text, voice, file_path)
        
        return jsonify({
            "message": "TTS generated successfully",
            "filename": filename,
            "url": f"/audio/{filename}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    """Serve the Web UI."""
    return send_from_directory('static', 'index.html')

@app.route('/audio/<path:filename>')
def serve_audio(filename):
    """Serve the generated audio files."""
    return send_from_directory('static/audio', filename)

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get recent TTS request history."""
    try:
        history = db.get_recent_requests()
        formatted_history = [
            {
                "text": row[0],
                "voice": row[1],
                "file_path": row[2],
                "timestamp": row[3]
            }
            for row in history
        ]
        return jsonify(formatted_history)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Ensure the audio directory exists
    if not os.path.exists('static/audio'):
        os.makedirs('static/audio')
    
    port = int(os.environ.get("PORT", 80))
    app.run(host='0.0.0.0', port=port, debug=True)
