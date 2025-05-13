import sounddevice as sd
import numpy as np
import speech_recognition as sr
import pyttsx3
import io
import os
import sys
from PIL import Image

# === Inicializa display GC9A01
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

# === Configurações de áudio
SAMPLERATE = 16000
DURATION = 4  # segundos de escuta por ciclo
DEVICE_INDEX = 1  # índice do microfone WM8960

# === Inicializa reconhecimento e voz
recognizer = sr.Recognizer()
tts = pyttsx3.init()
tts.setProperty('rate', 150)
tts.setProperty('volume', 1.0)
tts.setProperty('voice', 'pt+f5')  # voz feminina em português (ajustável)

def falar(texto):
    mostrar_imagem("robot.png")  # mostra a imagem do robô antes de falar
    print(f"🤖 Assistente: {texto}")
    tts.say(texto)
    tts.runAndWait()

def ouvir():
    mostrar_imagem("human.png")  # mostra a imagem do humano antes de escutar
    print("🎙️ Escutando...")
    audio_data = sd.rec(int(DURATION * SAMPLERATE), samplerate=SAMPLERATE, channels=1, dtype='int16', device=(DEVICE_INDEX, None))
    sd.wait()
    audio_bytes = audio_data.flatten().tobytes()
    audio_stream = io.BytesIO(audio_bytes)
    return sr.AudioData(audio_stream.read(), SAMPLERATE, 2)

def responder(texto):
    texto = texto.lower()
    if "oi" in texto or "olá" in texto:
        return "Olá! Como posso te ajudar hoje?"
    elif "nome" in texto:
        return "Eu sou o seu assistente de voz no Raspberry Pi."
    elif "obrigado" in texto or "valeu" in texto:
        return "De nada! Estou aqui sempre que precisar."
    elif "tchau" in texto:
        return "Até mais!"
    else:
        return "Desculpe, ainda estou aprendendo. Pode repetir de outra forma?"

# === Loop principal
print("🟢 Assistente de voz iniciado. Pressione Ctrl+C para sair.")

try:
    while True:
        audio = ouvir()

        try:
            texto = recognizer.recognize_google(audio, language="pt-BR")
            print(f"🗣️ Você: {texto}")
            resposta = responder(texto)
            falar(resposta)

        except sr.UnknownValueError:
            print("🤷‍♂️ Não entendi. Tente de novo.")
        except sr.RequestError as e:
            print(f"❌ Erro de conexão com o serviço de voz: {e}")
except KeyboardInterrupt:
    print("\n🔴 Encerrado pelo usuário.")