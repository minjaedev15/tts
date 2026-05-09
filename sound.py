import edge_tts
import asyncio
import os
import uuid

class SoundManager:
    @staticmethod
    async def get_all_voices():
        """Lists all available voices from edge-tts."""
        voices = await edge_tts.VoicesManager.create()
        return voices.voices

    @staticmethod
    async def generate_tts(text, voice, output_dir="static/audio"):
        """Generates a TTS file and returns the file path."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        filename = f"{uuid.uuid4()}.mp3"
        file_path = os.path.join(output_dir, filename)
        
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(file_path)
        
        return file_path, filename

def run_async(coro):
    """Utility to run async functions in a synchronous context."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()
