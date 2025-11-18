# Kometa (Jellyfin Meta Manager) Setup Guide

## Quick Setup Instructions

### Step 1: Get Your Jellyfin API Key

1. Open Jellyfin: `http://100.114.128.38:8096`
2. Go to **Dashboard** (gear icon) > **API Keys**
3. Click the **`+`** button to create a new API key
4. Name it: `Kometa`
5. **Copy the API key** - you'll need it in the next step

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

### Step 4: Update the API Key

Edit the `config.yml` file and replace all instances of `YOUR_API_KEY` with your actual Jellyfin API key:

```bash
nano ~/kometa/config.yml
# Use Ctrl+W to search for "YOUR_API_KEY"
# Replace each occurrence with your actual API key
# Save and exit
```

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

## Next Steps

Once Kometa is working, you can:
1. Add collections to `config/movies.yml` (see examples in the file)
2. Add tags based on TMDb data
3. Connect Trakt lists for curated collections
4. Customize collection ordering and display

For more advanced configuration, see the [Official Kometa Documentation](https://kometa.wiki/en/latest/).

