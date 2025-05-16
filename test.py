#!/usr/bin/env python3
import os
import io
import wave
import time

import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
import openai
import simpleaudio as sa

from dotenv import load_dotenv
from PIL import Image
import sys

# ─── Display GC9A01 ───────────────────────────────────────────────────────────
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
    img = Image.open(nome).convert("RGB").resize((240,240))
    display.display(img)

# ─── Configurações ───────────────────────────────────────────────────────────
load_dotenv()  # carrega OPENAI_API_KEY do .env

RECORD_SECONDS = 4
RECORD_FILE   = "captura.wav"

# ─── Captura de áudio ─────────────────────────────────────────────────────────
def capturar_audio():
    mostrar_imagem("human.png")
    print("🎙️ Gravando...")
    fs = 44100
    data = sd.rec(int(RECORD_SECONDS * fs), samplerate=fs,
                  channels=1, dtype="float32", device="default")
    sd.wait()
    data16 = (data * 32767).astype("int16")
    sf.write(RECORD_FILE, data16, fs, subtype="PCM_16")
    print("✅ Áudio salvo em", RECORD_FILE)

# ─── Transcrição ───────────────────────────────────────────────────────────────
def transcrever():
    r = sr.Recognizer()
    with sr.AudioFile(RECORD_FILE) as src:
        audio = r.record(src)
    try:
        texto = r.recognize_google(audio, language="pt-BR")
        print("🗣️ Você disse:", texto)
        return texto
    except sr.UnknownValueError:
        print("❓ Não entendi.")
        return ""
    except sr.RequestError as e:
        print("❌ Erro no serviço:", e)
        return ""

# ─── ChatGPT ───────────────────────────────────────────────────────────────────
def chamar_chatgpt(prompt: str) -> str:
    resp = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente útil."},
            {"role": "user",   "content": prompt}
        ]
    )
    resposta = resp.choices[0].message.content.strip()
    print("🤖 GPT diz:", resposta)
    return resposta

# ─── TTS (retorna bytes WAV) ──────────────────────────────────────────────────
def texto_para_fala_wav(texto: str) -> bytes:
    out = openai.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=texto,
        response_format="wav"
    )
    return out.content  # bytes do WAV PCM 16-bit 44.1kHz estéreo

# ─── Playback com simpleaudio ─────────────────────────────────────────────────
def tocar_wav_bytes(bytes_wav: bytes):
    mostrar_imagem("robot.png")
    bio = io.BytesIO(bytes_wav)
    with wave.open(bio, "rb") as wf:
        wave_obj = sa.WaveObject(
            wf.readframes(wf.getnframes()),
            num_channels=wf.getnchannels(),
            bytes_per_sample=wf.getsampwidth(),
            sample_rate=wf.getframerate()
        )
    print("▶️ Reproduzindo resposta...")
    play = wave_obj.play()
    play.wait_done()
    print("✅ Pronto.\n")

# ─── Loop principal ───────────────────────────────────────────────────────────
print("🟢 Assistente totalmente Python iniciado. Ctrl+C para sair.\n")
try:
    while True:
        capturar_audio()
        texto = transcrever()
        if not texto:
            continue

        resposta = chamar_chatgpt(texto)
        wav_bytes = texto_para_fala_wav(resposta)
        tocar_wav_bytes(wav_bytes)

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\n🔴 Encerrando assistente.")
    if os.path.exists(RECORD_FILE):
        os.remove(RECORD_FILE)