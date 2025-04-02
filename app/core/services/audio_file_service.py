import base64

class AudioServive:
    def save_audio_file(audio_file_base64: str, filename: str):
        audio_bytes = base64.b64decode(audio_file_base64)
        with open(filename, "wb") as f:
            f.write(audio_bytes)
