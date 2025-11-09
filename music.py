from random import randint
import pygame

def play_music():
    # Initialize pygame mixer
    pygame.mixer.init()

    # Generate random number to randomly select one of 8 tracks
    randNum = randint(1, 8)
    #print(randNum)
    musicTrack = f"photon_tracks/Track0{randNum}.mp3"

    # Play music track
    pygame.mixer.music.load(musicTrack)
    pygame.mixer.music.play()