
# Jellyfin AI Tagger

This script uses a local AI model to automatically tag your Jellyfin movies with your own subjective categories. It fetches movie metadata, prompts your local AI for categorization, and then updates the movie's tags in Jellyfin.

This allows you to create highly personalized collections based on your own tastes, powered by AI.

## How It Works

1.  **Fetches Movies:** The script gets a list of all movies from your Jellyfin server.
2.  **Gets Metadata:** For each movie, it fetches detailed metadata (plot, genres, etc.) from The Movie Database (TMDb).
3.  **Prompts Local AI:** It constructs a detailed prompt with the movie's metadata and sends it to your local AI model's API endpoint.
4.  **Applies Tags:** It takes the AI's response and updates the movie's tags in Jellyfin with your subjective categories.

## Prerequisites

- Python 3.6+
- The `requests` and `python-dotenv` Python libraries.
- A running local AI model with an OpenAI-compatible API endpoint (e.g., LM Studio, Ollama with a compatible frontend).
- A TMDb API key.

## Setup and Configuration

1.  **Install Python Libraries:**
    ```sh
    pip install requests python-dotenv
    ```

2.  **Get a TMDb API Key:**
    - Create a free account on [The Movie Database (TMDb)](https://www.themoviedb.org/).
    - Go to your account `Settings` > `API` and request an API key.

3.  **Update your `.env` file:**
    Add the following lines to your existing `.env` file, or create one if it doesn't exist.

    ```env
    # --- Existing Configuration ---
    JELLYFIN_SERVER_URL="http://localhost:8096"
    ADMIN_API_KEY="YOUR_ADMIN_API_KEY"
    USER_ID="YOUR_USER_ID"
    NUM_VISIBLE_LIBRARIES="5"

    # --- New Configuration for AI Tagger ---
    # Your TMDb API key
    TMDB_API_KEY="YOUR_TMDB_API_KEY"

    # The API endpoint for your local AI model.
    # This example is for LM Studio.
    # For Ollama, it might be http://localhost:11434/api/chat
    LOCAL_AI_API_URL="http://localhost:1234/v1/chat/completions"
    ```

4.  **Configure the Script (`ai_tagger.py`):**
    Open the `ai_tagger.py` script and modify the following sections if needed:

    - **`SUBJECTIVE_CATEGORIES`:**
      This is the most important part. Edit this Python list to include the subjective categories you want to use.
      ```python
      SUBJECTIVE_CATEGORIES = [
          "girly-pop", "date-night", "feel-good", "inspirational",
          "raunchy", "mind-bending", "rainy-day", "so-bad-its-good"
      ]
      ```

    - **`AI_PROMPT_TEMPLATE`:**
      You can experiment with this prompt to get better results from your AI model.
      ```python
      AI_PROMPT_TEMPLATE = """
      You are an expert movie curator...
      """
      ```

    - **`get_ai_categorization` function:**
      This function contains the API call to your local AI. The provided code assumes an OpenAI-compatible API (like the one provided by LM Studio). If your local AI has a different API structure, you will need to modify the `payload` and how the response is parsed.

      ```python
      def get_ai_categorization(movie_details):
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
          # ...
          # ----------------------------------------------------
      ```

## Running the Script

1.  **Start your Local AI Server:**
    Make sure your local AI model is running and accessible at the `LOCAL_AI_API_URL` you configured.

2.  **Run the Python Script:**
    ```sh
    python ai_tagger.py
    ```

The script will then begin processing your movie library. This may take a long time, especially for large libraries.

## Using the AI-Generated Tags

Once the script has run, your movies will have new tags in Jellyfin. You can now use these tags to create dynamic collections.

A great way to do this is with **Jellyfin Meta Manager (JMM)**. In your JMM `movies.yml` configuration, you can create collections based on these tags:

```yaml
collections:
  Girly Pop:
    jellyfin_tag: girly-pop
  Date Night Movies:
    jellyfin_tag: date-night
  Mind-Bending Films:
    jellyfin_tag: mind-bending
```

When JMM runs, it will automatically create and update these collections for you, displaying them as new rows on your Jellyfin home screen.
