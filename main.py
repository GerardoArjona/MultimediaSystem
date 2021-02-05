#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Se importan las librerias necesarias
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

# Se crea una función principal que llama a un función menú, 
# para mostrar el menú en consola
def main():
    menu()

# Función menú, la cual da acceso a los distintos módulos del centro
# multimedia
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

#Módulo: Spotify
def spotify():
    option = 0
    while(option == 0):
        print("--- Spotify ---")
        # Permisos del usuario al momnento de usar la API de Spotify
        scope = 'user-read-private user-read-playback-state user-modify-playback-state'
        username = input("Nombre de usuario: ")
        try:
            # Se intenta obtener el token de autenticación de la API
            token = util.prompt_for_user_token(username, scope)
        except (AttributeError, JSONDecodeError):
            # Si falla, se limpia la cache y se obtiene el token de autenticación
            os.remove(f".cache-{username}")
            token = util.prompt_for_user_token(username, scope)

        # Objeto Spotify, que nos dará acceso a la información de Spotify 
        spotifyObject = spotipy.Spotify(auth=token)
        
        # Información del usuario
        system('clear') 
        user = spotifyObject.current_user()
        displayName = user['display_name']
        follower = user['followers']['total']
        print()
        print("------> Bienvenido a Spotify " + displayName)
        print()

        # Dispositivos conectados y vinculados al usuario de Spotify
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

        # Se muestra el menú principal del módulo, en el cual se seleccionará si
        # se desea cambiar de dispositivo o buscar a un artista
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
            # Buscar artista
            if choice == "0":
                print()
                # Se obtiene el nombre del artista y se busca usando el objeto spotify
                searchQuery = input("Nombre:")
                searchResults = spotifyObject.search(searchQuery,1,0,"artist")
                print()
                system('clear')
                print()
                print("------> Bienvenido a Spotify " + displayName)
                print("---------> Dispositivo: " + devices['devices'][int(selected_device)]['name'])
                print()
                # Durante dos segundos se muestra la información relevante del artista encontrado
                artist = searchResults['artists']['items'][0]
                print(">>>> Artista: "+ artist['name'])
                print(">>>> Followers: "+ str(artist['followers']['total']) + " followers")
                print(">>>> Generos: "+ artist['genres'][0])
                print()
                artistID = artist['id']
                print()
                time.sleep(2)
                # Se muestran los detalles de los albums del artista
                trackURIs = []
                trackArt = []
                z = 0
                # De cada album obtenemos cada canción
                albumResults = spotifyObject.artist_albums(artistID)
                albumResults = albumResults['items']

                # Mostramos cada albúm
                for item in albumResults:
                    print("ALBUM: " + item['name'])
                    albumID = item['id']
                    albumArt = item['images'][0]['url']

                    # Obtenemos y mostramos cada canción del album en cuestión
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
                
                # De acuerdo a la selección del usuario se reproduce la canción
                # en el dispositivo seleccionado
                while True:
                    try:
                        songSelection = input("Selecciona una cancion: ")
                        if songSelection == "x":
                            break
                        trackSelectionList = []
                        trackSelectionList.append(trackURIs[int(songSelection)])
                        # Se reproduce la canción seleccionado en el dispositivo seleccionado
                        spotifyObject.start_playback(deviceID, None, trackSelectionList)
                        # En el navegador se muestra la imagen del album en cuestión
                        webbrowser.open(trackArt[int(songSelection)])
                    except:
                        pass

            # Seleccionamos el dispositivo en donde reproducir la música
            if choice == "1":
                system('clear')
                selected_device = None
                device_index = 0
                print()
                print("------> Bienvenido a Spotify " + displayName)
                print()
                print("Dispositivos:")
                # Se muestran los dispositivos disponibles y se espera una seleccion por
                # parte del usuario
                for device in devices['devices']:
                    print(str(device_index)+") " + device['name'])
                    device_index = device_index + 1
                print()
                selected_device = input("Selecciona un dispositvo donde reproducir: ")
                # Se almacena el dispositivo seleccionado
                deviceID = devices['devices'][int(selected_device)]['id']
            
            # Salimos del módulo
            if choice == "2":
                option = 1
                break

# Módulo: Netflix
def netflix():
    option = 0
    # Se muestra el menú principal del módulo y la busqueda de película
    while(option == 0):
        system('clear')
        print("--- Netflix ---")
        print()
        print("0) Buscar pelicula")
        print("1) Regresar al menu principal")
        print()
        choice = input("Selecciona una opcion: ")
        # Busqueda de película
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
                # Usando la selección del usuario y una api de terceros se realiza una búsqueda en Netflix
                try:
                    url = "https://unogsng.p.rapidapi.com/search"

                    querystring = {"query":movie}

                    headers = {
                        'x-rapidapi-key': "3758ec7ff8msh359f1f771180b29p1e80bfjsn72906a727e22",
                        'x-rapidapi-host': "unogsng.p.rapidapi.com"
                        }

                    url = "https://unogsng.p.rapidapi.com/search"

                    response = requests.request("GET", url, headers=headers, params=querystring)

                    # Si la busqueda es existosa se muestran las opciones de peliculas a elegir al usuario
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
                            # De acuerdo a la seleccion del usuario se despliega una navegador conteniendo la url
                            # exacta de la pelicula a ver en Netflix.
                            webbrowser.open("https://www.netflix.com/watch/" + str(movieIds[int(selection)]))
                            continue
                    # si la busqueda falla se muestra un mensaje de fallo y se regresa al menu principal
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
        # Salida del modulo
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