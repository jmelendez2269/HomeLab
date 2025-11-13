# Home Lab Media Server: Step-by-Step Implementation Guide

This guide provides a granular, step-by-step checklist for setting up your fully automated, containerized media server stack.

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
  - Inside the `movies` folder, create subfolders for each genre (e.g., `action`, `comedy`, `scifi`).

- [ ] **Create a Dedicated User:**
  - Go to `Control Panel` > `User & Group`.
  - Create a new user (e.g., `docker_user`).
  - Give this user **Read/Write** access to the `media` shared folder.

### 1.2. On Your Windows PC

- [ ] **Map Network Drive:**
  - In Windows File Explorer, right-click "This PC" and select "Map network drive...".
  - **Drive:** `M:`
  - **Folder:** `\YOUR_SYNOLOGY_IP\media`
  - Check `Connect using different credentials` and use the `docker_user` credentials.

---

## Section 2: Docker Stack Setup

- [ ] **Create Project Folder:**
  - On your Windows PC, create a folder named `media-stack` (e.g., in `C:\Docker`).

- [ ] **Create `.env` File:**
  - Inside `media-stack`, create a file named `.env`.
  - Copy the content from `implementation_plan.md` (Phase 3.2) into this file.
  - **Crucially, edit the placeholder values** for `TZ`, `VPN_SERVICE_PROVIDER`, etc.

- [ ] **Create `docker-compose.yml` File:**
  - Inside `media-stack`, create a file named `docker-compose.yml`.
  - Copy the content from `implementation_plan.md` (Phase 3.3) into this file.

- [ ] **Launch the Stack:**
  - Open a terminal (PowerShell) in the `media-stack` directory.
  - Run the command: `docker-compose up -d`.
  - Wait for all container images to download and start.

---

## Section 3: Initial Service Configuration

### 3.1. qBittorrent

- [ ] Navigate to `http://localhost:8080`.
- [ ] Login with `admin`/`adminadmin` and change the password immediately.
- [ ] Go to `Tools` > `Options` > `Downloads`.
- [ ] Set `Default Save Path` to exactly: `/downloads`.
- [ ] Click `Apply` and `OK`.

### 3.2. Prowlarr

- [ ] Navigate to `http://localhost:9696`.
- [ ] Go to `Indexers` > `Add Indexer` (`+`).
- [ ] Add your preferred indexers (e.g., `1337x` for public).
- [ ] Test and save each indexer.

### 3.3. Sonarr (for TV Shows)

- [ ] Navigate to `http://localhost:8989`.
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

- [ ] Navigate to `http://localhost:7878`.
- [ ] **Connect Download Client and Indexers** (follow the same steps as for Sonarr).
- [ ] **Configure Root Folder:**
  - Go to `Settings` > `Media Management`.
  - `Add Root Folder` and enter the path: `/movies`.

### 3.5. Jellyfin

- [ ] Navigate to `http://localhost:8096` and complete the startup wizard.
- [ ] **Add Media Libraries:**
  - Go to `Dashboard` > `Libraries` > `Add Media Library`.
  - **Content Type:** `Movies`
  - **Display Name:** `Action` (or your first genre)
  - **Folders:** Add the path `/data/movies/action`.
  - Repeat this for every genre folder you created.
  - Add a `TV Shows` library pointing to `/data/tv`.
- [ ] **Create User Accounts:**
  - Go to `Dashboard` > `Users`.
  - Create accounts for other users.
  - In each user's profile (`Access` tab), uncheck `Enable access to all libraries` and select only the libraries you want them to see.

---

## Section 4: Advanced Features (Optional)

### 4.1. Jellyfin Meta Manager (JMM)

- [ ] **Install:** `pip install jellyfin-meta-manager`.
- [ ] **Create `config.yml` and `movies.yml`** in a new folder.
- [ ] **Configure `movies.yml`** to create collections from Trakt lists (see `implementation_plan.md`, Phase 8.2).
- [ ] **Run JMM:** Execute the script from PowerShell.
- [ ] **Schedule Automation:** Use Windows Task Scheduler to run the JMM script nightly.

### 4.2. Trakt Integration

- [ ] **Install Trakt Plugin:**
  - In Jellyfin, go to `Dashboard` > `Plugins` > `Catalog`.
  - Find and install the **Trakt** plugin.
  - Restart Jellyfin.
- [ ] **Configure Trakt Plugin:**
  - Go to the new "Trakt" section in the dashboard and link your Trakt.tv account.
- [ ] **(Optional) Install JellyNext Plugin:**
  - Look for **JellyNext** in the plugin catalog for personalized recommendations.

### 4.3. Dynamic Library Rotation

- [ ] **Setup:** Follow the instructions in `README.md` to configure `rotate_jellyfin_libraries.py` and its `.env` file.
- [ ] **Schedule:** Use Windows Task Scheduler to run the script on your desired schedule (e.g., daily).

### 4.4. AI-Powered Tagging

- [ ] **Install Ollama:** Download and install Ollama from the official website.
- [ ] **Download an AI Model:** Run `ollama pull llama3:8b` in your terminal.
- [ ] **Setup:** Follow the instructions in `ai_tagger_README.md` to configure `ai_tagger.py` with your API keys and preferences.
- [ ] **Run:** Start your Ollama server, then run `python ai_tagger.py`. This may take a long time.
- [ ] **Use Tags in JMM:** After the script runs, update your JMM `movies.yml` to create collections from your new AI-generated tags.
