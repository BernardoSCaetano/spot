# Spotify Playlist MP3 Downloader

This project fetches tracks from a Spotify playlist (including private playlists) and downloads the corresponding MP3 files from YouTube. Downloaded files are stored in organized folders with proper metadata for car audio systems and music players.

## Features

- 🎵 **Spotify Integration**: Authenticate with Spotify (supports private playlists)
- 📥 **Smart Downloads**: Fetch playlist tracks and download MP3s from YouTube
- 📁 **Auto Organization**: Creates playlist-named folders with numbered tracks
- 🤖 **AI-Powered Filenames**: Uses local Ollama to generate clean, consistent filenames automatically
- 🚗 **Car Audio Ready**: Prepares files with proper ID3v2.3 metadata for car stereos (automatic)
- 🔍 **Optimized Search**: Avoids official videos/intros for better audio quality
- 📊 **Progress Tracking**: Real-time download progress with success/failure indicators
- 🛡️ **Duplicate Handling**: Prevents overwrites with intelligent file naming
- ⏭️ **Skip Re-downloads**: Tracks already downloaded songs to avoid duplicates

## Setup

### 1. Prerequisites

- Python 3.7+
- FFmpeg (for audio conversion)
- Ollama (for AI-powered filename generation) - _Optional but recommended_

### 2. Installation

```bash
# Clone this repository
git clone https://github.com/BernardoSCaetano/spot.git
cd spot

# Install dependencies
pip install -r requirements.txt

# Set up AI features (optional but recommended)
./setup_ollama.sh
```

### 3. Environment Setup

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use your preferred editor
```

### 4. Spotify API Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Add redirect URI: `http://127.0.0.1:8888/callback`
4. Copy your Client ID and Client Secret
5. Update `.env` file with your credentials:
   ```env
   SPOTIPY_CLIENT_ID=your_actual_client_id
   SPOTIPY_CLIENT_SECRET=your_actual_client_secret
   PLAYLIST_ID=your_playlist_id
   ```

### 5. Get Playlist ID

- Open Spotify and go to your playlist
- Copy the playlist URL: `https://open.spotify.com/playlist/2NjzrKmSXhOvofpoTEE9UC`
- The playlist ID is the part after `/playlist/`: `2NjzrKmSXhOvofpoTEE9UC`

## Usage

### Basic Download (Complete Workflow)

```bash
# Download playlist with automatic AI filename generation and car audio preparation
python spotdl/main.py

# This automatically:
# 1. Downloads tracks from YouTube
# 2. Generates clean filenames using AI
# 3. Prepares car audio optimized files in CarAudio/ folder
# 4. Avoids re-downloading existing tracks
# 5. Creates both downloads/ and CarAudio/ folders
```

**No separate commands needed** - everything happens in one streamlined process!

### Car Audio Preparation

Car audio preparation is now **completely automatic** with every download:

```bash
# Single command does everything
python spotdl/main.py

# No additional steps needed!
# Car audio files are automatically created in CarAudio/ folder
```

**Automatic Car Audio Features:**

- Creates separate CarAudio/ folder with optimized files
- AI-generated car-friendly filenames
- VW Passat CC compatible ID3v2.3 tags
- FAT32-friendly file naming
- Sequential track numbering

### AI-Powered Workflow (Always-On)

The downloader includes **always-on AI and car audio preparation**:

```bash
# Set up Ollama (one-time setup)
./setup_ollama.sh

# Single command for complete workflow
python spotdl/main.py
```

**Integrated Features (Automatic):**

- **Smart Filenames**: AI generates clean, consistent filenames for every track
- **Car Audio Ready**: Files automatically prepared for VW-compatible systems
- **Dual Output**: Both original and car-optimized files created
- **Fallback Support**: Works without AI if Ollama unavailable

**What Happens Automatically:**

- Downloads tracks with AI-cleaned filenames
- Creates original files in downloads/ folder
- Creates car audio files in CarAudio/ folder
- Prevents re-downloading existing tracks
- Generates VW-compatible ID3v2.3 tags

## VS Code Integration

This project includes comprehensive VS Code tasks for easy development and usage:

```bash
# Access via Command Palette (Cmd+Shift+P):
# "Tasks: Run Task" → Select from available tasks
```

### 🎵 **Quick Tasks Available:**

- **Download Playlist (Complete AI-Powered Process + Car Audio)** - Everything in one command
- **Start Ollama Server** - Launch AI server in background
- **Install Ollama Models** - Set up GPT-OSS and Qwen models
- **Setup Complete Environment** - One-click setup for everything

### 🔧 **Input Variables:**

- **Playlist ID**: Uses your `.env` file or prompts for input

**Streamlined Workflow**: Single command does everything - downloads, AI cleaning, and car audio preparation automatically.

## Features in Detail

### Smart File Organization with AI

- **AI-Generated Filenames**: Clean, consistent names for every track using local Ollama
- **Dual Organization**: Creates both original downloads and car-optimized versions
- **Sequential Numbering**: Files numbered `01. Artist - Song.mp3` for proper order
- **Duplicate Prevention**: Intelligent file naming and download tracking system
- **Playlist Folders**: Named `"Playlist Name - PlaylistID"` for easy identification

### Car Audio Optimization (Automatic)

- **AI-Optimized Metadata**: Clean artist names, titles, and album info using Ollama
- **ID3v2.3 tags**: Maximum car stereo compatibility (UTF-16 encoding)
- **FAT32-friendly filenames**: No special characters, optimized for USB sticks
- **Sequential numbering**: Proper track order in car stereos
- **VW Compatible**: Tested with VW Passat CC and similar systems
- **Automatic Creation**: CarAudio folder generated with every download

### Download Optimization

- **Avoids official videos** with intros/outros
- **Duration filtering** to prevent long videos
- **Fallback search** strategies for failed downloads
- **Audio-first formats** (M4A/MP3 priority)

## File Structure

After running the downloader, you'll get:

```
downloads/
├── Playlist Name - PlaylistID/
│   ├── 01. Artist - Song.mp3            # Original downloads
│   ├── 02. Artist - Song.mp3
│   └── .download_tracking.json          # Prevents re-downloads
└── CarAudio/
    └── Playlist Name/
        ├── 01 - Song.mp3                 # Car-optimized files
        ├── 02 - Song.mp3                 # (AI-cleaned filenames)
        └── ...
```

**Key Points:**

- **downloads/**: Original files with full artist-song names
- **CarAudio/**: Car stereo optimized with simplified names
- **Tracking**: `.download_tracking.json` prevents duplicate downloads
- **AI Filenames**: Both folders use AI-generated clean names

## Car Audio Tips

For optimal car stereo compatibility:

- Format USB stick as **FAT32**
- Use **USB 2.0 stick** (≤32GB recommended)
- Copy the entire playlist folder to USB root
- Tested with VW Passat CC and similar systems

## Requirements

See `requirements.txt`:

- spotipy (Spotify API)
- yt-dlp (YouTube downloads)
- mutagen (metadata handling)
- python-dotenv (environment variables)
- requests (AI integration)

**Optional AI Dependencies:**

- Ollama (local AI server for filename generation)
- Recommended models: gpt-oss, qwen2.5:7b

## Security

⚠️ **Important**: Never commit your `.env` file to version control!

- Your actual credentials are in `.env` (ignored by git)
- `.env.example` shows the required format without sensitive data
- The `.gitignore` file prevents accidental commits of credentials

## Notes

- Requires valid Spotify API credentials
- Downloaded files are for personal use only
- Respects YouTube's terms of service
- FFmpeg required for audio conversion

## License

MIT
