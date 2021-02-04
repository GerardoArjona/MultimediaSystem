#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import json
import spotipy
import webbrowser
import time
import requests
import json
import psutil
import vlc
import random
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
    option = 0
    while(option == 0):
        system('clear')
        print("--- Netflix ---")
        print()
        print("0) Buscar pelicula")
        print("1) Regresar al menu principal")
        print()
        choice = input("Selecciona una opcion: ")
        # Search for artist
        if choice == "0":
            system('clear')
            print("--- Netflix ---")
            print()
            print("* Para regresar escribir: -regresar")
            print()
            movie = input("Pelicula a buscar: ")
            print()
            print("Buscando...")
            print()

            if movie == "-regresar":
                pass
            else:
                try:
                    url = "https://unogsng.p.rapidapi.com/search"

                    querystring = {"query":movie}

                    headers = {
                        'x-rapidapi-key': "3758ec7ff8msh359f1f771180b29p1e80bfjsn72906a727e22",
                        'x-rapidapi-host': "unogsng.p.rapidapi.com"
                        }

                    url = "https://unogsng.p.rapidapi.com/search"

                    response = requests.request("GET", url, headers=headers, params=querystring)

                    if response.status_code == 200:

                        system('clear')
                        print("--- Netflix ---")
                        print()
                        print("Resultados encontrados")
                        print()
                        movie_count = 0
                        movieIds = []
                        for movie in response.json()['results']:
                            movieIds.append(movie["nfid"])
                            print(str(movie_count) + ")")
                            print(" - Titulo: " + movie['title'])
                            print(" - Sinopsis: ")
                            print("\t" + movie['synopsis'])
                            print("---------------------------------------")
                            movie_count = movie_count + 1 
                        print()
                        print("x) Escoger otra pelicula ")
                        print()
                        selection = input("Selecciona una pelicula: ")

                        if selection == "x":
                            pass
                        else:
                            webbrowser.open("https://www.netflix.com/watch/" + str(movieIds[int(selection)]))
                            continue
                    else:
                        system('clear')
                        print("--- Netflix ---")
                        print()
                        print("Resultados no encontrados...")
                        print()
                        time.sleep(2)
                        pass
                except:
                    system('clear')
                    print("--- Netflix ---")
                    print()
                    print("Resultados no encontrados...")
                    print()
                    time.sleep(2)
                    pass
        if choice == "1":
            option = 1
            break

def usb():
    import usb
    option = 0
    while(option == 0):
        system('clear')
        print("--- USB ---")
        print()
        drives = []
        drive_count = 0

        partitions = psutil.disk_partitions()

        for p in partitions:
            mounts = p.mountpoint.split("/")
            if(mounts[1] == "media" and mounts[2] == "pi"):
                drives.append(p.mountpoint)
                print(str(drive_count) + ") " + mounts[-1])
                drive_count = drive_count + 1
        print()
        print("x) Regresar")
        print()

        selection = input("Selecciona un USB: ")

        if(selection == "x"):
            break

        try:
            music = []
            images = []
            movies = []
            usb_content = os.listdir(drives[int(selection)])
            vlc_instance = vlc.Instance()
            player = vlc_instance.media_player_new()
            system('clear')
            print("--- USB ---")
            print()
            for usb_file in usb_content:
                usb_file_type = usb_file.split(".")[-1]
                if(usb_file_type == "mp3"):
                    music.append(usb_file)
                elif(usb_file_type == "mp4"):
                    movies.append(usb_file)
                elif(usb_file_type == "jpg" or usb_file_type == "jpeg"):
                    images.append(usb_file)
            if(len(music) > 0):
                print("m) Musica")
            if(len(music) > 0):
                print("p) Peliculas o videos")
            if(len(music) > 0):
                print("i) Imagenes o fotos")
            print()
            print("x) Regresar")
            print()
            usb_media_selection = input("Selecciona: ")
            if(usb_media_selection == "m"):
                # timer = threading.timer(5, new_song)
                # timer.start()
                playing_song = ""
                auto_song = True
                while(True):
                    system('clear')
                    print("--- USB ---")
                    print()
                    song_count = 0
                    if(auto_song == True):
                        player.stop()
                        playing_song = music[random.randint(0, len(music) - 1 )]
                        source = drives[int(selection)] + "/" + music[random.randint(0, len(music) - 1 )]
                        media = vlc_instance.media_new(source)
                        player.set_media(media)
                        player.play()
                    for song in music:
                        if(playing_song == song):
                            print(str(song_count)+ ") "+ song + " <------- Reproduciendo") 
                        else:
                            print(str(song_count)+ ") "+ song)
                        song_count = song_count + 1
                    print()
                    print("x) Regresar")
                    print()
                    song_selection = input("Selecciona una cancion: ")
                    if(song_selection == "x"):
                        player.stop()
                        break
                    else:
                        player.stop()
                        auto_song = False
                        playing_song = music[int(song_selection)]
                        source = drives[int(selection)] + "/" + music[int(song_selection)]
                        media = vlc_instance.media_new(source)
                        player.set_media(media)
                        player.play()
            elif(usb_media_selection == "p"):
                playing_movie = ""
                while(True):
                    system('clear')
                    print("--- USB ---")
                    print()
                    movie_count = 0
                    for movie in movies:
                        if(playing_movie == movie):
                            print(str(movie_count) + ") " + movie + " <------- Reproduciendo") 
                        else:
                            print(str(movie_count) + ") " + movie)
                        movie_count = movie_count + 1
                    print()
                    print("x) Regresar")
                    print()
                    movie_selection = input("Selecciona una pelicula o video: ")
                    if(movie_selection == "x"):
                        player.stop()
                        break
                    else:
                        player.stop()
                        playing_movie = movies[int(movie_selection)]
                        source = drives[int(selection)] + "/" + movies[int(movie_selection)]
                        media = vlc_instance.media_new(source)
                        player.set_media(media)
                        player.play()
            elif(usb_media_selection == "i"):
                vlc_i = vlc.Instance()
                image_player = vlc_i.media_list_player_new()
                while True:
                    system('clear')
                    print("--- USB ---")
                    print()
                    slideshow_images = []
                    for image in images:
                        print(image)
                        slideshow_images.append(drives[int(selection)] + "/" + image)
                    Media = vlc_instance.media_list_new(slideshow_images)
                    try:
                        image_player.set_media_list(Media)
                        for index, name in enumerate(slideshow_images):
                            print(name)
                            image_player.play_item_at_index(index)
                            time.sleep(5)
                        image_player.stop()
                    except Exception as e:
                        print(e)
                    system('clear')
                    print("--- USB ---")
                    print()
                    print("Las imagenes se han mostrado, favor de regresar")
                    print()
                    print("x) Regresar")
                    print()
                    image_selection = input("Selecciona: ")
                    if(image_selection == "x"):
                        image_player.stop()
                        break
            elif(usb_media_selection == "x"):
                pass

        except: 
            pass

main()