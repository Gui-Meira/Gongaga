from random import shuffle

def feedback():  
    while True:
        answer = input("\nDid you like this reccomendation (yes/no/exit --> suggest another activity)?: ").strip().lower()
        if answer == "yes":
            print("\nGreat, have fun!")
            return True
        elif answer == "exit":
            print("Going back to activity suggestions...")
            return None
        elif answer == "no":
            print("\nLet's find something else...")
            return False
        else:
            print("Please, answer correctly.")

#futuramente usar PANDA(library) para fazer uma pesquisa mais específica;
#categorizar as atividades baseado no tempo disponível do usuário;
#adicionar mais uma opção de atividade caso queira error mostrar o resultado;
random_activities = ['watching anime', 'watching movie', 'running or strolling', 'playing games', 
                'drawing', 'reading books', 'listening to a song', 'calling your parents', 
                'writing your thoughts', 'learning a language', 'cooking', 'studying']

shuffle(random_activities)

print("\nWELCOME TO THE DECISION-MAKING RANDOMIZER!")
print("\nWe know you are indecisive, let us choose something.")
liked = False
while random_activities:
    while not liked:
        activity = random_activities.pop()
        print("\nYou could try:", activity)
        if activity == 'watching anime':
            break_main_loop = False
            while True:
                
                import requests
                    
                anime_name = input("Anime request (exit --> suggest another activity): ").strip().lower()
                if anime_name == 'exit':
                    print("Going back to activity suggestions...")
                    break_main_loop = True
                    break 
                
                try:
                    res = requests.get(f"https://api.jikan.moe/v4/anime?q={anime_name}&limit=1",timeout=60)
                    res.raise_for_status()
                    data = res.json()
                    
                    if res.status_code == 200:
                        anime = data['data'][0]
                        anime_id = anime["mal_id"]
                        print(f"\nTitle: {anime['title']}")
                        print(f"Score: {anime['score']}")
                        print(f"Type: {anime['type']}")
                        print(f"Episodes: {anime['episodes']}")
                        
                        season = anime.get('season', 'Unknown')
                        year = anime.get('year', 'Unknonw')
                        print(f"Season: {season.capitalize() if season else 'Unknown'}")
                        print(f"Year: {year if year else 'Unknown'}")                      
                        
                        studios = anime['studios']
                        if studios:
                            studio_names = ', '.join(studio['name'] for studio in studios)
                            print(f"Studios: {studio_names}")
                        genres = anime['genres']
                        if genres:
                            genre_names = ', '.join(genre['name'] for genre in genres)
                            print(f"Genres: {genre_names}")
                        
                        duration = anime.get("duration", 'Unknown')
                        print(f"Duration: {duration}")

                        character_res = requests.get(f"https://api.jikan.moe/v4/anime/{anime_id}/characters")
                        character_res.raise_for_status()
                        character_data = character_res.json()

                        main_chars = [entry["character"]["name"]
                                      for entry in character_data["data"]
                                      if entry.get("role") == "Main"][:5]
                        if main_chars:
                            print(f"Main Characters: {', '.join(main_chars)}")
                        else:
                            print(f"Main Characters: No information available")

                        print(f"Synopsis: {anime['synopsis']}")
                    else:
                        print("Error fetching data from anime API.")
                
                except requests.Timeout:
                    print("The request took too long, try again later.")
                except requests.ConnectionError:
                    print("Connection error, check your internet connection.")
                
                result = feedback()
                if result is True:
                    liked = True
                    break
                elif result is None:
                    break_main_loop = True
                    break
            if break_main_loop:
                continue  

        elif activity == 'watching movie':             
            break_main_loop_1 = False
            while True:        

                import requests

                api_key_1 = "7a9ec72ba0ce87e204846427c79125bf"
                def get_genres(api_key):
                    url = "https://api.themoviedb.org/3/genre/movie/list"
                    res = requests.get(url, params={"api_key": api_key, "language": "en-US"})
                    res.raise_for_status()
                    data = res.json()
                    return {genre["id"]: genre["name"] for genre in data["genres"]}
                try:
                    genre_map = get_genres(api_key_1)
                except:
                    print("Failed to fetch genres.")
                    genre_map = {}
                    
                movie_name = input("Movie request (exit --> suggest another activity): ").strip().lower()
                if movie_name == 'exit':
                    print("Going back to activity suggestions...")
                    break_main_loop_1 = True
                    break 

                try:
                    res_1 = requests.get("https://api.themoviedb.org/3/search/movie",  
                                params={"api_key": api_key_1, 
                                        "query": movie_name, 
                                        "language": "en-US"}, 
                               timeout=40)
                    res_1.raise_for_status()
                    data_1 = res_1.json()

                    if res_1.status_code == 200:
                        if data_1["results"]:
                            movie_name = data_1["results"][0]
                            title = movie_name.get("title", "Unknown title")
                            release_date = movie_name.get("release_date", "Unknown date")
                            rating = movie_name.get("vote_average", "No rating",)
                            overview = movie_name.get("overview", "No synopsis available.")
                            movie_id = movie_name.get("id")
                            
                            print(f"\nTitle: {title}")
                            print(f"Release year: {release_date.split('-')[0]}")
                            
                            details_res = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}",
                                        params={"api_key": api_key_1, "language": "en-US"})
                            details_res.raise_for_status()
                            details_data = details_res.json()
                            runtime = details_data.get("runtime", None)
                            if runtime:
                                hours = runtime // 60
                                minutes = runtime % 60
                                print(f"Duration: {hours}h {minutes}min")
                            else:
                                print("Runtime information not available.")

                            if rating >= 8:
                                rt = "Excellent"
                            elif rating >= 6:
                                rt = "Good"
                            elif rating >= 4:
                                rt = "Average"
                            elif rating >= 2:
                                rt = "Poor"
                            else:
                                rt = "Terrible"
                            print(f"TMDB Users Rating: {rating:.2f} --> {rt}")

                            genre_ids = movie_name.get("genre_ids", [])
                            genres = [genre_map.get(gid, "Unknown") for gid in genre_ids]
                            print(f"Genres: {', '.join(genres) if genres else 'Unknown genres'}")

                            credits_res = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/credits",
                                        params={"api_key": api_key_1, "language": "en-US"})
                            credits_res.raise_for_status()
                            credits_data = credits_res.json()
                            cast = [actor["name"] for actor in credits_data.get("cast", [])[:5]]
                            print(f"Main Cast: {", ".join(cast) if cast else "No cast information available"}")
                            
                            print(f"Synopsis: {overview}")

                            res_2 = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers",
                                    params={"api_key": api_key_1})
                            res_2.raise_for_status()
                            data_2 = res_2.json()
                            us = data_2.get("results", {}).get("US", {})
                            flatrate = us.get("flatrate", [])
                            if flatrate:
                                providers = [prov["provider_name"] for prov in flatrate]
                                print("\nAvailable on:", ", ".join(providers))
                            else:
                                print("\nNot available for streaming.")
                        else:
                            print("Movie not found.")
                
                except requests.Timeout:
                    print("The request took too long, try again later.")
                except requests.ConnectionError:
                    print("Connection error, check your internet connection.")

                result = feedback()
                if result is True:
                    liked = True
                    break
                elif result is None:
                    break_main_loop_1 = True
                    break
            if break_main_loop_1:
                continue  

        elif activity == 'playing games':   
            break_main_loop_2 = False
            while True:
                
                import requests

                game_name = input("Game request (exit --> suggest another activity): ").strip().lower()
                if game_name == 'exit':
                    print("Going back to activity suggestions...")
                    break_main_loop_2 = True
                    break 

                api_key_2 = "47fccaf08a364c2cbe9fe3a076b217ff"

                try:
                    res_2 = requests.get(f"https://api.rawg.io/api/games?search={game_name}&key={api_key_2}",timeout=60)
                    res_2.raise_for_status()
                    data_2 = res_2.json()
                    
                    if data_2['results']:
                        game = data_2['results'][0]
                        game_id = game['id']

                        detailed_res_2 = requests.get(f"https://api.rawg.io/api/games/{game_id}",
                            params={"key": api_key_2},
                           timeout=40)
                        detailed_res_2.raise_for_status()
                        detailed_data_2 = detailed_res_2.json()

                        print(f"\nTitle: {game['name']}")
                        print(f"Released: {game['released']}")
                        
                        plat = [p['platform']['name'] for p in game['platforms']]                  
                        print(f"Platforms: {", ".join(plat) if plat else "No platforms available"}")
                        
                        gen = [g['name'] for g in detailed_data_2.get('genres', [])]
                        print(f"Genres: {", ".join(gen) if gen else "No genres available"}")

                        tags = [tag['name'] for tag in detailed_data_2.get('tags', [])][:10]
                        print(f"Tags: {", ".join(tags).capitalize() if tags else "No tags available"}")

                        publishers = [publi['name'] for publi in detailed_data_2.get('publishers', [])]
                        print(f"Publishers: {", ".join(publishers) if publishers else "No publishers available"}")

                        metacritic = game.get('metacritic')
                        if metacritic:    
                            print(f"Metacritic Score: {metacritic}")
                        else:
                            print("Metacritic Score: No score available at the moment.")
                        
                        print(f"Description: {detailed_data_2.get('description_raw','no description available')}")
                    
                    else:
                        print("Error fetching data from gaming API.")
                
                except requests.Timeout:
                    print("The request took too long, try again later.")
                except requests.ConnectionError:
                    print("Connection error, check your internet connection.")

                result = feedback()
                if result is True:
                    liked = True
                    break
                elif result is None:
                    break_main_loop_2 = True
                    break
            if break_main_loop_2:
                continue
        
        elif activity == 'reading books':     
            break_main_loop_3 = False       
            while True:
                
                import requests

                book_name = input("Book request (exit --> suggest another activity): ").strip().lower()
                if book_name == 'exit':
                    print("Going back to activity suggestions...")
                    break_main_loop_3 = True
                    break

                try:
                    res_3 = requests.get("https://openlibrary.org/search.json",
                        params={"q": book_name, "lang": "eng"},
                        timeout=40)
                    res_3.raise_for_status()
                    data_3 = res_3.json()

                    if data_3["numFound"] > 0:
                        book = data_3["docs"][0]               
                        title = book.get("title", "No title")
                        author = ", ".join(book.get("author_name", ["Unknown author"]))
                        year = book.get("first_publish_year", "Unknown year")
                        edition_count = book.get("edition_count", "Unknown")
                        
                        print(f"\nTitle: {title}")
                        print(f"Author: {author}")
                        print(f"First Released Year: {year}")
                        print(f"Edition count: {edition_count}")
                               
                        if book.get("key"):
                            work_res = requests.get(f"https://openlibrary.org{book.get('key')}.json")
                            work_data = work_res.json()
                            
                            description = work_data.get("description", "No description available.")
                            if isinstance(description, dict):
                                desc = description.get("value", "No description available.")
                            else:
                                desc = description
                            
                            subjects = work_data.get("subjects", [])
                            if isinstance(subjects, list) and subjects:
                                subjects_text = ", ".join(subj.capitalize() for subj in subjects[:5])
                            else:
                                subjects_text = "Unknown subjects"

                            print(f"Subjects: {subjects_text}")
                            print(f"Description: {description}")
                        
                        else:
                            print("Description: Not available")
                            print("Subjects: Unknown subjects")

                    else:
                        print("Book not found.")

                except requests.Timeout:
                    print("The request took too long, try again later.")
                except requests.ConnectionError:
                    print("Connection error, check your internet connection.")
                except requests.exceptions.HTTPError as error:
                    print(f"HTTP error: {error.response.status_code} — {error.response.reason}")
                                
                result = feedback()
                if result is True:
                    liked = True
                    break
                elif result is None:
                    break_main_loop_3 = True
                    break
            if break_main_loop_3:
                continue

        elif activity == 'listening to a song':   #Mostrar artista, musica, produtora, album, duração das musicas;
            break_main_loop_4 = False
            while True:
                
                import spotipy            
                from spotipy.oauth2 import SpotifyClientCredentials

                client_id = '64d191f18842490bbbc5554a6702f568'
                client_secret = 'b57ae4c77c414c9e84b045d72135728c'

                oauth = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
                spot = spotipy.Spotify(auth_manager=oauth)

                artist_name = input("Artist request (exit --> suggest another activity): ")
                if artist_name == 'exit':
                    print("Going back to activity suggestions...")
                    break_main_loop_4 = True
                    break
            
                
            #API de lingua; 
else:
    print("\nYou have completed all activities, no more left.")