# Kometa (Jellyfin Meta Manager) Setup Guide

## Quick Setup Instructions

### Step 1: Get Your API Keys

#### Get Your Jellyfin API Key

1. Open Jellyfin: `http://100.114.128.38:8096`
2. Go to **Dashboard** (gear icon) > **API Keys**
3. Click the **`+`** button to create a new API key
4. Name it: `Kometa`
5. **Copy the API key** - you'll need it in the next step

#### Get Your TMDb API Key (Optional but Recommended)

TMDb (The Movie Database) API key is needed for:
- Creating collections based on TMDb data (genres, keywords, awards, etc.)
- Adding tags based on TMDb keywords
- Using `tmdb_discover` and `tmdb_keyword` features in Kometa

**Steps to get a free TMDb API key:**

1. Go to [TMDb](https://www.themoviedb.org/)
2. Click **Sign Up** (or **Log In** if you already have an account)
3. Create a free account (or log in)
4. Go to your **Account Settings** (click your profile icon > **Settings**)
5. Click on **API** in the left sidebar
6. Under **API Key (v3 auth)**, click **Request an API Key**
7. Fill out the form:
   - **Type of use:** Select "Developer" (for personal use)
   - **Application name:** Enter "Kometa" or "Jellyfin Meta Manager"
   - **Application URL:** Enter your Jellyfin URL (e.g., `http://100.114.128.38:8096`) or leave blank
   - **Application summary:** Enter "Personal media server automation"
8. Accept the terms and click **Submit**
9. **Copy your API key** - you'll need to add it to your Kometa config

**Note:** TMDb API keys are free for personal use. The approval process is usually instant or takes a few minutes.

### Step 2: Create Kometa Directory on Your Linux Server

SSH into your server and run:

```bash
ssh your_username@100.114.128.38

# Create Kometa directory
mkdir -p ~/kometa/config
cd ~/kometa
```

### Step 3: Copy the Config Files

**Option A: Copy from your local machine (if you have the files)**

From your Windows machine, copy the config files to your server:

```bash
# From Windows PowerShell or Command Prompt
scp kometa_config_example.yml your_username@100.114.128.38:~/kometa/config.yml
scp kometa_movies_example.yml your_username@100.114.128.38:~/kometa/config/movies.yml
scp kometa_tv_example.yml your_username@100.114.128.38:~/kometa/config/tv.yml
```

**Option B: Create files directly on the server**

```bash
# On your Linux server
cd ~/kometa
nano config.yml
# Paste the contents of kometa_config_example.yml
# Replace YOUR_API_KEY with your actual API key
# Save and exit (Ctrl+X, Y, Enter)

mkdir -p config
nano config/movies.yml
# Paste the contents of kometa_movies_example.yml
# Save and exit

nano config/tv.yml
# Paste the contents of kometa_tv_example.yml
# Save and exit
```

### Step 4: Update the API Keys

Edit the `config.yml` file and replace all instances of `YOUR_API_KEY` with your actual Jellyfin API key:

```bash
nano ~/kometa/config.yml
# Use Ctrl+W to search for "YOUR_API_KEY"
# Replace each occurrence with your actual Jellyfin API key
# Save and exit
```

**If you want to use TMDb features** (collections based on TMDb data, tags from keywords, etc.), you also need to add your TMDb API key to the config. Add this to your `config.yml` file under the `settings` section:

```yaml
settings:
  cache: true
  cache_expiration: 60
  missing_only_released: false
  log_level: info
  log_file: config/logs/kometa.log
  tmdb:
    apikey: YOUR_TMDB_API_KEY  # Add your TMDb API key here
```

Replace `YOUR_TMDB_API_KEY` with the API key you got from TMDb.

### Step 5: Verify Library Names Match

**Important:** Make sure the library names in `config.yml` match exactly what you named them in Jellyfin:

- In Jellyfin, go to **Dashboard** > **Libraries**
- Check the exact names of your movie libraries
- Update `config.yml` if needed (e.g., if you named it "Sci-Fi" vs "SciFi" or "Documentaries" vs "Documentary")

The config file includes these libraries:
- Action
- Comedy
- Documentaries
- Drama
- Family
- Horror
- Sci-Fi
- Thriller
- TV Shows

### Step 6: Test the Configuration

```bash
cd ~/kometa
jellyfin-meta-manager
```

This will:
- Test the connection to Jellyfin
- Show any errors
- Create collections/tags if configured

### Step 7: Schedule Automatic Runs (Optional)

To run Kometa automatically every night at 2 AM:

```bash
crontab -e
```

Add this line:
```
0 2 * * * /usr/local/bin/jellyfin-meta-manager -c ~/kometa/config.yml
```

Or if jellyfin-meta-manager is in a different location:
```bash
# Find the location
which jellyfin-meta-manager

# Then use the full path in crontab
0 2 * * * /path/to/jellyfin-meta-manager -c ~/kometa/config.yml
```

## Troubleshooting

### "Connection refused" error
- Make sure Jellyfin is running: `sudo docker compose ps jellyfin`
- Verify the API key is correct
- Try using `http://127.0.0.1:8096` instead of `localhost:8096`

### "Library not found" error
- Check that library names in `config.yml` match exactly what's in Jellyfin
- Library names are case-sensitive

### "Permission denied" error
- Make sure you have read/write access to the `~/kometa` directory
- Check file permissions: `chmod 644 ~/kometa/config.yml`

## Using TMDb with Kometa

### What TMDb is Used For

TMDb (The Movie Database) provides rich metadata that Kometa can use to:

1. **Create Collections Based on TMDb Data:**
   - Genre-based collections (e.g., all Sci-Fi movies)
   - Decade collections (e.g., 80s movies, 90s movies)
   - Award winners (e.g., Oscar winners, Golden Globe winners)
   - Keyword-based collections (e.g., "time travel", "heist", "superhero")

2. **Add Tags Based on TMDb Keywords:**
   - Automatically tag movies based on TMDb keywords
   - Examples: "based on book", "time travel", "heist", "superhero"

### Example TMDb Collections

Add these to your `config/movies.yml` file:

```yaml
collections:
  # Decade Collections
  80s Movies:
    tmdb_discover:
      primary_release_date.gte: 1980-01-01
      primary_release_date.lte: 1989-12-31
    collection_order: release
  
  90s Movies:
    tmdb_discover:
      primary_release_date.gte: 1990-01-01
      primary_release_date.lte: 1999-12-31
    collection_order: release
  
  # Award Winners
  Oscar Winners:
    tmdb_discover:
      with_awards: true
      primary_release_date.gte: 1929-01-01
    collection_order: release
  
  # Genre-based (using TMDb genre IDs)
  Sci-Fi Movies:
    tmdb_discover:
      with_genres: [878]  # Sci-Fi genre ID
    collection_order: release
```

### Example TMDb Tags

Add these to your `config/movies.yml` file:

```yaml
tags:
  Based on a Book:
    tmdb_keyword: based on book
  
  Time Travel:
    tmdb_keyword: time travel
  
  Heist:
    tmdb_keyword: heist
  
  Superhero:
    tmdb_keyword: superhero
```

### TMDb Genre IDs Reference

Common TMDb genre IDs you might use:
- **Action:** 28
- **Adventure:** 12
- **Animation:** 16
- **Comedy:** 35
- **Crime:** 80
- **Documentary:** 99
- **Drama:** 18
- **Family:** 10751
- **Fantasy:** 14
- **History:** 36
- **Horror:** 27
- **Music:** 10402
- **Mystery:** 9648
- **Romance:** 10749
- **Sci-Fi:** 878
- **Thriller:** 53
- **War:** 10752
- **Western:** 37

For a complete list, see [TMDb Genre List](https://www.themoviedb.org/talk/5daf6eb0ae36680011d0e111).

## Next Steps

Once Kometa is working, you can:
1. Add collections to `config/movies.yml` (see examples in the file)
2. Add tags based on TMDb data
3. Connect Trakt lists for curated collections
4. Customize collection ordering and display
5. Combine TMDb and Trakt lists for comprehensive automation

## Trakt Lists Resources

### Useful Trakt Lists for Collections

**Official Trakt Community Lists:**
- [Trakt Community Lists - TV Shows](https://trakt.tv/shows/community/lists) - Browse thousands of curated TV show lists sorted by popularity, reactions, and more. Includes top-rated shows, genre collections, and decade lists.
- [Trakt Community Lists - Movies](https://trakt.tv/movies/community/lists) - Browse curated movie lists from the Trakt community.

**Reddit Community Lists:**
- [My Trakt Lists - Useful for Kodi Addons](https://www.reddit.com/r/Addons4Kodi/comments/116961i/my_trakt_lists_hopefully_they_will_be_useful_for/) - A comprehensive collection of Trakt lists organized by genre, mood, and theme. Great source for finding public lists to use in Kometa.

**How to Use Trakt Lists in Kometa:**

1. Find a Trakt list you like (from the Reddit post or Trakt.tv)
2. Get the list URL (e.g., `https://trakt.tv/users/USERNAME/lists/list-name`)
3. Add it to your `config/movies.yml`:

```yaml
collections:
  Feel Good Movies:
    trakt_list: https://trakt.tv/users/USERNAME/lists/feel-good-movies
    collection_order: release
```

For more advanced configuration, see the [Official Kometa Documentation](https://kometa.wiki/en/latest/).

