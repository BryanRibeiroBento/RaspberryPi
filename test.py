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

# ─── Configurações ───────────────────────────────────────────────────────────
load_dotenv()  # carrega OPENAI_API_KEY do .env
openai.api_key = os.getenv("OPENAI_API_KEY")

RECORD_SECONDS = 4
RECORD_FILE   = "captura.wav"

# ─── Captura de áudio ─────────────────────────────────────────────────────────
def capturar_audio():
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
    return out.content  # bytes do WAV PCM compatível

# ─── Playback com simpleaudio ─────────────────────────────────────────────────
def tocar_wav_bytes(bytes_wav: bytes):
    bio = io.BytesIO(bytes_wav)
    with wave.open(bio, "rb") as wf:
        wave_obj = sa.WaveObject(
            wf.readframes(wf.getnframes()),
            num_channels=wf.getnchannels(),
            bytes_per_sample=wf.getsampwidth(),
            sample_rate=wf.getframerate()
        )
    play = wave_obj.play()
    play.wait_done()

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

        print("▶️ Reproduzindo resposta...")
        tocar_wav_bytes(wav_bytes)
        print("✅ Pronto.\n")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\n🔴 Encerrando assistente.")
    try:
        os.remove(RECORD_FILE)
    except FileNotFoundError:
        pass