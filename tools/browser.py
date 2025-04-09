import webbrowser

def search_google(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)

def search_youtube(query):
    url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    webbrowser.open(url)