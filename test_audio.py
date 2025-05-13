import sounddevice as sd
import numpy as np
import speech_recognition as sr
import io

# === Configurações de áudio ===
samplerate = 16000       # Hz (compatível com Google)
duration = 5             # Segundos de gravação por vez
device_index = 1         # Use a entrada do WM8960 (verifique com sd.query_devices())

recognizer = sr.Recognizer()

print("🎙️ Fale algo...")

while True:
    try:
        # === Captura áudio ao vivo com o sounddevice ===
        print("\n⏺️ Gravando...")
        audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16', device=(device_index, None))
        sd.wait()
        print("✅ Áudio capturado.")

        # === Converte o áudio para formato compatível com SpeechRecognition ===
        audio_bytes = audio_data.flatten().tobytes()
        audio_stream = io.BytesIO(audio_bytes)
        audio = sr.AudioData(audio_stream.read(), samplerate, 2)

        # === Reconhecimento de fala ===
        print("🧠 Reconhecendo...")
        text = recognizer.recognize_google(audio, language="pt-BR")
        print(f"🗣️ Você disse: {text}")

    except sr.UnknownValueError:
        print("❌ Não entendi o que foi dito.")
    except sr.RequestError as e:
        print(f"❌ Erro ao se comunicar com o serviço: {e}")
    except KeyboardInterrupt:
        print("\n🚪 Encerrando...")
        break