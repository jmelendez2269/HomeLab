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
| **qBittorrent** | 8081 | `http://100.114.128.38:8081` | `admin` / (check logs for temp password) |
| **Prowlarr** | 9696 | `http://100.114.128.38:9696` | None (first-time setup) |
| **Sonarr** | 8989 | `http://100.114.128.38:8989` | None (first-time setup) |
| **Radarr** | 7878 | `http://100.114.128.38:7878` | None (first-time setup) |
| **Readarr** | 8787 | `http://100.114.128.38:8787` | None (first-time setup) |

**Important Notes:**
- **qBittorrent uses port 8081** (not 8080). Check your `.env` file - if `QBITTORRENT_PORT=8080`, change it to `8081` or update the docker-compose.yml port mapping.
- **Readarr port 8787** may not be mapped if `READARR_PORT` isn't set in your `.env` file. Verify it's set: `READARR_PORT=8787`

**Note:** 
- The IP address `100.114.128.38` is a **Tailscale IP** - this allows secure access from anywhere, not just your local network.
- Services behind gluetun (qBittorrent, Prowlarr, Sonarr, Radarr, Readarr) use the VPN connection. Jellyfin is directly accessible.
- Make sure Tailscale is running on both your server and the device you're accessing from.

---

## 📋 Service Configuration Checklist

### Step 1: qBittorrent (Download Client)

1. Navigate to `http://100.114.128.38:8081` (Tailscale IP) - **Note: Use port 8081, not 8080**
2. Login credentials:
   - Username: `admin`
   - Password: Check container logs for temporary password: `sudo docker compose logs qbittorrent | grep password`
   - If no password was set, try `adminadmin`
   - **Change the password immediately** after first login
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
   - **Host:** `localhost` or `127.0.0.1` (NOT `qbittorrent` - since both services share gluetun's network namespace)
   - **Port:** `8081` (use 8081, not 8080)
   - **URL Base:** Leave empty (unless you've configured a base path in qBittorrent)
   - **Username:** `admin`
   - **Password:** Enter your qBittorrent password
   - **Category:** `tv-sonarr` (optional but recommended - helps organize downloads)
   - **Post Import Category:** Leave empty (or set to `tv-sonarr` if you want to keep the category after import)
   - **Priority:** `Normal` (or choose based on your preference)
   - Click **Test** to verify the connection
   - Click **Save** once the test succeeds
3. **Connect Indexers (Recommended Method - Use Prowlarr Apps):**
   
   **This is the easiest and most reliable method. Configure Prowlarr to connect to Sonarr:**
   - Open Prowlarr: `http://100.114.128.38:9696`
   - Go to `Settings` > `Apps`
   - Click `Add` (`+`) button
   - Select `Sonarr`
   - Fill in the fields:
     - **Name:** `Sonarr` (or any name you prefer)
     - **Prowlarr Server:** `http://localhost:9696` (use localhost since both services share gluetun's network)
     - **Sonarr Server:** `http://localhost:8989` (use localhost since both services share gluetun's network)
     - **API Key:** Get this from Sonarr: Go to Sonarr `Settings` > `General` > `API Key` and copy it
     - **Sync App Indexers:** ✅ **Check this box** (this automatically syncs all Prowlarr indexers to Sonarr)
   - Click `Test` to verify the connection
   - Click `Save` once the test succeeds
   - **Result:** All your Prowlarr indexers will automatically appear in Sonarr - no manual Torznab configuration needed!
   
   **Alternative: Manual Torznab Method (if Apps method doesn't work):**
   - In Sonarr, go to `Settings` > `Indexers` > `Add` (`+`)
   - Select `Torznab`
   - **Name:** `Prowlarr`
   - **URL:** `http://localhost:9696`
   - **API Path:** `/prowlarr/api` (or `/api` if that fails)
   - **API Key:** From Prowlarr `Settings` > `General` > `API Key`
   - Click `Test` then `Save`
4. **Configure Root Folder:**
   - Go to `Settings` > `Media Management`
   - Click `Add Root Folder`
   - Enter the path: `/tv`
   - Click `OK`

### Step 4: Radarr (Movies)

1. Navigate to `http://100.114.128.38:7878` (Tailscale IP)
2. **Connect Download Client:**
   - Same steps as Sonarr, but use:
     - **Category:** `movies-radarr` (instead of `tv-sonarr`)
     - **Post Import Category:** Leave empty or set to `movies-radarr`
3. **Connect Indexers (Recommended - Use Prowlarr Apps):**
   - **Best method:** In Prowlarr, go to `Settings` > `Apps` > `Add` > Select `Radarr`
     - **Prowlarr Server:** `http://localhost:9696`
     - **Radarr Server:** `http://localhost:7878`
     - **API Key:** Get from Radarr: `Settings` > `General` > `API Key`
     - **Sync App Indexers:** ✅ Check this box
     - Click `Test` then `Save`
   - **Alternative:** Same manual Torznab method as Sonarr (see Sonarr section above)
4. **Configure Root Folder:**
   - Go to `Settings` > `Media Management`
   - Click `Add Root Folder`
   - Enter the path: `/movies`
   - **Note:** When adding movies, you'll need to manually edit paths to place them in genre subfolders (e.g., `/movies/action`, `/movies/comedy`)

### Step 5: Readarr (Books)

1. Navigate to `http://100.114.128.38:8787` (Tailscale IP)
2. **Connect Download Client:**
   - Same steps as Sonarr/Radarr, but use:
     - **Category:** `books-readarr` (instead of `tv-sonarr`)
     - **Post Import Category:** Leave empty or set to `books-readarr`
3. **Connect Indexers (Recommended - Use Prowlarr Apps):**
   - **Best method:** In Prowlarr, go to `Settings` > `Apps` > `Add` > Select `Readarr`
     - **Prowlarr Server:** `http://localhost:9696`
     - **Readarr Server:** `http://localhost:8787`
     - **API Key:** Get from Readarr: `Settings` > `General` > `API Key`
     - **Sync App Indexers:** ✅ Check this box
     - Click `Test` then `Save`
   - **Alternative:** Same manual Torznab method as Sonarr (see Sonarr section above)
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

### Connection Refused Errors (ERR_CONNECTION_REFUSED)

If you get "connection refused" when accessing services:

1. **Verify Tailscale is running:**
   - On your Windows computer, check if Tailscale is running (system tray icon)
   - On your Linux server, check: `sudo tailscale status`
   - Both devices must be connected to the same Tailscale network
   - Test connectivity: `ping 100.114.128.38` from Windows Command Prompt

2. **Verify containers are running:**
   ```bash
   ssh your_username@100.114.128.38
   cd ~/media-stack
   docker compose ps
   ```
   All services should show "Up" status

3. **Check gluetun VPN connection (IMPORTANT):**
   ```bash
   # On the Linux server (use sudo if you get permission errors)
   sudo docker compose logs gluetun | tail -50
   ```
   Look for messages like "VPN is connected" or "Public IP: XXX". If gluetun's VPN isn't connected, services behind it won't be accessible.
   
   **Note:** Services behind gluetun (qBittorrent, Prowlarr, Sonarr, Radarr, Readarr) require gluetun's VPN to be connected. If you haven't configured VPN credentials in your `.env` file, gluetun won't connect.
   
   **If you get "permission denied" errors:** Use `sudo` before docker commands, or log out and back in after running `sudo usermod -aG docker $USER` to apply docker group membership.

4. **Check if ports are listening:**
   ```bash
   # On the Linux server
   sudo ss -tulpn | grep 8080
   sudo ss -tulpn | grep 9696
   ```
   If nothing shows up, the services aren't binding to the network interface.

5. **Check container logs for errors:**
   ```bash
   # Use sudo if you get permission errors
   sudo docker compose logs qbittorrent
   sudo docker compose logs gluetun
   ```

6. **Verify gluetun is exposing ports correctly:**
   ```bash
   # Check gluetun container ports (use sudo if needed)
   sudo docker inspect gluetun | grep -A 10 "Ports"
   ```

7. **Check firewall on Linux server:**
   ```bash
   sudo ufw status
   # If firewall is active, you may need to allow Tailscale traffic
   sudo ufw allow in on tailscale0
   ```

8. **If gluetun VPN is connected but services still aren't accessible:**
   - Check if ports are actually listening: `sudo ss -tulpn | grep -E "(8080|8081|9696|8989|7878|8787)"`
   - Try restarting the services: `sudo docker compose restart qbittorrent prowlarr sonarr radarr readarr`
   - Verify gluetun is exposing the ports: `sudo docker port gluetun`
   - Check if services are binding to the correct interface (should be 0.0.0.0, not 127.0.0.1)
   - Try accessing from the server itself: `curl http://localhost:8081` (should work if service is running)

9. **If Sonarr/Radarr/Readarr can't connect to qBittorrent:**
   - Verify qBittorrent is running: `sudo docker compose ps qbittorrent`
   - Check qBittorrent logs: `sudo docker compose logs qbittorrent | tail -20`
   - Test connection from within gluetun network: `sudo docker exec gluetun wget -O- http://qbittorrent:8081 2>&1 | head -5`
   - Verify qBittorrent is listening on the correct port inside the container:
     ```bash
     sudo docker exec qbittorrent netstat -tulpn | grep 8081
     # or
     sudo docker exec qbittorrent ss -tulpn | grep 8081
     ```
   - Check if WEBUI_PORT matches: Look at qBittorrent logs for "WebUI will be started" message
   - **IMPORTANT:** Use `localhost` or `127.0.0.1` instead of `qbittorrent` as the host (since both services share gluetun's network namespace, container names don't resolve - use localhost)
   - Restart both services: `sudo docker compose restart qbittorrent sonarr`

10. **If gluetun VPN isn't configured:**
   - Services behind gluetun require VPN credentials in your `.env` file
   - If you don't want to use a VPN, you'll need to modify the docker-compose.yml to remove `network_mode: "service:gluetun"` and add direct port mappings
   - Alternatively, access Jellyfin (port 8096) which doesn't use gluetun

### Other Common Issues

1. Check container logs: `docker compose logs [service_name]`
2. Verify containers are running: `docker compose ps`
3. Check the `troubleshooting_log.md` file for common issues
4. Ensure your `.env` file has correct values (especially PUID/PGID)
5. Restart services if needed: `docker compose restart [service_name]`

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

