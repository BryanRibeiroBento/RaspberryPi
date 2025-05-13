import os
import sys
import time
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio  # uso direto do backend

# === Força ALSA como driver de áudio (caso necessário) ===
os.environ["SDL_AUDIODRIVER"] = "alsa"

# === Caminho do arquivo de áudio ===
base_dir = os.path.dirname(__file__)
audio_path = os.path.join(base_dir, "jazz.wav")

# === Função para tocar a música ===
def tocar_musica():
    try:
        print("🔊 Carregando áudio...")
        som = AudioSegment.from_wav(audio_path)
        print(f"✅ Áudio carregado ({len(som)} ms)")
        print("▶️ Tocando áudio...")
        playback = _play_with_simpleaudio(som)
        playback.wait_done()
        print("✅ Reprodução finalizada.")
    except Exception as e:
        print(f"❌ Erro ao tocar áudio: {e}")

# === Executa ===
if __name__ == "__main__":
    tocar_musica()