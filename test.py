import os
import sounddevice as sd
import soundfile as sf

# === Caminho para o arquivo de áudio ===
audio_path = os.path.join(os.path.dirname(__file__), "jazz.wav")

# === Lê o arquivo de áudio
data, samplerate = sf.read(audio_path)

# === Lista os dispositivos disponíveis (opcional para debug)
print("\n🔎 Dispositivos disponíveis:")
print(sd.query_devices())

# === Define o dispositivo de saída (por exemplo: card 1, device 0 da WM8960)
sd.default.device = ('', 1)  # '' = default input, 1 = index da saída (WM8960)

# === Toca o áudio
print(f"\n▶️ Tocando '{audio_path}' na saída WM8960...")
sd.play(data, samplerate)
sd.wait()
print("✅ Reprodução concluída.")