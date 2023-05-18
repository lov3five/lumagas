import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame

def sound_notification():
    pygame.mixer.init()
    beep_sound = pygame.mixer.Sound("./utils/beep-01a.wav")
    beep_sound.play()
    pygame.time.delay(3000)