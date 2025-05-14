import os
import time
import subprocess
import speech_recognition as sr

# === Função para capturar a voz com arecord
def gravar_audio():
    print("🎙️ Fale agora...")
    subprocess.run([
        "arecord", "-D", "default",
        "-f", "cd", "-t", "wav", "-d", "4",
        "-q", "captura.wav"
    ])
    print("✅ Áudio capturado.")

# === Função para transcrever o áudio
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

# === Loop contínuo
print("🟢 Assistente de escuta iniciado. Pressione Ctrl+C para sair.")

try:
    while True:
        gravar_audio()
        resposta = transcrever_audio()
        print(f"🗣️ Você disse: {resposta}")
        time.sleep(5)  # aguarda 5 segundos antes de escutar novamente
except KeyboardInterrupt:
    print("\n🔴 Encerrado pelo usuário.")
    if os.path.exists("captura.wav"):
        os.remove("captura.wav")