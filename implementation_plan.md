# Home Lab Media Server Implementation Plan

## 1. Overview

**Goal:** To build a fully automated, containerized media server stack. This setup will automatically download, sort, and manage movies and TV shows, serving them through a user-friendly interface.

**Key Features:**
- **Automated Media Acquisition:** Movies and TV shows will be automatically found and downloaded based on user requests.
- **Centralized Media Storage:** All media files will be stored on a Synology NAS.
- **Containerized Services:** All applications will run in Docker containers for clean and easy management.
- **Curated User Experience:** A single media server instance will provide different, curated interfaces for different users.
- **Secure Remote Access:** Remote access will be provided securely via Tailscale, eliminating the need for open ports on the router.

---

## 2. Core Technologies

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Orchestration** | Docker Compose | To define and run our multi-container application. |
| **Media Server** | Jellyfin | To organize, serve, and stream media with curated user profiles. |
| **Movie Automation** | Radarr | To monitor for and grab new movie releases. |
| **TV Automation** | Sonarr | To monitor for and grab new TV show episodes. |
| **Book Automation** | Readarr | To monitor for and grab new book releases. |
| **Indexer Manager** | Prowlarr | To manage all of our indexer configurations in one place. |
| **Download Client** | qBittorrent | To download the media files. |
| **Download Security**| GlueTUN | To ensure the download client's traffic is routed through a VPN. |
| **Remote Access** | Tailscale | To provide secure remote access for users without opening ports. |
| **File Storage** | Synology NAS (SMB) | To provide centralized, network-accessible storage for media files. |

---

## 3. Reference Videos

This plan combines strategies and concepts discussed in the following videos provided by you:

- **Video 1: [Automated Home Media Server on a Synology NAS](https://www.youtube.com/watch?v=5hN3Ohfi8pQ)**
  - This video demonstrates the full "Arr" stack running in Docker on a Synology NAS, using Plex as the media server. We are adopting its containerized approach.

- **Video 2: [Home Lab Media Server on Windows](https://www.youtube.com/watch?v=LD8-Qr3B2-o)**
  - This video shows the applications running directly on Windows and introduces Emby. We are using the same core applications but running them in Docker on Windows for better management.

- **Video 3: [Jellyfin Theming and Customization](https://www.youtube.com/watch?v=RXdaoPS4FwI&t=163s)**
  - This video provides a comprehensive guide to customizing the look and feel of your Jellyfin server. Refer to this for advanced theming options once your core setup is complete.

---

## 4. Phase 1: Media Organization Strategy

Before configuring the server, it's crucial to decide on your media organization strategy. Adopting a structured approach from the start will create a polished, easy-to-navigate experience.

### 4.1. The "Netflix" Model: Folders, Collections, and Tags

Our goal is a Netflix-style home screen with curated rows for different genres. We will achieve this by using Jellyfin's features strategically. Here is the rule of thumb:

-   **Folders (for Libraries):** Use folders for your main, broad categories. A movie should only exist in **one** folder. These will appear as rows on your Jellyfin home screen.
    -   ***Examples:*** `Action`, `Comedy`, `Sci-Fi`, `Horror`, `Family`, `Documentaries`.
-   **Collections:** Use collections to group movies that are part of a direct series or cinematic universe. A movie can only be in **one** collection.
    -   ***Examples:*** *The Lord of the Rings*, *Marvel Cinematic Universe*, *James Bond*.
-   **Tags:** Use tags for flexible, overlapping attributes. A movie can have **many** tags.
    -   ***Examples:*** "80s," "Based on a Book," "Oscar Winner," "Date Night," "Mind-Bending."

### 4.2. File Naming and Organization Tools

-   **For New Media:** Radarr and Sonarr will handle this automatically. They will rename files according to best practices (`Movie Title (Year)`) and move them to the correct folders.
-   **For Existing Media:** If you have a large, unorganized collection, manual renaming is impractical. Tools like **Filebot** or **Tiny Media Manager** are highly recommended for scanning and renaming your existing files to match the expected format.

---

## 5. Phase 2: Prerequisite Configuration

### 5.1. On Your Synology NAS

1.  **Enable SMB Service:**
    - Go to `Control Panel` > `File Services` > `SMB` and ensure `Enable SMB service` is checked.

2.  **Create Media Folders:**
    - Open `File Station` and navigate to your desired volume.
    - Create a main shared folder named `media`.
    - Inside `media`, create the following folders:
        - `downloads`
        - `tv`
        - `books`
        - `movies`
    - Inside the `movies` folder, create subfolders for each genre you want to use. **Do not use spaces or special characters in folder names.**
        - *Example Starting Point:*
            - `movies/action`
            - `movies/comedy`
            - `movies/drama`
            - `movies/family`
            - `movies/horror`
            - `movies/scifi`
            - `movies/thriller`

3.  **Create a Dedicated User:**
    - Go to `Control Panel` > `User & Group` and create a new user (e.g., `docker_user`).
    - Give this user **Read/Write** access to the `media` shared folder.

### 5.2. On Your Windows PC

1.  **Map Network Drive:**
    - In Windows File Explorer, right-click "This PC" and select "Map network drive...".
    - **Drive:** `M:`
    - **Folder:** `\\YOUR_SYNOLOGY_IP\media`
    - Check `Connect using different credentials` and use the `docker_user` credentials you just created.

---

## 6. Phase 3: Docker Environment Setup

### 6.1. Project Folder Structure

On your Windows PC, create the following folder structure. You can place the `media-stack` folder anywhere you like (e.g., `C:\Docker\media-stack`).

```
media-stack/
├── .env
└── docker-compose.yml
```

### 6.2. Environment File (`.env`)

Create the `.env` file and paste the following content into it. **You must edit the placeholder values.**

```env
# --- General Settings ---
# Set your timezone, e.g., "America/New_York". See https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
TZ=Etc/UTC

# --- VPN Settings (for GlueTUN) ---
# See https://gluetun.net/docs/providers/ for supported providers
VPN_SERVICE_PROVIDER=
VPN_TYPE=openvpn # or wireguard
WIREGUARD_PRIVATE_KEY=
WIREGUARD_ADDRESSES=
# -- or for OpenVPN --
OPENVPN_USER=
OPENVPN_PASSWORD=

# --- Service Configuration ---
# You can leave these as default
JELLYFIN_PORT=8096
RADARR_PORT=7878
SONARR_PORT=8989
PROWLARR_PORT=9696
READARR_PORT=8787
QBITTORRENT_PORT=8080
```

### 6.3. Docker Compose File (`docker-compose.yml`)

Create the `docker-compose.yml` file and paste the following content into it.

```yaml
version: "3.7"
services:
  gluetun:
    image: qmcgaw/gluetun
    container_name: gluetun
    cap_add:
      - NET_ADMIN
    environment:
      - TZ=${TZ}
      - VPN_SERVICE_PROVIDER=${VPN_SERVICE_PROVIDER}
      - VPN_TYPE=${VPN_TYPE}
      - OPENVPN_USER=${OPENVPN_USER}
      - OPENVPN_PASSWORD=${OPENVPN_PASSWORD}
      - WIREGUARD_PRIVATE_KEY=${WIREGUARD_PRIVATE_KEY}
      - WIREGUARD_ADDRESSES=${WIREGUARD_ADDRESSES}
    ports:
      - "${QBITTORRENT_PORT}:${QBITTORRENT_PORT}" # qBittorrent Web UI
      - "6881:6881/tcp" # qBittorrent
      - "6881:6881/udp" # qBittorrent
      - "${PROWLARR_PORT}:9696" # Prowlarr Web UI
      - "${SONARR_PORT}:8989" # Sonarr Web UI
      - "${RADARR_PORT}:7878" # Radarr Web UI
      - "${READARR_PORT}:8787" # Readarr Web UI
    volumes:
      - ./gluetun:/gluetun
    restart: unless-stopped

  qbittorrent:
    image: lscr.io/linuxserver/qbittorrent:latest
    container_name: qbittorrent
    network_mode: "service:gluetun"
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=${TZ}
      - WEBUI_PORT=${QBITTORRENT_PORT}
    volumes:
      - ./qbittorrent/config:/config
      - "M:/downloads:/downloads"
    depends_on:
      - gluetun
    restart: unless-stopped

  prowlarr:
    image: lscr.io/linuxserver/prowlarr:latest
    container_name: prowlarr
    network_mode: "service:gluetun"
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=${TZ}
    volumes:
      - ./prowlarr/config:/config
    depends_on:
      - gluetun
    restart: unless-stopped

  sonarr:
    image: lscr.io/linuxserver/sonarr:latest
    container_name: sonarr
    network_mode: "service:gluetun"
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=${TZ}
    volumes:
      - ./sonarr/config:/config
      - "M:/tv:/tv"
      - "M:/downloads:/downloads"
    depends_on:
      - gluetun
    restart: unless-stopped

  radarr:
    image: lscr.io/linuxserver/radarr:latest
    container_name: radarr
    network_mode: "service:gluetun"
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=${TZ}
    volumes:
      - ./radarr/config:/config
      - "M:/movies:/movies"
      - "M:/downloads:/downloads"
    depends_on:
      - gluetun
    restart: unless-stopped

  readarr:
    image: lscr.io/linuxserver/readarr:latest
    container_name: readarr
    network_mode: "service:gluetun"
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=${TZ}
    volumes:
      - ./readarr/config:/config
      - "M:/books:/books"
      - "M:/downloads:/downloads"
    depends_on:
      - gluetun
    restart: unless-stopped

  jellyfin:
    image: lscr.io/linuxserver/jellyfin:latest
    container_name: jellyfin
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=${TZ}
    ports:
      - "${JELLYFIN_PORT}:8096"
    volumes:
      - ./jellyfin/config:/config
      - "M:/tv:/data/tv"
      - "M:/movies:/data/movies"
    restart: unless-stopped
```

---

## 7. Phase 4 (Detailed): Launching and Configuring Services

### 7.1. Launch the Stack

1.  Open a terminal (PowerShell) in the `media-stack` directory where your `docker-compose.yml` file is located.
2.  Run the command: `docker-compose up -d`
3.  This will download all the container images and start them. This may take some time on the first run. You can view the logs for all containers by running `docker-compose logs -f`.

### 7.2. Initial Service Setup

After the containers are running, you will configure each service through its web interface.

---

#### **A. qBittorrent (Download Client)**

1.  **Navigate:** Open `http://localhost:8080` in your browser.
2.  **Login:** The default username is `admin` and the password is `adminadmin`. You will be forced to change this immediately. Set a new, secure password.
    - **Note:** On the first run, the container might generate a temporary random password. If `adminadmin` does not work, check the container logs for a message containing the temporary password. You can view the logs by running `docker-compose logs qbittorrent` in the `media-stack` directory.
3.  **Set Default Save Path:**
    - Go to `Tools` > `Options` (the gear icon).
    - Select the `Downloads` tab.
    - Under `Saving Management`, find the `Default Save Path` field and enter exactly: `/downloads`
    - This path refers to the folder *inside the container* which we mapped to your `M:\downloads` drive.
4.  **Save:** Click `Apply` and `OK` at the bottom.

---

#### **B. Prowlarr (Indexer Manager)**

1.  **Navigate:** Open `http://localhost:9696`.
2.  **Add Indexers:**
    - Click on `Indexers` in the left menu, then click `Add Indexer` (the `+` button).
    - A list of presets will appear. Search for the indexers you use. If you don't have private indexers, you can start with public ones like `1337x`.
    - **Note:** Some public indexers, like `1337x`, may be protected by Cloudflare, which can block requests from the server. If you encounter errors, it is often easier to use alternative indexers. Good public alternatives include **YTS** (for movies) and **EZTV** (for TV shows).
    - Click on the desired indexer. A dialog will pop up.
    - Click `Test` (the green checkmark). If it succeeds, click `Save`.
    - Repeat for all the indexers you wish to use.

---

#### **C. Readarr (Book Automation)**

1.  **Navigate:** Open Readarr at `http://localhost:8787`.
2.  **Connect Download Client:**
    - Go to `Settings` > `Download Clients`.
    - Click `Add` (`+`).
    - Select `qBittorrent`.
    - **Name:** `qBittorrent`
    - **Host:** `qbittorrent`
    - **Port:** `8080`
    - **Username/Password:** Enter the new username and password you set for the qBittorrent web UI.
    - Click `Test`. If it succeeds, click `Save`.
3.  **Connect Indexers via Prowlarr:**
    - Go to `Settings` > `Indexers`.
    - Click `Add` (`+`).
    - Select `Prowlarr`.
    - **Name:** `Prowlarr`
    - **Sync Level:** `Full Sync` is recommended.
    - **Prowlarr Server:** `http://prowlarr:9696`
    - **API Key:** Get this from your Prowlarr UI.
    - Click `Test`. If it succeeds, click `Save`.
4.  **Configure Root Media Folder:**
    - Go to `Settings` > `Media Management`.
    - In the `Root Folders` section, click `Add Root Folder`.
    - The path to enter is exactly `/books`. Click `OK`.

---

#### **D. Radarr (Movie Automation)**

The setup for Radarr is critical for our new genre-based sorting.

1.  **Navigate:** Open Radarr at `http://localhost:7878`.
2.  **Connect Download Client & Indexers:**
    - Go to `Settings` > `Download Clients` and connect to qBittorrent as described in the original plan.
    - Go to `Settings` > `Indexers` and connect to Prowlarr as described in the original plan.
3.  **Configure Root Folders:**
    - Go to `Settings` > `Media Management`.
    - Under `Root Folders`, click `Add Root Folder` and add the path `/movies`. This tells Radarr the parent directory where all genre subfolders live.
4.  **Adding a Movie (New Workflow):**
    - When you search for and add a new movie, Radarr will ask for a **Root Folder**.
    - It should default to `/movies`, but now you will manually edit the path for that specific movie to include the correct genre subfolder.
    - **Example:** For the movie "Dune", you would change the path from `/movies` to `/movies/scifi`.
    - This tells Radarr exactly where to move the file after it's downloaded, automatically sorting it into your genre-based structure.
    - In the "Tags" section here, you can add tags like "Based on a Book". While these don't sync to Jellyfin automatically, it helps you keep track of them for later.

---

#### **E. Sonarr (TV Shows)**

The setup for Sonarr and Radarr is nearly identical. We will use Sonarr as the example.

1.  **Navigate:** Open Sonarr at `http://localhost:8989` or Radarr at `http://localhost:7878`.
2.  **Connect Download Client:**
    - Go to `Settings` > `Download Clients`.
    - Click `Add` (`+`).
    - Select `qBittorrent`.
    - **Name:** `qBittorrent` (or anything you like).
    - **Host:** `qbittorrent` (This is the container's service name, which acts as its network address).
    - **Port:** `8080` (or your configured port).
    - **Username/Password:** Enter the new username and password you set for the qBittorrent web UI.
    - Click `Test`. If it succeeds, click `Save`.
3.  **Connect Indexers via Prowlarr:**
    - Go to `Settings` > `Indexers`.
    - Click `Add` (`+`).
    - Select `Prowlarr`.
    - **Name:** `Prowlarr`
    - **Sync Level:** `Full Sync` is recommended.
    - **Prowlarr Server:** `http://prowlarr:9696`
    - **API Key:** Open the Prowlarr UI (`http://localhost:9696`), go to `Settings` > `General`, and copy the API Key. Paste it here.
    - Click `Test`. If it succeeds, click `Save`. Your indexers from Prowlarr will now be available in Sonarr/Radarr.
4.  **Configure Root Media Folders:**
    - **For Sonarr:** Go to `Settings` > `Media Management`. In the `Root Folders` section, click `Add Root Folder`. The path to enter is exactly `/tv`. Click `OK`.
    - **For Radarr:** Go to `Settings` > `Media Management`. In the `Root Folders` section, click `Add Root Folder`. The path to enter is exactly `/movies`. Click `OK`.
    - These paths refer to the folders *inside the containers* which we mapped to your `M:\tv` and `M:\movies` drives.

---

#### **F. Jellyfin (Media Server)**

1.  **Navigate:** Open `http://localhost:8096` and complete the initial startup wizard (create admin user, etc.).
2.  **Add Media Libraries (New Method):**
    - Go to the `Dashboard` > `Libraries`.
    - Click `Add Media Library`.
    - **Content Type:** `Movies`
    - **Display Name:** `Action`
    - **Folders:** Click `+` and add the path `/data/movies/action`.
    - Click `OK`.
    - **REPEAT THIS PROCESS** for every genre folder you created (e.g., a "Comedy" library pointing to `/data/movies/comedy`, and so on).
    - Also add your `TV Shows` library, pointing to `/data/tv`.
3.  **Using Collections and Tags:**
    - **To Create a Collection:** In your library, right-click a movie > `Add to collection`. You can create a new one or add to an existing one. This is perfect for movie series.
    - **To Add Tags:** Right-click a movie > `Metadata`. Scroll to the bottom to find the "Tags" section and add your desired tags.
4.  **Create & Configure User Accounts:**
    - Go to `Dashboard` > `Users` to create accounts for others (e.g., `Neighbor`).
    - In the user's profile, go to the `Access` tab.
    - **Uncheck** `Enable access to all libraries`.
    - Check only the libraries you want that user to see (e.g., only `Horror` and `Thriller` for your neighbor).
5.  **Install Essential Plugins:**
    - Go to `Dashboard` > `Plugins` > `Catalog`.
    - Install the following for an enhanced experience:
        - **Jelly Scrub:** Provides video scrubbing with preview thumbnails.
        - **Intro Skipper:** Adds a "Skip Intro" button.
        - **Trailers:** Allows watching movie trailers.
        - **Merge Versions:** Merges multiple quality versions (e.g., 1080p, 4K) of a movie into one item.
    - You may need to add third-party repositories to find all of these. Refer to the plugin's documentation for specific installation instructions.
6.  **Customize Jellyfin Theme/Appearance (Optional):**
    - Once your core setup is complete, you can further personalize your Jellyfin server's look and feel. Refer to **Video 3: [Jellyfin Theming and Customization](https://www.youtube.com/watch?v=RXdaoPS4FwI&t=163s)** for a detailed guide on advanced theming options.

Your services are now configured with a sophisticated, genre-based layout!

---

## 8. Phase 5: Advanced Automated Tagging (Optional)

This is an advanced, optional step to be performed after your server is running. It uses **Jellyfin Meta Manager (JMM)** to automatically apply tags and create collections.

### 8.1. High-Level Steps

1.  **Install Python:** Ensure you have a current version of Python installed on your Windows PC.
2.  **Install JMM:** Open PowerShell and install JMM using the command: `pip install jellyfin-meta-manager`.
3.  **Create Configuration Files:** JMM is controlled by YAML files (`.yml`). You will need to create a main `config.yml` file and a `movies.yml` file to define your rules.
4.  **Define Rules:** In the `movies.yml` file, you will define the logic for your tags. For example, you can tell JMM to add an `animation` tag to any movie that has "Animation" as a genre on TheMovieDB.
5.  **Run the Script:** Execute JMM from PowerShell to apply your rules.
6.  **Schedule Automation:** Use the Windows Task Scheduler to run the JMM script automatically on a nightly basis, ensuring your library is always up-to-date.

For detailed instructions on configuration and rule creation, refer to the **[Official Jellyfin Meta Manager Documentation](https://metamanager.wiki/en/latest/index.html)**.

### 8.2. Dynamic Collections with Trakt

A core feature of Jellyfin Meta Manager (JMM) is its ability to sync with Trakt to create dynamic, auto-updating collections. This allows you to have rows on your Jellyfin home screen that mirror Trakt's popular lists.

You can configure JMM to connect to your Trakt account and automatically create collections in Jellyfin that mirror those dynamic lists. Every time JMM runs (e.g., every night), it will update these collections with the latest movies from Trakt.

The end result is that on your Jellyfin home screen, you will see new, auto-updating rows like:
- Trending Now
- Popular Movies
- Most Anticipated

#### Configuration in JMM

In your `movies.yml` file for JMM, you would add a section like this:

```yaml
collections:
  Trending:
    trakt_trending: 10
  Popular:
    trakt_popular: 10
  Most Anticipated:
    trakt_anticipated: 10
```

This tells JMM to create three collections: "Trending", "Popular", and "Most Anticipated", each populated with the top 10 movies from the corresponding Trakt list. You can adjust the number to your liking.

### 8.3. Dynamic Library Rotation Script

To further enhance the dynamic nature of your Jellyfin server, a Python script (`rotate_jellyfin_libraries.py`) has been provided. This script allows you to automatically rotate which libraries are visible to a specific user on a scheduled basis.

This is particularly useful for creating a fresh and engaging experience for users by preventing the same categories from always being displayed.

For detailed instructions on how to set up, configure, and schedule this script, please refer to the `README.md` file in the project root.

---

## 9. Phase 6: Secure Remote Access

1.  **Install Tailscale:**
    - On your Windows PC, download and install Tailscale. Log in to your account.
    - On your neighbor's device(s), have them install Tailscale and log in to the same account (or share your server with their account).

2.  **Access Jellyfin:**
    - Find the Tailscale IP address of your Windows PC from the Tailscale admin console.
    - Your neighbor can now access your Jellyfin server at `http://YOUR_TAILSCALE_IP:8096`. They will see only the libraries you granted them access to.

---

## 10. Phase 7: AI-Powered Subjective Tagging (Optional)

For the ultimate in personalized curation, you can use a local AI model to automatically tag your movies with your own subjective categories. This allows you to create collections that are perfectly tailored to your tastes.

A Python script, `ai_tagger.py`, has been provided to facilitate this. It works by:
1.  Fetching metadata for each movie in your Jellyfin library.
2.  Prompting a local AI model to assign your custom subjective categories.
3.  Applying these categories as tags to the movies in Jellyfin.

These tags can then be used by Jellyfin Meta Manager (JMM) to create dynamic collections.

For detailed instructions on how to set up and use this advanced feature, please refer to the `ai_tagger_README.md` file.

---

## 11. Phase 8: Trakt Integration (Optional)

To further enhance your media server, you can integrate it with Trakt.tv. This turns Trakt into a central hub for your viewing activity and helps you discover new content.

### 11.1. Level 1: Two-Way Sync with the Official Trakt Plugin

This is the recommended first step for Trakt integration.

-   **What it is:** A free plugin for Jellyfin that syncs your activity with your Trakt.tv profile.
-   **Key Features:** Scrobbling (watch history sync), rating sync, and watchlist sync.
-   **How to Install:**
    1.  In your Jellyfin dashboard, go to **Advanced** > **Plugins** > **Catalog**.
    2.  Find and install the **Trakt** plugin.
    3.  Restart your Jellyfin server.
    4.  Configure the plugin in the new "Trakt" section of your dashboard.

### 11.2. Level 2: Personalized Recommendations with JellyNext

This uses your Trakt history to help you discover new content.

-   **What it is:** A separate plugin that provides personalized recommendations.
-   **Key Features:** An "Up Next" list based on your history and integration with Radarr/Sonarr to automatically download recommendations.
-   **How to Install:** Look for the **JellyNext** plugin in the Jellyfin plugin catalog.

### 11.3. Level 3: Custom Curation with Personal Lists

This is a great way to supplement the AI tagger for very specific collections.

-   **What it is:** You can create your own personal lists on the Trakt.tv website.
-   **How it works:** JMM can use these personal lists to create corresponding collections in Jellyfin, giving you manual control over curation. This is configured in your JMM `movies.yml` file.
