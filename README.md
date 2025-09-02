# Spotify Playlist MP3 Downloader

Download Spotify playlists as MP3 files with AI-powered filename cleaning and automatic car audio preparation.

## ✨ Features

- 🎵 **One Command Does Everything**: Download, clean filenames with AI, and prepare car audio files
- 🤖 **AI-Powered**: Clean filenames using local Ollama (works without AI too)
- 🚗 **Car Audio Ready**: Automatic VW Passat CC compatible files with ID3v2.3 tags
- ⏭️ **Skip Re-downloads**: Never downloads the same track twice
- 📁 **Dual Output**: Original files + car-optimized versions

## 🚀 Quick Start

### 1. Install

```bash
git clone https://github.com/BernardoSCaetano/spot.git
cd spot
pip install -r requirements.txt
```

### 2. Setup Spotify

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create app with redirect URI: `http://127.0.0.1:8888/callback`
3. Create `.env` file:

```env
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
PLAYLIST_ID=your_playlist_id
```

### 3. Setup AI (Optional)

```bash
./setup_ollama.sh
```

### 4. Run

```bash
python spotdl/main.py
```

That's it! You get both `downloads/` and `CarAudio/` folders automatically.

## 📁 Output Structure

```
downloads/
├── Playlist Name - ID/
│   ├── 01. Artist - Song.mp3        # Original files
│   └── .download_tracking.json      # Prevents re-downloads
└── CarAudio/
    └── Playlist Name/
        └── 01 - Song.mp3             # Car-optimized files
```

## 🎯 Requirements

- Python 3.7+
- FFmpeg
- Ollama (optional, for AI features)

## ⚖️ Fair Use & Legal Notice

**This tool is for personal, educational, and fair use purposes only.**

### Legal Guidelines

| ✅ **Acceptable Use**         | ❌ **Not Acceptable**        |
| ----------------------------- | ---------------------------- |
| Personal offline listening    | Commercial redistribution    |
| Educational/research purposes | Sharing copyrighted content  |
| Backing up your own playlists | Public performance/broadcast |
| Fair use commentary/criticism | Circumventing paid services  |

### Important Notes

- **YouTube Terms**: Using third-party downloaders violates YouTube's ToS (though not necessarily illegal)
- **Copyright**: Downloading copyrighted content without permission may infringe copyright law
- **Fair Use**: Personal, educational, and transformative uses are generally protected
- **Your Responsibility**: Ensure you have rights to download and use the content

### Best Practices

1. **Use YouTube Premium** for official offline access when possible
2. **Download only content you have rights to** (your uploads, CC-licensed, public domain)
3. **Keep downloads private** - don't redistribute or share copyrighted material
4. **Respect artists** - support them through legitimate purchases and streaming

**By using this tool, you acknowledge these responsibilities and agree to use it in compliance with applicable laws and terms of service.**

## 🛡️ Security

- Your `.env` file is gitignored to protect credentials
- No data is sent to external services (except Spotify/YouTube APIs)
- AI processing happens locally via Ollama

## 📄 License

MIT License - see LICENSE file for details.
