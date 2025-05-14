import os
from PIL import Image
import sys
import time
import openai
import subprocess
from dotenv import load_dotenv

# === Carrega variáveis do arquivo .env
load_dotenv()


# === Inicializa display
sys.path.append(os.path.join(os.path.dirname(__file__), 'library'))
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

def mostrar_imagem(nome):
    img = Image.open(nome).convert("RGB").resize((240, 240))
    display.display(img)

# === Inicializa o TTS
nome = "eye.jpg"
mostrar_imagem(nome)





# === Texto a ser falado
texto = "Hey Marco, I'm Optiko your Personal Data Analyst, How may I help You?"



# === Solicita a fala
response = openai.audio.speech.create(
    model="tts-1",         # Ou "tts-1-hd"
    voice="nova",          # nova, shimmer, alloy, echo, fable, onyx
    input=texto
)

# === Salva como MP3
with open("resposta.mp3", "wb") as f:
    f.write(response.content)
print("✅ Áudio salvo como resposta.mp3")

# === Converte MP3 → WAV
subprocess.run([
    "ffmpeg", "-y", "-i", "resposta.mp3", "resposta.wav"
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("✅ Convertido para resposta.wav")

# === Toca na WM8960
subprocess.run(["aplay", "-D", "hw:1,0", "resposta.wav"])