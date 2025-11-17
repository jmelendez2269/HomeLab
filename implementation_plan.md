# Home Lab Media Server Implementation Plan

## 1. Overview

**Goal:** To build a fully automated, containerized media server stack running on a dedicated server. This setup will automatically download, sort, and manage media, storing it on a Synology NAS and serving it through a user-friendly interface.

**Key Features:**
- **Dedicated Server:** The entire application stack will run on a dedicated Lenovo M710 desktop for stability and performance.
- **Automated Media Acquisition:** Movies, TV shows, and books will be automatically found and downloaded based on user requests.
- **Centralized Media Storage:** All media files will be stored on a Synology NAS.
- **Containerized Services:** All applications will run in Docker containers for clean and easy management.
- **Curated User Experience:** A single media server instance will provide different, curated interfaces for different users.
- **Secure Remote Access:** Remote access will be provided securely via Tailscale, eliminating the need for open ports on the router.

---

## 2. Core Technologies

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Server Host** | Lenovo M710 | The dedicated computer running the entire stack. |
| **Operating System** | Ubuntu Server LTS | A stable, lightweight Linux OS for the server host. |
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

## 5. Phase 2: Server and NAS Preparation

### 5.1. On Your Lenovo M710

1.  **Install Ubuntu Server:**
    -   Create a bootable USB drive with the latest **Ubuntu Server LTS** image. You can find the official guide here: [https://ubuntu.com/tutorials/create-a-usb-stick-on-windows](https://ubuntu.com/tutorials/create-a-usb-stick-on-windows)
    -   Install Ubuntu Server on the Lenovo M710. During the installation process:
        -   When prompted, select the option to **install the OpenSSH server**. This is crucial for remote access.
        -   You can stick with the default options for most other steps.

2.  **Find the Server's IP Address:**
    -   Once the installation is complete and the server has booted, log in.
    -   Run the command `ip a` to find the server's IP address (it will likely be under a name like `enpXsY` and start with `192.168...` or similar). Note this IP address for future use.

### 5.2. On Your Synology NAS

The NAS preparation is much simpler in this new setup.

1.  **Enable SMB Service:**
    -   Go to `Control Panel` > `File Services` > `SMB` and ensure `Enable SMB service` is checked.

2.  **Create Media Folders:**
    -   Open `File Station` and navigate to your desired volume.
    -   Create a main shared folder named `media`.
    -   Inside `media`, create the following folders:
        -   `downloads`
        -   `tv`
        -   `books`
        -   `movies`
    -   Inside the `movies` folder, create subfolders for each genre you want to use (e.g., `action`, `comedy`, `scifi`, etc.).

3.  **Create a Dedicated User:**
    -   Go to `Control Panel` > `User & Group` and create a new user (e.g., `docker_user`).
    -   Give this user **Read/Write** access to the `media` shared folder. Note the username and password.

---

## 6. Phase 3: Docker and Network Share Setup on Linux

Connect to your new Ubuntu server from your Windows PC using PowerShell:
`ssh your_ubuntu_username@YOUR_UBUNTU_SERVER_IP`

All the following commands are to be run on the Ubuntu server.

1.  **Install Docker and Docker Compose:**
    -   Follow the official Docker guide to install Docker Engine on Ubuntu: [https://docs.docker.com/engine/install/ubuntu/](https://docs.docker.com/engine/install/ubuntu/)
    -   Install the Docker Compose plugin: `sudo apt-get install docker-compose-plugin`

2.  **Install CIFS Utilities:**
    -   This package is required to mount SMB (Windows/NAS) shares.
    -   `sudo apt-get update && sudo apt-get install cifs-utils`

3.  **Create Mount Point and Credentials File:**
    -   Create a directory where the NAS share will be mounted: `sudo mkdir /mnt/nas`
    -   Create a file to securely store your NAS credentials: `sudo nano /etc/nas-credentials`
    -   In the text editor, add the following lines, replacing the values with your `docker_user` credentials:
        ```
        username=docker_user
        password=your_password
        ```
    -   Save the file (`Ctrl+X`, then `Y`, then `Enter`).
    -   Secure the credentials file: `sudo chmod 600 /etc/nas-credentials`

4.  **Mount the NAS Share Automatically (fstab):**
    -   Edit the `/etc/fstab` file to automatically mount the share on boot: `sudo nano /etc/fstab`
    -   Add the following line to the end of the file. **You must replace `YOUR_SYNOLOGY_IP`**.
        ```
        //YOUR_SYNOLOGY_IP/media /mnt/nas cifs credentials=/etc/nas-credentials,iocharset=utf8,gid=1000,uid=1000,file_mode=0777,dir_mode=0777 0 0
        ```
    -   Save the file (`Ctrl+X`, then `Y`, then `Enter`).
    -   Mount the drive now without rebooting: `sudo mount -a`
    -   Verify it's mounted by checking the contents: `ls -l /mnt/nas` (you should see your `movies`, `tv`, etc. folders).

---

## 7. Phase 4: Docker Stack Deployment

1.  **Create Project Folder:**
    -   On your Ubuntu server, create a folder for your project: `mkdir ~/media-stack && cd ~/media-stack`

2.  **Create Environment File (`.env`):**
    -   `nano .env`
    -   Paste the following content. **You must edit the placeholder values for `TZ` and your VPN.** The `PUID` and `PGID` should be `1000` for this setup, as you are the only user on this new server.
        ```env
        # --- General Settings ---
        TZ=Etc/UTC
        PUID=1000
        PGID=1000

        # --- VPN Settings (for GlueTUN) ---
        VPN_SERVICE_PROVIDER=
        VPN_TYPE=openvpn
        OPENVPN_USER=
        OPENVPN_PASSWORD=
        WIREGUARD_PRIVATE_KEY=
        WIREGUARD_ADDRESSES=

        # --- Service Configuration ---
        JELLYFIN_PORT=8096
        RADARR_PORT=7878
        SONARR_PORT=8989
        READARR_PORT=8787
        PROWLARR_PORT=9696
        QBITTORRENT_PORT=8080
        ```

3.  **Create Docker Compose File (`docker-compose.yml`):**
    -   `nano docker-compose.yml`
    -   Paste the following content. Note how the volume paths now point to `/mnt/nas`.
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
              - "${QBITTORRENT_PORT}:${QBITTORRENT_PORT}"
              - "${PROWLARR_PORT}:9696"
              - "${SONARR_PORT}:8989"
              - "${RADARR_PORT}:7878"
              - "${READARR_PORT}:8787"
              - "6881:6881/tcp"
              - "6881:6881/udp"
            volumes:
              - ./gluetun:/gluetun
            restart: unless-stopped

          qbittorrent:
            image: lscr.io/linuxserver/qbittorrent:latest
            container_name: qbittorrent
            network_mode: "service:gluetun"
            environment:
              - PUID=${PUID}
              - PGID=${PGID}
              - TZ=${TZ}
              - WEBUI_PORT=${QBITTORRENT_PORT}
            volumes:
              - ./qbittorrent/config:/config
              - /mnt/nas/downloads:/downloads
            depends_on:
              - gluetun
            restart: unless-stopped

          prowlarr:
            image: lscr.io/linuxserver/prowlarr:latest
            container_name: prowlarr
            network_mode: "service:gluetun"
            environment:
              - PUID=${PUID}
              - PGID=${PGID}
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
              - PUID=${PUID}
              - PGID=${PGID}
              - TZ=${TZ}
            volumes:
              - ./sonarr/config:/config
              - /mnt/nas/tv:/tv
              - /mnt/nas/downloads:/downloads
            depends_on:
              - gluetun
            restart: unless-stopped

          radarr:
            image: lscr.io/linuxserver/radarr:latest
            container_name: radarr
            network_mode: "service:gluetun"
            environment:
              - PUID=${PUID}
              - PGID=${PGID}
              - TZ=${TZ}
            volumes:
              - ./radarr/config:/config
              - /mnt/nas/movies:/movies
              - /mnt/nas/downloads:/downloads
            depends_on:
              - gluetun
            restart: unless-stopped

          readarr:
            image: lscr.io/linuxserver/readarr:latest
            container_name: readarr
            network_mode: "service:gluetun"
            environment:
              - PUID=${PUID}
              - PGID=${PGID}
              - TZ=${TZ}
            volumes:
              - ./readarr/config:/config
              - /mnt/nas/books:/books
              - /mnt/nas/downloads:/downloads
            depends_on:
              - gluetun
            restart: unless-stopped

          jellyfin:
            image: lscr.io/linuxserver/jellyfin:latest
            container_name: jellyfin
            environment:
              - PUID=${PUID}
              - PGID=${PGID}
              - TZ=${TZ}
            ports:
              - "${JELLYFIN_PORT}:8096"
            volumes:
              - ./jellyfin/config:/config
              - /mnt/nas/tv:/data/tv
              - /mnt/nas/movies:/data/movies
              - /mnt/nas/books:/data/books
            restart: unless-stopped
        ```

---

## 8. Phase 5: Launching and Configuring Services

### 8.1. Launch the Stack

1.  From your SSH session in the `~/media-stack` directory, run the command: `docker compose up -d`
2.  This will download all the container images and start them. You can view the logs for all containers by running `docker-compose logs -f`.

### 8.2. Initial Service Setup

After the containers are running, you will configure each service through its web interface by navigating to `http://YOUR_UBUNTU_SERVER_IP:PORT`.

---

#### **A. qBittorrent (Download Client)**

1.  **Navigate:** Open `http://YOUR_UBUNTU_SERVER_IP:8080` in your browser.
2.  **Login:** The default username is `admin` and the password is `adminadmin`. You will be forced to change this immediately. Set a new, secure password.
    - **Note:** On the first run, the container might generate a temporary random password. If `adminadmin` does not work, check the container logs for a message containing the temporary password. You can view the logs by running `docker-compose logs qbittorrent` in the `media-stack` directory.
3.  **Set Default Save Path:**
    - Go to `Tools` > `Options` (the gear icon).
    - Select the `Downloads` tab.
    - Under `Saving Management`, find the `Default Save Path` field and enter exactly: `/downloads`
    - This path refers to the folder *inside the container* which we mapped to your `/mnt/nas/downloads` folder.
4.  **Save:** Click `Apply` and `OK` at the bottom.

---

#### **B. Prowlarr (Indexer Manager)**

1.  **Navigate:** Open `http://YOUR_UBUNTU_SERVER_IP:9696`.
2.  **Add Indexers:**
    - Click on `Indexers` in the left menu, then click `Add Indexer` (the `+` button).
    - A list of presets will appear. Search for the indexers you use.
    - **Note:** Some public indexers, like `1337x`, may be protected by Cloudflare, which can block requests from the server. If you encounter errors, it is often easier to use alternative indexers. Good public alternatives include **YTS** (for movies) and **EZTV** (for TV shows).
    - Click on the desired indexer. A dialog will pop up.
    - Click `Test` (the green checkmark). If it succeeds, click `Save`.
    - Repeat for all the indexers you wish to use.

---

#### **C. Readarr (Book Automation)**

1.  **Navigate:** Open Readarr at `http://YOUR_UBUNTU_SERVER_IP:8787`.
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

1.  **Navigate:** Open Radarr at `http://YOUR_UBUNTU_SERVER_IP:7878`.
2.  **Connect Download Client & Indexers:**
    - Connect to qBittorrent and Prowlarr as you did for Readarr.
3.  **Configure Root Folders:**
    - Go to `Settings` > `Media Management`.
    - Under `Root Folders`, click `Add Root Folder` and add the path `/movies`. This tells Radarr the parent directory where all genre subfolders live.
4.  **Adding a Movie (New Workflow):**
    - When you search for and add a new movie, Radarr will ask for a **Root Folder**.
    - It should default to `/movies`, but now you will manually edit the path for that specific movie to include the correct genre subfolder.
    - **Example:** For the movie "Dune", you would change the path from `/movies` to `/movies/scifi`.

---

#### **E. Sonarr (TV Shows)**

1.  **Navigate:** Open Sonarr at `http://YOUR_UBUNTU_SERVER_IP:8989`.
2.  **Connect Download Client & Indexers:**
    - Connect to qBittorrent and Prowlarr as you did for the other apps.
3.  **Configure Root Media Folders:**
    - Go to `Settings` > `Media Management`. In the `Root Folders` section, click `Add Root Folder`. The path to enter is exactly `/tv`. Click `OK`.

---

#### **F. Jellyfin (Media Server)**

1.  **Navigate:** Open `http://YOUR_UBUNTU_SERVER_IP:8096` and complete the initial startup wizard.
2.  **Add Media Libraries (New Method):**
    - Go to the `Dashboard` > `Libraries`.
    - Click `Add Media Library`.
    - **Content Type:** `Movies`
    - **Display Name:** `Action`
    - **Folders:** Click `+` and add the path `/data/movies/action`.
    - Click `OK`.
    - **REPEAT THIS PROCESS** for every genre folder you created.
    - Also add your `TV Shows` library (pointing to `/data/tv`), and your `Books` library (pointing to `/data/books`).

---

## 9. Phase 6: Advanced Automated Tagging (Optional)

This is an advanced, optional step to be performed after your server is running. It uses **Jellyfin Meta Manager (JMM)** to automatically apply tags and create collections.

### 9.1. High-Level Steps

1.  **Install Python:** Ensure you have a current version of Python installed on your Ubuntu Server.
2.  **Install JMM:** Open a terminal and install JMM using the command: `pip install jellyfin-meta-manager`.
3.  **Create Configuration Files:** JMM is controlled by YAML files (`.yml`).
4.  **Define Rules:** In your configuration files, define the logic for your tags.
5.  **Run the Script:** Execute JMM from your terminal to apply your rules.
6.  **Schedule Automation:** Use `cron` on Linux to run the JMM script automatically on a nightly basis.

For detailed instructions, refer to the **[Official Jellyfin Meta Manager Documentation](https://metamanager.wiki/en/latest/index.html)**.

---

## 10. Phase 7: Secure Remote Access

1.  **Install Tailscale:**
    - On your Lenovo M710 server, install Tailscale.
    - On your personal devices (PC, phone, etc.), install Tailscale.
    - Log in to the same Tailscale account on all devices.

2.  **Access Your Services:**
    - Find the Tailscale IP address of your M710 server from the Tailscale admin console.
    - You can now access all your services from any device, anywhere, using the Tailscale IP (e.g., `http://YOUR_TAILSCALE_IP:8096`).

---

## 11. Phase 8: AI-Powered Subjective Tagging (Optional)

For the ultimate in personalized curation, you can use a local AI model to automatically tag your movies with your own subjective categories. This is an advanced topic for after the main setup is complete. The `ai_tagger.py` script in this repository can be adapted for this purpose.

---

## 12. Phase 9: Trakt Integration (Optional)

To further enhance your media server, you can integrate it with Trakt.tv. This is best done after the core services are running and configured. The official Trakt plugin for Jellyfin is the recommended starting point.