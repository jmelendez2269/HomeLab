# TMDb (The Movie Database) Setup for Kometa

This guide explains how to set up TMDb API access for use with Kometa (Jellyfin Meta Manager).

## What is TMDb?

TMDb (The Movie Database) is a community-driven database of movie and TV show information. Kometa can use TMDb data to:
- Create collections based on genres, keywords, release dates, and awards
- Automatically tag movies based on TMDb keywords
- Discover movies using TMDb's search and filter capabilities

## Getting Your TMDb API Key

### Step 1: Create a TMDb Account

1. Go to [TMDb](https://www.themoviedb.org/)
2. Click **Sign Up** (top right corner)
3. Fill out the registration form:
   - Username
   - Email address
   - Password
4. Verify your email address (check your inbox)

### Step 2: Request an API Key

1. Log in to your TMDb account
2. Click on your **profile icon** (top right) > **Settings**
3. Click on **API** in the left sidebar
4. Under **API Key (v3 auth)**, click **Request an API Key**
5. Fill out the application form:
   - **Type of use:** Select **"Developer"** (for personal use)
   - **Application name:** Enter `Kometa` or `Jellyfin Meta Manager`
   - **Application URL:** Enter your Jellyfin URL (e.g., `http://100.114.128.38:8096`) or leave blank
   - **Application summary:** Enter `Personal media server automation with Kometa`
6. Accept the terms of service
7. Click **Submit**

### Step 3: Get Your API Key

- Your API key will be displayed immediately (or within a few minutes)
- **Copy the API key** - it looks like: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`
- You can view it again later in **Settings** > **API**

**Important:** TMDb API keys are **free** for personal use. There's no cost or credit card required.

## Adding TMDb API Key to Kometa

### Option 1: Add to config.yml (Recommended)

Edit your `~/kometa/config.yml` file and add the TMDb API key to the settings section:

```yaml
settings:
  cache: true
  cache_expiration: 60
  missing_only_released: false
  log_level: info
  log_file: config/logs/kometa.log
  tmdb:
    apikey: YOUR_TMDB_API_KEY  # Replace with your actual TMDb API key
```

### Option 2: Environment Variable

You can also set it as an environment variable:

```bash
export TMDB_API_KEY="your_api_key_here"
```

Then run Kometa:
```bash
jellyfin-meta-manager
```

## Testing TMDb Connection

After adding your API key, test it by running Kometa:

```bash
cd ~/kometa
jellyfin-meta-manager
```

If TMDb is configured correctly, Kometa will be able to:
- Query TMDb for movie information
- Create collections based on TMDb data
- Apply tags based on TMDb keywords

## Common TMDb Features in Kometa

### 1. Collections Based on TMDb Discover

```yaml
collections:
  80s Movies:
    tmdb_discover:
      primary_release_date.gte: 1980-01-01
      primary_release_date.lte: 1989-12-31
    collection_order: release
```

### 2. Collections Based on TMDb Genres

```yaml
collections:
  Sci-Fi Movies:
    tmdb_discover:
      with_genres: [878]  # Sci-Fi genre ID
    collection_order: release
```

### 3. Tags Based on TMDb Keywords

```yaml
tags:
  Based on a Book:
    tmdb_keyword: based on book
  
  Time Travel:
    tmdb_keyword: time travel
```

## TMDb Genre IDs

Here are common genre IDs you might use:

| Genre | ID |
|-------|-----|
| Action | 28 |
| Adventure | 12 |
| Animation | 16 |
| Comedy | 35 |
| Crime | 80 |
| Documentary | 99 |
| Drama | 18 |
| Family | 10751 |
| Fantasy | 14 |
| History | 36 |
| Horror | 27 |
| Music | 10402 |
| Mystery | 9648 |
| Romance | 10749 |
| Sci-Fi | 878 |
| Thriller | 53 |
| War | 10752 |
| Western | 37 |

For a complete list, visit: [TMDb Genre List](https://www.themoviedb.org/talk/5daf6eb0ae36680011d0e111)

## TMDb API Rate Limits

TMDb has rate limits for API requests:
- **40 requests per 10 seconds** per API key
- This is usually more than enough for personal use
- Kometa caches results to minimize API calls

## Troubleshooting

### "Invalid API key" error
- Verify your API key is correct (no extra spaces)
- Make sure you copied the entire key
- Check that your API key request was approved

### "Rate limit exceeded" error
- Wait a few seconds and try again
- Kometa's caching should prevent this in normal use
- If it persists, check if multiple instances are running

### Collections not updating
- Make sure your TMDb API key is in the config
- Check Kometa logs for errors
- Verify the TMDb discover parameters are correct

## Additional Resources

- [TMDb Official Website](https://www.themoviedb.org/)
- [TMDb API Documentation](https://developers.themoviedb.org/3/getting-started/introduction)
- [Kometa TMDb Documentation](https://kometa.wiki/en/latest/)

