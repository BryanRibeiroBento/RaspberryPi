import os
import subprocess
import speech_recognition as sr
import pyttsx3
from PIL import Image
import sys
import time

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
tts = pyttsx3.init()
tts.setProperty('rate', 150)
tts.setProperty('volume', 1.0)
tts.setProperty('voice', 'pt+f5')

def falar(texto):
    mostrar_imagem("robot.png")
    print(f"🤖 Assistente: {texto}")
    tts.say(texto)
    tts.runAndWait()

def ouvir_e_transcrever():
    mostrar_imagem("human.png")

    print("🎙️ Gravando...")
    subprocess.run([
        "arecord", "-D", "hw:1,0", "-f", "cd",
        "-t", "wav", "-d", "4", "-q", "voz.wav"
    ])

    recognizer = sr.Recognizer()
    with sr.AudioFile("voz.wav") as source:
        audio = recognizer.record(source)

    print("🧠 Reconhecendo...")
    return recognizer.recognize_google(audio, language="pt-BR")

def responder(texto):
    texto = texto.lower()
    if "oi" in texto or "olá" in texto:
        return "Olá! Como posso te ajudar hoje?"
    elif "nome" in texto:
        return "Eu sou o seu assistente de voz."
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
        try:
            texto = ouvir_e_transcrever()
            print(f"🗣️ Você: {texto}")
            resposta = responder(texto)
            falar(resposta)

        except sr.UnknownValueError:
            print("❌ Não entendi. Pode repetir?")
        except sr.RequestError as e:
            print(f"❌ Erro ao conectar ao serviço de fala: {e}")
        except KeyboardInterrupt:
            raise
except KeyboardInterrupt:
    print("\n🔴 Assistente encerrado.")