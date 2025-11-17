# Home Lab Media Server: Step-by-Step Implementation Guide

This guide provides a granular, step-by-step checklist for setting up your fully automated, containerized media server stack on a dedicated Linux server.

---

## Section 1: Prerequisite Setup

### 1.1. On Your Synology NAS

- [ ] **Enable SMB Service:**
  - Go to `Control Panel` > `File Services` > `SMB`.
  - Ensure `Enable SMB service` is checked.

- [ ] **Create Media Folders:**
  - Open `File Station`.
  - Create a main shared folder named `media`.
  - Inside `media`, create the following folders:
    - [ ] `downloads`
    - [ ] `tv`
    - [ ] `movies`
    - [ ] `books`
  - Inside the `movies` folder, create subfolders for each genre (e.g., `action`, `comedy`, `scifi`).

- [ ] **Create a Dedicated User:**
  - Go to `Control Panel` > `User & Group`.
  - Create a new user (e.g., `docker_user`).
  - Give this user **Read/Write** access to the `media` shared folder and note down the password.

### 1.2. On Your Linux Server (Lenovo M710)

- [ ] **Install Ubuntu Server & Docker:**
  - Follow the instructions in `implementation_plan.md` (Phase 5.1 & 6.1) to install Ubuntu Server, OpenSSH, Docker, and Docker Compose.

- [ ] **Mount the NAS Media Share:**
  - Follow the instructions in `implementation_plan.md` (Phase 6.2 - 6.4) to install `cifs-utils`, create a mount point at `/mnt/nas`, and configure `/etc/fstab` to automatically mount your Synology's `/media` share.
  - Verify the mount with `ls -l /mnt/nas`. You should see your `movies`, `tv`, etc. folders.

---

## Section 2: Docker Stack Setup

*Connect to your Ubuntu server from your main PC using PowerShell or another terminal: `ssh your_username@YOUR_UBUNTU_SERVER_IP`*

- [ ] **Create Project Folder:**
  - On your Ubuntu server, create the project folder: `mkdir ~/media-stack && cd ~/media-stack`

- [ ] **Create `.env` File:**
  - Create the file: `nano .env`
  - Copy the content from `implementation_plan.md` (Phase 7.2) into this file.
  - **Crucially, edit the placeholder values** for `TZ`, `VPN_SERVICE_PROVIDER`, etc. Set `PUID=1000` and `PGID=1000`.

- [ ] **Create `docker-compose.yml` File:**
  - Create the file: `nano docker-compose.yml`
  - Copy the content from `implementation_plan.md` (Phase 7.3) into this file.

- [ ] **Launch the Stack:**
  - From the `~/media-stack` directory, run the command: `docker compose up -d`.
  - Wait for all container images to download and start. You can monitor progress with `docker compose logs -f`.

---

## Section 3: Initial Service Configuration

**Server IP (Tailscale):** `100.114.128.38`

*In your browser, navigate to the service URLs below using the Tailscale IP address. Tailscale provides secure, encrypted access from anywhere without needing to open ports on your router.*

### 3.1. qBittorrent

- [ ] Navigate to `http://100.114.128.38:8080` (Tailscale IP).
- [ ] Login with `admin`/`adminadmin` and change the password immediately.
- [ ] Go to `Tools` > `Options` > `Downloads`.
- [ ] Set `Default Save Path` to exactly: `/downloads`.
- [ ] Click `Apply` and `OK`.

### 3.2. Prowlarr

- [ ] Navigate to `http://100.114.128.38:9696` (Tailscale IP).
- [ ] Go to `Indexers` > `Add Indexer` (`+`).
- [ ] Add your preferred indexers (e.g., `1337x` for public).
- [ ] Test and save each indexer.

### 3.3. Sonarr (for TV Shows)

- [ ] Navigate to `http://100.114.128.38:8989` (Tailscale IP).
- [ ] **Connect Download Client:**
  - Go to `Settings` > `Download Clients` > `Add` (`+`).
  - Select `qBittorrent`.
  - **Host:** `qbittorrent`
  - **Port:** `8080`
  - Enter your new qBittorrent username and password.
  - Test and save.
- [ ] **Connect Indexers:**
  - Go to `Settings` > `Indexers` > `Add` (`+`).
  - Select `Prowlarr`.
  - **Prowlarr Server:** `http://prowlarr:9696`
  - **API Key:** Copy it from Prowlarr (`Settings` > `General`).
  - Test and save.
- [ ] **Configure Root Folder:**
  - Go to `Settings` > `Media Management`.
  - `Add Root Folder` and enter the path: `/tv`.

### 3.4. Radarr (for Movies)

- [ ] Navigate to `http://100.114.128.38:7878` (Tailscale IP).
- [ ] **Connect Download Client and Indexers** (follow the same steps as for Sonarr).
- [ ] **Configure Root Folder:**
  - Go to `Settings` > `Media Management`.
  - `Add Root Folder` and enter the path: `/movies`.
  - **Workflow Note:** When adding a new movie, you must manually edit the path to place it in the correct genre subfolder (e.g., `/movies/scifi`).

### 3.5. Readarr (for Books)

- [ ] Navigate to `http://100.114.128.38:8787` (Tailscale IP).
- [ ] **Connect Download Client and Indexers** (follow the same steps as for Sonarr/Radarr).
- [ ] **Configure Root Folder:**
  - Go to `Settings` > `Media Management`.
  - `Add Root Folder` and enter the path: `/books`.

### 3.6. Jellyfin

- [ ] Navigate to `http://100.114.128.38:8096` (Tailscale IP) and complete the startup wizard.
- [ ] **Add Media Libraries:**
  - Go to `Dashboard` > `Libraries` > `Add Media Library`.
  - **Content Type:** `Movies`
  - **Display Name:** `Action` (or your first genre)
  - **Folders:** Add the path `/data/movies/action`.
  - Repeat this for every genre folder you created.
  - Add a `TV Shows` library pointing to `/data/tv`.
  - Add a `Books` library pointing to `/data/books`.
- [ ] **Create User Accounts:**
  - Go to `Dashboard` > `Users`.
  - Create accounts for other users.
  - In each user's profile (`Access` tab), uncheck `Enable access to all libraries` and select only the libraries you want them to see.

---

## Section 4: Advanced Features (Optional)

### 4.1. Jellyfin Meta Manager (JMM)

- [ ] **Install:** `pip install jellyfin-meta-manager`.
- [ ] **Create `config.yml` and `movies.yml`** in a new folder on your server.
- [ ] **Configure `movies.yml`** to create collections from Trakt lists (see `implementation_plan.md`, Phase 9).
- [ ] **Run JMM:** Execute the script from your server's terminal.
- [ ] **Schedule Automation:** Use `cron` on Linux to run the JMM script nightly. (e.g., `crontab -e` and add `0 2 * * * /usr/bin/python3 /path/to/jmm/script.py`).

### 4.2. Trakt Integration

- [ ] **Install Trakt Plugin:**
  - In Jellyfin, go to `Dashboard` > `Plugins` > `Catalog`.
  - Find and install the **Trakt** plugin.
  - Restart Jellyfin.
- [ ] **Configure Trakt Plugin:**
  - Go to the new "Trakt" section in the dashboard and link your Trakt.tv account.

### 4.3. Dynamic Library Rotation

- [ ] **Setup:** Follow the instructions in `README.md` to configure `rotate_jellyfin_libraries.py` and its `.env` file on your server.
- [ ] **Schedule:** Use `cron` to run the script on your desired schedule (e.g., daily).

### 4.4. AI-Powered Tagging

- [ ] **Install Ollama:** On your server, follow the official guide to install Ollama.
- [ ] **Download an AI Model:** Run `ollama pull llama3:8b` in your server's terminal.
- [ ] **Setup:** Follow the instructions in `ai_tagger_README.md` to configure `ai_tagger.py` with your API keys and preferences.
- [ ] **Run:** Start your Ollama server, then run `python3 ai_tagger.py`. This may take a long time.
- [ ] **Use Tags in JMM:** After the script runs, update your JMM `movies.yml` to create collections from your new AI-generated tags.
