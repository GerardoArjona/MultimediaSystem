#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import json
import spotipy
import webbrowser
import time
import spotipy.util as util
from json.decoder import JSONDecodeError
from os import system, name

def main():
    menu()

def menu():
    option = 0
    while(option != 4):
        system('clear') 
        print(" *************** Centro Multimedia ***************")
        print("1) Spotify")
        print("2) Netflix")
        print("3) USB")
        print("4) Salir")
        line = input("Seleccion una opción:")
        option = int(line)
        print(option)
        if(option == 1):
            system('clear') 
            spotify()
        elif(option == 2):
            system('clear') 
            netflix()
        elif(option == 3):
            system('clear') 
            usb()
        elif(option == 4):
            system('clear')
            break
        else:
            pass

def spotify():
    option = 0
    while(option == 0):
        print("--- Spotify ---")
        scope = 'user-read-private user-read-playback-state user-modify-playback-state'
        username = input("Nombre de usuario: ")
        try:
            token = util.prompt_for_user_token(username, scope)
        except (AttributeError, JSONDecodeError):
            os.remove(f".cache-{username}")
            token = util.prompt_for_user_token(username, scope)

        # Spotify object  
        spotifyObject = spotipy.Spotify(auth=token)
        
        # User information
        system('clear') 
        user = spotifyObject.current_user()
        displayName = user['display_name']
        follower = user['followers']['total']
        print()
        print("------> Bienvenido a Spotify " + displayName)
        print()

        #Devices
        devices = spotifyObject.devices()
        selected_device = None
        device_index = 0
        print("Dispositivos:")
        for device in devices['devices']:
            print(str(device_index)+") " + device['name'])
            device_index = device_index + 1
        print()
        selected_device = input("Selecciona un dispositvo donde reproducir: ")
        deviceID = devices['devices'][int(selected_device)]['id']

        while True:
            system('clear')
            print()
            print("------> Bienvenido a Spotify " + displayName)
            print("---------> Dispositivo: " + devices['devices'][int(selected_device)]['name'])
            print()
            print("0) Buscar artista")
            print("1) Seleccionar dispositvo")
            print("2) Regresar al menu principal")
            print()
            choice = input("Selecciona una opcion: ")
            # Search for artist
            if choice == "0":
                print()
                searchQuery = input("Nombre:")
                searchResults = spotifyObject.search(searchQuery,1,0,"artist")
                print()
                system('clear')
                print()
                print("------> Bienvenido a Spotify " + displayName)
                print("---------> Dispositivo: " + devices['devices'][int(selected_device)]['name'])
                print()
                # Print artist details
                artist = searchResults['artists']['items'][0]
                print(">>>> Artista: "+ artist['name'])
                print(">>>> Followers: "+ str(artist['followers']['total']) + " followers")
                print(">>>> Generos: "+ artist['genres'][0])
                print()
                artistID = artist['id']
                print()
                time.sleep(2)
                # Album details
                trackURIs = []
                trackArt = []
                z = 0
                # Extract data from album
                albumResults = spotifyObject.artist_albums(artistID)
                albumResults = albumResults['items']

                for item in albumResults:
                    print("ALBUM: " + item['name'])
                    albumID = item['id']
                    albumArt = item['images'][0]['url']

                    # Extract track data
                    trackResults = spotifyObject.album_tracks(albumID)
                    trackResults = trackResults['items']

                    for item in trackResults:
                        print(str(z) + ") " + item['name'])
                        trackURIs.append(item['uri'])
                        trackArt.append(albumArt)
                        z+=1
                    print()
                
                print("x) Escoger otro artista ")
                print()
                # See album art
                while True:
                    try:
                        songSelection = input("Selecciona una cancion: ")
                        if songSelection == "x":
                            break
                        trackSelectionList = []
                        trackSelectionList.append(trackURIs[int(songSelection)])
                        spotifyObject.start_playback(deviceID, None, trackSelectionList)
                        webbrowser.open(trackArt[int(songSelection)])
                    except:
                        pass

            if choice == "1":
                system('clear')
                selected_device = None
                device_index = 0
                print()
                print("------> Bienvenido a Spotify " + displayName)
                print()
                print("Dispositivos:")
                for device in devices['devices']:
                    print(str(device_index)+") " + device['name'])
                    device_index = device_index + 1
                print()
                selected_device = input("Selecciona un dispositvo donde reproducir: ")
                deviceID = devices['devices'][int(selected_device)]['id']

            if choice == "2":
                option = 1
                break

def netflix():
    print("--- Netflix ---")
    line = input()
    option = int(line)
    print(option)

def usb():
    print("--- USB ---")
    line = input()
    option = int(line)
    print(option)



main()