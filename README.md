---
title: Home Assistant on HF Spaces
emoji: 🏠
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
---

# Home Assistant on Hugging Face Spaces

Run [Home Assistant Core](https://www.home-assistant.io/) on Hugging Face Spaces with persistent storage, terminal access, and one-click updates.

## Features

- **Full Home Assistant Core** — Smart home automation platform
- **JupyterLab Terminal** — Web-based terminal at `/lab` for config management
- **Persistent Storage** — HA config, database, and customizations survive restarts (via HF Storage Bucket)
- **One-Click Updates** — Update HA directly from the UI (auto-rebuilds Space)
- **Reverse Proxy** — Caddy routes traffic efficiently

## Setup

### 1. Create a Storage Bucket

This Space needs a **Storage Bucket** mounted at `/config` for persistence:

1. Go to your Space's **Settings** → **Storage Buckets**
2. Create a new bucket (e.g., `ha-config`)
3. Mount it at `/config` with **Read-Write** access

### 2. Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `HF_TOKEN` | ✅ Yes | Hugging Face token with write access to this Space (used by updater) |
| `JUPYTER_TOKEN` | No | JupyterLab login token (default: `huggingface`) |

Set `HF_TOKEN` in **Space Settings** → **Secrets**.

### 3. Deployment

Push to your HF Space repo:

```bash
git push hf main
```

## Usage

| Endpoint | Description |
|----------|-------------|
| `/` | Home Assistant (loading page → auto-redirects) |
| `/lab` | JupyterLab terminal & file manager |
| `/healthz` | Health check endpoint |

### Terminal Access

1. Visit `https://your-space.hf.space/lab`
2. Login with token: `huggingface` (or your custom `JUPYTER_TOKEN`)
3. Open **Terminal** from the Launcher

## Updating

The **HA Space Updater** integration provides one-click updates:

1. Go to **Settings** → **Devices & Services** → **HA Space Updater**
2. Configure with your Space ID (`username/space-name`)
3. Click **Update** when a new version is available

This triggers a Space rebuild with the latest Home Assistant Core.

## Architecture

```
Browser → HF Spaces Proxy → Caddy (:7860)
                              ├── /healthz → respond OK
                              ├── / → landing page (static)
                              ├── /lab* → JupyterLab (:8888)
                              └── /* → Home Assistant (:8123)
```

## Limitations

- No Zigbee/Z-Wave (no physical device passthrough on HF Spaces)
- No mDNS/UPnP (cloud-only, no local network discovery)
- DHCP watcher errors are expected in cloud environments (harmless)
- First startup is slow (~1-2 min) while HA creates its database

## Terms of Use

This Space complies with Hugging Face's Acceptable Use Policy:
- No cryptomining
- No spam or malicious content
- No abuse of HF services
- Legitimate smart home automation use only
