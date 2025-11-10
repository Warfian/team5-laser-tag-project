from random import randint
import pygame

initialized = False

def initialize():
    global initialized
    if not initialized:
        pygame.mixer.init()
        initialized = True

def play_music():
    initialize()

    # Generate random number to randomly select one of 8 tracks
    randNum = randint(1, 8)
    #print(randNum)
    musicTrack = f"photon_tracks/Track0{randNum}.mp3"

    # Play music track
    pygame.mixer.music.load(musicTrack)
    pygame.mixer.music.play()

def play_hit():
    initialize()
    pygame.mixer.Sound("photon_tracks/hit.wav").play()

def play_friendly_fire():
    initialize()
    pygame.mixer.Sound("photon_tracks/hitown.wav").play()

def play_base():
    initialize()
    pygame.mixer.Sound("photon_tracks/reset.wav").play()
