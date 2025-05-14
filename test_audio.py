import os
import time
import subprocess
import speech_recognition as sr
import pyttsx3

# === Inicializa TTS (voz)
tts = pyttsx3.init()
tts.setProperty('rate', 150)
tts.setProperty('volume', 1.0)
tts.setProperty('voice', 'pt+f5')  # voz feminina, idioma português

# === Captura áudio com arecord
def gravar_audio():
    print("🎙️ Fale agora...")
    subprocess.run([
        "arecord", "-D", "default",
        "-f", "cd", "-t", "wav", "-d", "4",
        "-q", "captura.wav"
    ])
    print("✅ Áudio capturado.")

# === Transcreve com speech_recognition
def transcrever_audio():
    recognizer = sr.Recognizer()
    with sr.AudioFile("captura.wav") as source:
        audio = recognizer.record(source)
    try:
        texto = recognizer.recognize_google(audio, language="pt-BR")
        return texto
    except sr.UnknownValueError:
        return "🤷 Não entendi."
    except sr.RequestError as e:
        return f"❌ Erro: {e}"

# === Gera resposta com base no texto
def gerar_resposta(texto):
    texto = texto.lower()
    if "seu nome" in texto:
        return "Meu nome é assistente Pi."
    elif "oi" in texto or "olá" in texto:
        return "Olá! Como posso te ajudar?"
    elif "que horas" in texto:
        return "Desculpe, ainda não sei ver as horas."
    elif "obrigado" in texto or "valeu" in texto:
        return "De nada, sempre à disposição."
    elif "tchau" in texto:
        return "Até logo!"
    else:
        return "Ainda estou aprendendo. Pode repetir de outro jeito?"

# === Fala usando pyttsx3
def falar(texto):
    print(f"🤖 Assistente: {texto}")
    tts.say(texto)
    tts.runAndWait()

# === Loop principal
print("🟢 Assistente de voz iniciado. Pressione Ctrl+C para sair.")

try:
    while True:
        gravar_audio()
        texto_usuario = transcrever_audio()
        print(f"🗣️ Você disse: {texto_usuario}")
        time.sleep(5)
        resposta = gerar_resposta(texto_usuario)
        falar(resposta)
except KeyboardInterrupt:
    print("\n🔴 Encerrado pelo usuário.")
    if os.path.exists("captura.wav"):
        os.remove("captura.wav")