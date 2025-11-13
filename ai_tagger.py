
import requests
import json
import os
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
JELLYFIN_SERVER_URL = os.getenv("JELLYFIN_SERVER_URL", "http://localhost:8096")
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "YOUR_ADMIN_API_KEY")
USER_ID = os.getenv("USER_ID", "YOUR_USER_ID")
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "YOUR_TMDB_API_KEY")
LOCAL_AI_API_URL = os.getenv("LOCAL_AI_API_URL", "http://localhost:1234/v1/chat/completions") # Example for LM Studio

# --- AI Configuration ---
# Define the subjective categories you want the AI to use
SUBJECTIVE_CATEGORIES = [
    "girly-pop", "date-night", "feel-good", "inspirational",
    "raunchy", "mind-bending", "rainy-day", "so-bad-its-good"
]

# The prompt template for the AI
AI_PROMPT_TEMPLATE = """
You are an expert movie curator. Your task is to assign a movie to one or more of the following subjective categories: {categories}.

To help you understand my categories, here are some examples:
- **girly-pop**: 'Mean Girls', 'The Devil Wears Prada', 'Legally Blonde'
- **date-night**: 'About Time', 'La La Land', 'When Harry Met Sally...'
- **mind-bending**: 'Inception', 'The Matrix', 'Primer', 'Shutter Island'
- **feel-good**: 'Paddington 2', 'School of Rock', 'Ted Lasso'
- **raunchy**: 'Superbad', 'The Hangover', 'Booksmart'

Based on these examples, please categorize the following movie.

- Movie Title: {title}
- Year: {year}
- Genres: {genres}
- Plot Summary: {overview}

Respond with a comma-separated list of the categories you think this movie belongs to. If it fits none, respond with "None".
"""

def get_jellyfin_movies(headers):
    """Fetches all movies from the user's Jellyfin libraries."""
    print("Fetching all movies from Jellyfin...")
    try:
        response = requests.get(f"{JELLYFIN_SERVER_URL}/Users/{USER_ID}/Items", params={"Recursive": "true", "IncludeItemTypes": "Movie"}, headers=headers)
        response.raise_for_status()
        movies = response.json().get("Items", [])
        print(f"Found {len(movies)} movies.")
        return movies
    except requests.exceptions.RequestException as e:
        print(f"Error fetching movies from Jellyfin: {e}")
        return []

def get_tmdb_details(movie, headers):
    """Fetches detailed movie information from TMDb."""
    tmdb_id = movie.get("ProviderIds", {}).get("Tmdb")
    if not tmdb_id:
        return None

    print(f"Fetching details for '{movie['Name']}' from TMDb...")
    try:
        response = requests.get(f"https://api.themoviedb.org/3/movie/{tmdb_id}", params={"api_key": TMDB_API_KEY})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching details from TMDb for movie ID {tmdb_id}: {e}")
        return None

def get_ai_categorization(movie_details):
    """Gets subjective categorization from the local AI model."""
    prompt = AI_PROMPT_TEMPLATE.format(
        categories=', '.join(SUBJECTIVE_CATEGORIES),
        title=movie_details.get('title', 'N/A'),
        year=movie_details.get('release_date', 'N/A')[:4],
        genres=', '.join([genre['name'] for genre in movie_details.get('genres', [])]),
        overview=movie_details.get('overview', 'N/A')
    )

    # --- Adapt this section for your local AI's API ---
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "local-model", # Or whatever your model is called
        "messages": [
            {"role": "system", "content": "You are an expert movie curator."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
    }

    print(f"Sending prompt to local AI for '{movie_details.get('title', 'N/A')}'...")
    try:
        response = requests.post(LOCAL_AI_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        ai_response = response.json()
        # The actual response format will depend on your local AI's API.
        # This example assumes an OpenAI-compatible API.
        categories_str = ai_response['choices'][0]['message']['content']
        return [cat.strip() for cat in categories_str.split(',') if cat.strip() and cat.strip().lower() != 'none']
    except requests.exceptions.RequestException as e:
        print(f"Error getting categorization from local AI: {e}")
        return []
    # ----------------------------------------------------

def update_jellyfin_movie_tags(movie, new_tags, headers):
    """Updates the tags for a movie in Jellyfin."""
    print(f"Updating tags for '{movie['Name']}'...")
    # First, we need to get the full item details to get the existing tags
    try:
        response = requests.get(f"{JELLYFIN_SERVER_URL}/Users/{USER_ID}/Items/{movie['Id']}", headers=headers)
        response.raise_for_status()
        item_details = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching item details for '{movie['Name']}': {e}")
        return

    existing_tags = set(item_details.get("Tags", []))
    # Remove old subjective tags to avoid duplicates
    for cat in SUBJECTIVE_CATEGORIES:
        if cat in existing_tags:
            existing_tags.remove(cat)

    # Add the new AI-generated tags
    for tag in new_tags:
        if tag in SUBJECTIVE_CATEGORIES:
            existing_tags.add(tag)

    item_details["Tags"] = list(existing_tags)

    # Now, update the item
    try:
        update_response = requests.post(f"{JELLYFIN_SERVER_URL}/Items/{movie['Id']}", headers=headers, json=item_details)
        update_response.raise_for_status()
        print(f"Successfully updated tags for '{movie['Name']}'. New tags: {', '.join(new_tags)}")
    except requests.exceptions.RequestException as e:
        print(f"Error updating tags for '{movie['Name']}': {e}")
        if update_response:
            print(f"Response content: {update_response.text}")


def ai_tag_movies():
    """
    Main function to iterate through movies, get AI categorization, and update tags.
    """
    jellyfin_headers = {
        "X-Emby-Token": ADMIN_API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    movies = get_jellyfin_movies(jellyfin_headers)
    if not movies:
        return

    for movie in movies:
        tmdb_details = get_tmdb_details(movie, jellyfin_headers)
        if not tmdb_details:
            continue

        ai_tags = get_ai_categorization(tmdb_details)
        if ai_tags:
            update_jellyfin_movie_tags(movie, ai_tags, jellyfin_headers)
        else:
            print(f"No new tags assigned by AI for '{movie['Name']}'.")

        # Be a good citizen and don't spam APIs
        time.sleep(2)

if __name__ == "__main__":
    if any(key == "YOUR_" + key for key in [ADMIN_API_KEY, USER_ID, TMDB_API_KEY]):
        print("Please configure your JELLYFIN_SERVER_URL, ADMIN_API_KEY, USER_ID, and TMDB_API_KEY in a .env file or directly in the script.")
    else:
        ai_tag_movies()
