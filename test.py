import os
os.environ["SDL_AUDIODRIVER"] = "alsa"  # FORÇA USO DO ALSA

import sys
import time
import spidev
import RPi.GPIO as GPIO
from PIL import Image
import pygame
import threading



# === Inicia o mixer para tocar música ===
pygame.mixer.init()
pygame.mixer.music.load("jazz.wav")  # Altere o nome do arquivo se necessário

# === Toca a música em uma thread separada ===
def play_music():
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)

music_thread = threading.Thread(target=play_music)
music_thread.start()

# === Inicia o display ===
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

# === Carrega imagem base ===
img_path = "badbunny.png"
base_image = Image.open(img_path).convert("RGB").resize((240, 240))

# === Loop de animação ===
angle = 0
while pygame.mixer.music.get_busy():  # roda enquanto a música estiver tocando
    rotated = base_image.rotate(angle)
    display.display(rotated)
    angle = (angle + 5) % 360
    time.sleep(0.05)

# Opcional: limpa tela ou mostra imagem estática ao fim
display.display(base_image)