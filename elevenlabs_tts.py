import time
import pygame


def play_audio(sound_file):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
        
def main():
    play_audio('ElevenLabs_2026-02-08T03_10_28_Northern Terry_pvc_sp87_s30_sb90_se38_b_m2.mp3')


if __name__ == '__main__':
    main()