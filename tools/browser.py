import webbrowser

def search_platform(plataforma, query):
    query_encoded = query.replace(' ', '%20')
    
    urls = {
        'google': f"https://www.google.com/search?q={query_encoded}",
        'youtube': f"https://www.youtube.com/results?search_query={query_encoded}",
        'instagram': f"https://www.instagram.com/explore/search/keyword/?q={query_encoded}",
        'tiktok': f"https://www.tiktok.com/search?q={query_encoded}",
        'twitch': f"https://www.twitch.tv/search?term={query_encoded}",
    }

    plataforma = plataforma.lower()
    if plataforma in urls:
        webbrowser.open(urls[plataforma])
    else:
        print(f"Plataforma '{plataforma}' não reconhecida.")
