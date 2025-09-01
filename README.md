# Spotify Playlist MP3 Downloader

This project fetches tracks from a Spotify playlist (including private playlists) and downloads the corresponding MP3 files from YouTube. Downloaded files are stored in organized folders with proper metadata for car audio systems and music players.

## Features

- 🎵 **Spotify Integration**: Authenticate with Spotify (supports private playlists)
- 📥 **Smart Downloads**: Fetch playlist tracks and download MP3s from YouTube
- 📁 **Auto Organization**: Creates playlist-named folders with numbered tracks
- 🤖 **AI Metadata Fixing**: Uses local AI to clean and standardize metadata (NEW!)
- 🚗 **Car Audio Ready**: Prepares files with proper ID3v2.3 metadata for car stereos
- 🔍 **Optimized Search**: Avoids official videos/intros for better audio quality
- 📊 **Progress Tracking**: Real-time download progress with success/failure indicators
- 🛡️ **Duplicate Handling**: Prevents overwrites with intelligent file naming
- ⏭️ **Skip Re-downloads**: Tracks already downloaded songs to avoid duplicates

## Setup

### 1. Prerequisites

- Python 3.7+
- FFmpeg (for audio conversion)

### 2. Installation

```bash
# Clone this repository
git clone https://github.com/BernardoSCaetano/spot.git
cd spot

# Install dependencies
pip install -r requirements.txt
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

### Basic Download

```bash
# Download playlist tracks
python spotdl/main.py
```

### Car Audio Preparation

```bash
# Prepare existing downloads for car audio
python spotdl/main.py --car-audio

# With AI metadata fixing (requires Ollama)
python spotdl/main.py --car-audio --fix-metadata

# Or specify a specific folder
python spotdl/main.py --car-audio "/path/to/playlist/folder"
```

### AI Metadata Fixing (Optional)

Clean and standardize metadata using local AI:

```bash
# Set up Ollama (one-time setup)
./setup_ollama.sh

# Fix metadata for a folder
python spotdl/metadata_fixer.py "path/to/music/folder"

# Interactive mode (review each change)
python spotdl/metadata_fixer.py --interactive "path/to/music/folder"

# Use a different model (gpt-oss is default, qwen2.5:7b is faster)
python spotdl/metadata_fixer.py --model qwen2.5:7b "path/to/music/folder"
```

The AI will:

- Standardize artist names (e.g., "Beatles, The" → "The Beatles")
- Clean track titles (remove "(Remastered)", version info)
- Fix capitalization and remove problematic characters
- Add genre information

📖 **[Full AI Documentation](AI_METADATA_DOCS.md)** - Complete guide to AI metadata fixing

## VS Code Integration

This project includes comprehensive VS Code tasks for easy development and usage:

```bash
# Access via Command Palette (Cmd+Shift+P):
# "Tasks: Run Task" → Select from available tasks
```

### 🎵 **Quick Tasks Available:**

- **Download Playlist** - Download with playlist ID prompt
- **Download with AI Metadata Fixing** - One-step download + AI cleaning
- **Prepare Car Audio** - Convert latest download for car stereos
- **Start Ollama Server** - Launch AI server in background
- **Fix Metadata with AI** - Clean metadata for any folder

### 🔧 **Input Variables:**

- **Playlist ID**: Uses your `.env` file or prompts for input
- **Music Folder**: Defaults to downloads folder or specify custom path

📖 **[VS Code Tasks Guide](VSCODE_TASKS_GUIDE.md)** - Complete guide to all tasks and debug configurations

## Features in Detail

### Smart File Organization

- Creates folders named: `"Playlist Name - PlaylistID"`
- Files numbered: `01. Artist - Song.mp3`
- Handles duplicates with incremental naming

### Car Audio Optimization

- **ID3v2.3 tags** (maximum car stereo compatibility)
- **FAT32-friendly filenames** (no special characters)
- **Sequential numbering** for proper track order
- **Metadata includes**: Title, Artist, Album, Track Number, Genre

### Download Optimization

- **Avoids official videos** with intros/outros
- **Duration filtering** to prevent long videos
- **Fallback search** strategies for failed downloads
- **Audio-first formats** (M4A/MP3 priority)

## File Structure

```
downloads/
├── Playlist Name - PlaylistID/
│   ├── 01. Artist - Song.mp3
│   ├── 02. Artist - Song.mp3
│   └── ...
└── CarAudio/
    └── Playlist Name/
        ├── 01 - Song.mp3
        ├── 02 - Song.mp3
        └── ...
```

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
