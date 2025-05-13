import os
import sys
import time
from PIL import Image, ImageSequence
import sounddevice as sd
import soundfile as sf

# === Caminhos
base_dir = os.path.dirname(__file__)
gif_path = os.path.join(base_dir, "output.gif")      # GIF otimizado (240x240)
audio_path = os.path.join(base_dir, "jazz.wav")       # Arquivo de áudio

# === Lê o áudio
data, samplerate = sf.read(audio_path)
duration = len(data) / samplerate  # em segundos

# === Inicializa o display
sys.path.append(os.path.join(base_dir, "library"))
from GC9A01 import GC9A01

display = GC9A01(
    port=0,
    cs=0,
    dc=25,
    backlight=18,
    rst=24,
    width=240,
    height=240,
    rotation=0,
    spi_speed_hz=40000000
)

# === Carrega os frames do GIF
print("📦 Carregando GIF...")
gif = Image.open(gif_path)
frames = [frame.copy().convert("RGB") for frame in ImageSequence.Iterator(gif)]
durations = [frame.info.get("duration", 100) / 1000.0 for frame in ImageSequence.Iterator(gif)]  # em segundos

# === Inicia o áudio no processo principal
sd.default.device = ('', 1)  # WM8960 como saída
print("▶️ Tocando áudio e exibindo animação...")
sd.play(data, samplerate)

# === Exibe a animação enquanto o som toca
start = time.time()
idx = 0

while time.time() - start < duration:
    frame = frames[idx % len(frames)]
    display.display(frame)
    time.sleep(durations[idx % len(durations)])
    idx += 1

# === Finaliza som e exibe frame final
sd.stop()
display.display(frames[-1])
print("✅ Execução concluída.")