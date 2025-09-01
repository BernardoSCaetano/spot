# Spotify Playlist MP3 Downloader

A Python tool that downloads tracks from Spotify playlists (including private ones) and converts them to MP3 files with car audio system optimization.

## 🎵 Features

- **Spotify Integration**: Download from private playlists with OAuth authentication
- **Smart Search**: Optimized YouTube queries to avoid official videos/intros
- **Car Audio Ready**: Generates ID3v2.3 metadata for maximum car stereo compatibility
- **Auto Organization**: Creates playlist-named folders with numbered tracks
- **Progress Tracking**: Real-time download status with success/failure indicators
- **Duplicate Handling**: Prevents overwrites with intelligent file naming

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/BernardoSCaetano/spot.git
cd spot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup environment
cp .env.example .env
# Edit .env with your Spotify credentials

# 4. Run the downloader
python spotdl/main.py
```

## 📖 Full Documentation

See [README.md](README.md) for complete setup instructions, Spotify API configuration, and usage examples.

## 🔒 Security

This project uses environment variables to protect your Spotify credentials. Never commit your `.env` file to version control.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.
