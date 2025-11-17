# Next Steps: Media Server Setup

## ✅ Completed

- [x] Docker stack is running successfully
- [x] All containers are started (gluetun, qbittorrent, prowlarr, sonarr, radarr, readarr, jellyfin)
- [x] Fixed Readarr image issue (using `binhex/arch-readarr:latest`)
- [x] Resolved port conflicts
- [x] Fixed Docker permissions (user added to docker group)

---

## 🎯 Immediate Next Steps

### 1. Verify All Services Are Running

Check that all containers are running:
```bash
cd ~/media-stack
docker compose ps
```

You should see all 7 services with status "Up" or "running".

### 2. Access Service Web Interfaces

**Server IP (Tailscale):** `100.114.128.38`

Access each service through your browser using the Tailscale IP address. Tailscale provides secure, encrypted access from anywhere without needing to open ports on your router.

| Service | Port | URL | Default Credentials |
|---------|------|-----|---------------------|
| **Jellyfin** | 8096 | `http://100.114.128.38:8096` | Setup wizard on first access |
| **qBittorrent** | 8080 | `http://100.114.128.38:8080` | `admin` / `adminadmin` |
| **Prowlarr** | 9696 | `http://100.114.128.38:9696` | None (first-time setup) |
| **Sonarr** | 8989 | `http://100.114.128.38:8989` | None (first-time setup) |
| **Radarr** | 7878 | `http://100.114.128.38:7878` | None (first-time setup) |
| **Readarr** | 8787 | `http://100.114.128.38:8787` | None (first-time setup) |

**Note:** 
- The IP address `100.114.128.38` is a **Tailscale IP** - this allows secure access from anywhere, not just your local network.
- Services behind gluetun (qBittorrent, Prowlarr, Sonarr, Radarr, Readarr) use the VPN connection. Jellyfin is directly accessible.
- Make sure Tailscale is running on both your server and the device you're accessing from.

---

## 📋 Service Configuration Checklist

### Step 1: qBittorrent (Download Client)

1. Navigate to `http://100.114.128.38:8080` (Tailscale IP)
2. Login with `admin` / `adminadmin` and **change the password immediately**
3. Go to `Tools` > `Options` > `Downloads`
4. Set `Default Save Path` to exactly: `/downloads`
5. Click `Apply` and `OK`

### Step 2: Prowlarr (Indexer Manager)

1. Navigate to `http://100.114.128.38:9696` (Tailscale IP)
2. Go to `Indexers` > `Add Indexer` (`+` button)
3. Add your preferred indexers (e.g., `1337x`, `EZTV`, `RARBG` for public trackers)
4. Test and save each indexer
5. **Important:** Copy your API key from `Settings` > `General` > `API Key` (you'll need this for Sonarr/Radarr/Readarr)

### Step 3: Sonarr (TV Shows)

1. Navigate to `http://100.114.128.38:8989` (Tailscale IP)
2. **Connect Download Client:**
   - Go to `Settings` > `Download Clients` > `Add` (`+`)
   - Select `qBittorrent`
   - **Host:** `qbittorrent`
   - **Port:** `8080`
   - Enter your qBittorrent username and password
   - Test and save
3. **Connect Indexers:**
   - Go to `Settings` > `Indexers` > `Add` (`+`)
   - Select `Prowlarr`
   - **Prowlarr Server:** `http://prowlarr:9696`
   - **API Key:** Paste the API key from Prowlarr
   - Test and save
4. **Configure Root Folder:**
   - Go to `Settings` > `Media Management`
   - Click `Add Root Folder`
   - Enter the path: `/tv`
   - Click `OK`

### Step 4: Radarr (Movies)

1. Navigate to `http://100.114.128.38:7878` (Tailscale IP)
2. **Connect Download Client:**
   - Same steps as Sonarr (use `qbittorrent` as host, port `8080`)
3. **Connect Indexers:**
   - Same steps as Sonarr (use Prowlarr API key)
4. **Configure Root Folder:**
   - Go to `Settings` > `Media Management`
   - Click `Add Root Folder`
   - Enter the path: `/movies`
   - **Note:** When adding movies, you'll need to manually edit paths to place them in genre subfolders (e.g., `/movies/action`, `/movies/comedy`)

### Step 5: Readarr (Books)

1. Navigate to `http://100.114.128.38:8787` (Tailscale IP)
2. **Connect Download Client:**
   - Same steps as Sonarr/Radarr
3. **Connect Indexers:**
   - Same steps as Sonarr/Radarr (use Prowlarr API key)
4. **Configure Root Folder:**
   - Go to `Settings` > `Media Management`
   - Click `Add Root Folder`
   - Enter the path: `/books`

### Step 6: Jellyfin (Media Server)

1. Navigate to `http://100.114.128.38:8096` (Tailscale IP)
2. Complete the initial setup wizard:
   - Choose your language
   - Create an admin account
   - Set up your media libraries (see below)

3. **Add Media Libraries:**
   - Go to `Dashboard` > `Libraries` > `Add Media Library`
   - **For Movies (by genre):**
     - Content Type: `Movies`
     - Display Name: `Action` (or your first genre)
     - Folders: Add `/data/movies/action`
     - Repeat for each genre folder you created
   - **For TV Shows:**
     - Content Type: `TV Shows`
     - Display Name: `TV Shows`
     - Folders: Add `/data/tv`
   - **For Books:**
     - Content Type: `Books`
     - Display Name: `Books`
     - Folders: Add `/data/books`

4. **Create User Accounts:**
   - Go to `Dashboard` > `Users`
   - Click `Add User`
   - Create accounts for other users
   - In each user's profile (`Access` tab), uncheck `Enable access to all libraries` and select only the libraries you want them to see

---

## 🔧 Optional: Remove Obsolete Version Attribute

The `version: "3.7"` line in `docker-compose.yml` is obsolete in Docker Compose v2. You can optionally remove it:

```bash
cd ~/media-stack
nano docker-compose.yml
```

Remove the first line `version: "3.7"` and save.

---

## 🚀 Advanced Features (Future)

Once your basic setup is working, you can explore:

1. **Jellyfin Meta Manager (JMM)** - Automated collection management
2. **Trakt Integration** - Sync watch history and lists
3. **Dynamic Library Rotation** - Rotate content libraries
4. **AI-Powered Tagging** - Automated content tagging

See `STEP_BY_STEP_GUIDE.md` Section 4 for details on these features.

---

## 📝 Useful Commands

**View container logs:**
```bash
docker compose logs -f [service_name]
```

**Restart a service:**
```bash
docker compose restart [service_name]
```

**Stop all services:**
```bash
docker compose down
```

**Start all services:**
```bash
docker compose up -d
```

**View running containers:**
```bash
docker compose ps
```

---

## 🆘 Troubleshooting

If you encounter issues:

1. Check container logs: `docker compose logs [service_name]`
2. Verify containers are running: `docker compose ps`
3. Check the `troubleshooting_log.md` file for common issues
4. Ensure your `.env` file has correct values (especially PUID/PGID)

---

## ✅ Success Criteria

You'll know everything is working when:

- [ ] All 7 containers are running
- [ ] You can access all web interfaces
- [ ] qBittorrent can download files
- [ ] Prowlarr has indexers configured
- [ ] Sonarr/Radarr/Readarr are connected to qBittorrent and Prowlarr
- [ ] Jellyfin can scan and display your media libraries
- [ ] You can stream content from Jellyfin

Good luck with your media server setup! 🎬📺📚

