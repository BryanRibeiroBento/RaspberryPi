import os
import io
import time

import openai
import sounddevice as sd
import soundfile as sf

from dotenv import load_dotenv
import speech_recognition as sr

# ─── Configurações ───────────────────────────────────────────────────────────
load_dotenv()


RECORD_SECONDS = 4
RECORD_FILE   = "captura.wav"

# ─── Gravação em WAV via sounddevice ──────────────────────────────────────────
def capturar_audio():
    print("🎙️ Gravando...")
    # Captura em float32, mas vamos escrever em WAV PCM 16-bit
    samplerate = 44100
    data = sd.rec(int(RECORD_SECONDS * samplerate), samplerate=samplerate,
                  channels=1, dtype='float32', device='default')
    sd.wait()
    # Normaliza e converte para int16
    data16 = (data * 32767).astype('int16')
    sf.write(RECORD_FILE, data16, samplerate, subtype='PCM_16')
    print("✅ Captura salva em", RECORD_FILE)

# ─── Transcrição via Google SpeechRecognition ───────────────────────────────
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

# ─── Chama o ChatGPT para gerar a resposta em texto ──────────────────────────
def chamar_chatgpt(prompt: str) -> str:
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"system", "content":"Você é um assistente útil."},
            {"role":"user",   "content":prompt}
        ]
    )
    resposta = res.choices[0].message.content.strip()
    print("🤖 GPT diz:", resposta)
    return resposta

# ─── TTS da OpenAI retornando WAV em memória ─────────────────────────────────
def texto_para_fala_wav(resposta: str):
    # Requisição pedindo WAV PCM (não MP3)
    out = openai.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=resposta,
        audio_format="wav"     # chave para obter WAV em vez de MP3
    )
    bytes_wav = out.content   # conteúdo é o WAV PCM 16-bit 44.1kHz estéreo
    return bytes_wav

# ─── Reprodução em memória via sounddevice ─────────────────────────────────
def tocar_wav_bytes(bytes_wav: bytes):
    bio = io.BytesIO(bytes_wav)
    data, samplerate = sf.read(bio, dtype='int16')
    print("▶️ Reproduzindo resposta...")
    sd.play(data, samplerate=samplerate, device='default')
    sd.wait()
    print("✅ Reprodução concluída.\n")

# ─── Loop principal ─────────────────────────────────────────────────────────
print("🟢 Assistente 100% Python iniciado. Ctrl+C para sair.\n")

try:
    while True:
        capturar_audio()
        texto = transcrever()
        if not texto:
            continue
        resp = chamar_chatgpt(texto)
        wav_bytes = texto_para_fala_wav(resp)
        tocar_wav_bytes(wav_bytes)
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\n🔴 Encerrando assistente.")
    try:
        os.remove(RECORD_FILE)
    except FileNotFoundError:
        pass