# Troubleshooting Log

This document records the troubleshooting steps taken to resolve a persistent "permission denied" error when running the Docker stack on a Windows host connected to a Synology NAS SMB share.

## Initial Problem

When attempting to add a root folder (e.g., `/movies`) in Radarr, the application returned a "Folder is not writable by user 'abc'" error. This occurred despite the folder being accessible from the Windows host.

## Troubleshooting Steps

1.  **Verified Synology Permissions:** Confirmed that the dedicated `docker_user` had `Read/Write` permissions for the `media` shared folder on the Synology NAS.

2.  **Verified Windows Network Drive Mapping:** Disconnected and remapped the `M:` network drive on Windows, explicitly using the `docker_user` credentials and ensuring the "Connect using different credentials" option was checked. The error persisted.

3.  **Corrected PUID/PGID:**
    *   Enabled SSH on the Synology NAS.
    *   Connected via SSH and used the `id docker_user` command to find the correct user and group IDs.
    *   Found `uid=1027` and `gid=100`.
    *   Updated the `.env` file with `PUID=1027` and `PGID=100`.
    *   Recreated the containers with `docker-compose down` and `docker compose up -d`.
    *   The error persisted.

4.  **Corrected `docker-compose.yml` Variables:**
    *   Discovered that the `PUID` and `PGID` values in the `docker-compose.yml` file were hardcoded to `1000` and were not using the variables from the `.env` file.
    *   Corrected the `docker-compose.yml` to use `${PUID}` and `${PGID}` for all services.
    *   Recreated the containers.
    *   The error persisted.

5.  **Applied Recursive Permissions (ACLs):**
    *   In the Synology File Station, recursively applied the `docker_user`'s `Read/Write` permissions to the `media` folder and all its sub-folders and files.
    *   The error persisted.

6.  **Isolated the Write Issue (Troubleshooter Container):**
    *   Added a temporary `troubleshooter` service to the `docker-compose.yml` file using a simple `alpine` image.
    *   This container used the same `PUID`/`PGID` (`1027`/`100`) and mounted the same `M:/movies` volume.
    *   The container **successfully created a test file**, proving that the fundamental connection, permissions, and PUID/PGID settings were logically correct.

7.  **Tested Local Volume Mount:**
    *   Changed the `radarr` service's volume mount from the `M:` drive network share to a local Windows folder (`C:\temp_media\movies`).
    *   Radarr **successfully added the root folder**, proving the issue was specific to the network share.

8.  **Tested UNC Path:**
    *   Changed all `M:` drive paths in the `docker-compose.yml` to a direct UNC path (`//<synology_ip>/media/...`).
    *   The error persisted.

## Diagnosis and Pivot

The troubleshooting process revealed two key issues:

1.  There is a deep, intractable incompatibility between Docker for Windows, the Windows SMB client, and the Synology SMB server that prevents the `linuxserver.io` containers from gaining write access, even when a simpler container can.
2.  The original plan to pivot to running Docker on the Synology NAS was blocked because the user's NAS model, the **DS1817** (non-plus), has an ARM-based CPU and **does not support Docker (Container Manager)**.

## New Plan

Given the roadblocks, the decision was made to pivot to a more robust and reliable solution: using a dedicated computer to run the Docker stack.

*   **New Server:** A Lenovo M710 desktop.
*   **New OS:** Ubuntu Server LTS.
*   **New Approach:** The Lenovo M710 will run the Docker stack. It will mount the Synology `media` share over the network. This Linux-to-Linux connection is much more stable and avoids the Windows-specific permission issues. The `implementation_plan.md` has been updated to reflect this new direction.

---

## Docker Compose Setup Issues (November 2025)

### Issues Encountered

1. **Readarr Image Not Found:**
   - **Problem:** Initial attempt used `lscr.io/linuxserver/readarr:latest`, but LinuxServer.io does not maintain a Readarr image.
   - **Error:** `failed to resolve reference "lscr.io/linuxserver/readarr:latest": not found`
   - **Solution:** Changed to `binhex/arch-readarr:latest`, which is a publicly available image on Docker Hub.

2. **Port Conflicts:**
   - **Problem:** Port 8030 and 8080 were already in use, preventing gluetun from starting.
   - **Error:** `failed to bind host port 0.0.0.0:8030/tcp: address already in use`
   - **Solution:** 
     - Stopped and removed existing gluetun and qbittorrent containers: `sudo docker stop gluetun && sudo docker rm gluetun`
     - Checked for port conflicts: `sudo lsof -i :8080` or `sudo docker ps -a | grep gluetun`
     - If needed, changed port in `.env` file (e.g., `QBITTORRENT_PORT=8081`)

3. **Docker Permission Issues:**
   - **Problem:** User couldn't run Docker commands without `sudo`.
   - **Error:** `permission denied while trying to connect to the docker API`
   - **Solution:** Added user to docker group: `sudo usermod -aG docker $USER`, then logged out and back in (or run `newgrp docker`).

4. **YAML Indentation:**
   - **Problem:** Initial docker-compose.yml had inconsistent indentation.
   - **Solution:** Fixed all indentation to use consistent 2-space indentation throughout.

5. **Missing READARR_PORT Mapping:**
   - **Problem:** READARR_PORT was not mapped in gluetun's ports section.
   - **Solution:** Added `- "${READARR_PORT}:8787" # Readarr Web UI` to gluetun ports.

6. **Jellyfin DNS Configuration:**
   - **Added:** DNS configuration to jellyfin service for better connectivity:
     ```yaml
     dns:
       - 8.8.8.8
     ```

### Final Working Configuration

*   **Readarr Image:** `binhex/arch-readarr:latest`
*   **All containers successfully started** after resolving port conflicts and permission issues.
*   **Docker Compose version warning:** The `version: "3.7"` attribute is obsolete in Docker Compose v2 but can be safely ignored or removed.
