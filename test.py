#!/usr/bin/env python3
import os, io, wave, time
import sounddevice as sd, soundfile as sf
import speech_recognition as sr
import openai, simpleaudio as sa
from dotenv import load_dotenv
from PIL import Image
import sys

# ─── Display GC9A01 ─────────────────────────────────────────
sys.path.append(os.path.dirname(__file__) + '/library')
from GC9A01 import GC9A01
display = GC9A01(port=0, cs=0, dc=25, backlight=18, rst=24,
                 width=240, height=240, rotation=0, spi_speed_hz=40000000)

def mostrar_imagem(nome):
    img = Image.open(nome).convert("RGB").resize((240,240))
    display.display(img)

# ─── Config ──────────────────────────────────────────────────
load_dotenv()

RECORD_SECONDS = 4
RECORD_FILE = "captura.wav"

# ─── Grava ────────────────────────────────────────────────────
def capturar_audio():
    print("🎙️ Gravando...")
    fs = 44100
    data = sd.rec(int(RECORD_SECONDS * fs), samplerate=fs,
                  channels=1, dtype="float32", device="default")
    sd.wait()
    data16 = (data * 32767).astype("int16")
    sf.write(RECORD_FILE, data16, fs, subtype="PCM_16")
    print("✅ Captura salva")

# ─── Transcreve ───────────────────────────────────────────────
def transcrever():
    r = sr.Recognizer()
    with sr.AudioFile(RECORD_FILE) as src:
        audio = r.record(src)
    try:
        texto = r.recognize_google(audio, language="pt-BR")
        print("🗣️ Você disse:", texto)
        return texto
    except:
        print("❓ Não entendi.")
        return ""

# ─── ChatGPT ─────────────────────────────────────────────────
def chamar_chatgpt(prompt):
    resp = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"system","content":"Você é um assistente útil."},
                  {"role":"user",  "content":prompt}]
    )
    texto = resp.choices[0].message.content.strip()
    print("🤖 GPT diz:", texto)
    return texto

# ─── TTS OpenAI ──────────────────────────────────────────────
def texto_para_fala_wav(texto):
    out = openai.audio.speech.create(
        model="tts-1", voice="nova",
        input=texto, response_format="wav"
    )
    return out.content

# ─── Playback ────────────────────────────────────────────────
def tocar_wav_bytes(bytes_wav):
    bio = io.BytesIO(bytes_wav)
    with wave.open(bio, "rb") as wf:
        wave_obj = sa.WaveObject(
            wf.readframes(wf.getnframes()),
            num_channels=wf.getnchannels(),
            bytes_per_sample=wf.getsampwidth(),
            sample_rate=wf.getframerate()
        )
    print("▶️ Tocando resposta…")
    play = wave_obj.play()
    play.wait_done()
    print("✅ Pronto.\n")

# ─── Loop principal ──────────────────────────────────────────
print("🟢 Assistente Python iniciado. Ctrl+C para sair.\n")
try:
    while True:
        # 1) Humano
        mostrar_imagem("human.png")
        time.sleep(1.0)

        # 2) Grava
        capturar_audio()

        # 3) Transcreve + GPT
        txt = transcrever()
        if not txt:
            continue
        resp = chamar_chatgpt(txt)

        # 4) Robô
        mostrar_imagem("robot.png")
        time.sleep(1.0)

        # 5) TTS + playback
        wav = texto_para_fala_wav(resp)
        tocar_wav_bytes(wav)

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\n🔴 Encerrando…")
    try: os.remove(RECORD_FILE)
    except: pass