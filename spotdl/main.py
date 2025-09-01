import json
import os
import shutil
import sys
import time

import spotipy
import yt_dlp
from dotenv import load_dotenv
from mutagen.id3 import ID3, TALB, TCON, TIT2, TPE1, TRCK
from mutagen.mp3 import MP3
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables
load_dotenv()

# Spotify API credentials (loaded from environment variables)
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI', 'http://127.0.0.1:8888/callback')

# Playlist ID (loaded from environment variables)
PLAYLIST_ID = os.getenv('PLAYLIST_ID')

# Validate required environment variables
if not SPOTIPY_CLIENT_ID or not SPOTIPY_CLIENT_SECRET or not PLAYLIST_ID:
    print("❌ Missing required environment variables!")
    print("Please create a .env file with the following variables:")
    print("  SPOTIPY_CLIENT_ID=your_client_id")
    print("  SPOTIPY_CLIENT_SECRET=your_client_secret")
    print("  PLAYLIST_ID=your_playlist_id")
    print("\nSee .env.example for reference.")
    exit(1)

DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), 'downloads')
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Authenticate with Spotify with retry logic
def create_spotify_client():
    """Create Spotify client with retry mechanism"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=SPOTIPY_CLIENT_ID,
                client_secret=SPOTIPY_CLIENT_SECRET,
                redirect_uri=SPOTIPY_REDIRECT_URI,
                scope="playlist-read-private"
            ))
            # Test the connection
            sp.current_user()
            return sp
        except Exception as e:
            print(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                print("Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print("Failed to connect to Spotify after all retries.")
                raise

sp = create_spotify_client()

# Fetch playlist tracks
def get_playlist_tracks(playlist_id):
    """Fetch tracks from Spotify playlist with error handling"""
    try:
        # Get playlist info first
        playlist_info = sp.playlist(playlist_id, fields="name,id")
        playlist_name = sanitize_filename(playlist_info['name'])
        
        # Create playlist-specific download directory
        playlist_folder = f"{playlist_name} - {playlist_id}"
        playlist_download_dir = os.path.join(DOWNLOAD_DIR, playlist_folder)
        os.makedirs(playlist_download_dir, exist_ok=True)
        
        results = sp.playlist_tracks(playlist_id)
        if not results or 'items' not in results:
            print("No tracks found in playlist or invalid response.")
            return [], playlist_download_dir
            
        tracks = []
        for item in results['items']:
            if not item or not item.get('track'):
                continue
            track = item['track']
            track_id = track['id']  # Add Spotify track ID for tracking
            name = track['name']
            artists = ', '.join([artist['name'] for artist in track['artists']])
            duration_ms = track['duration_ms']
            tracks.append({
                'id': track_id,  # Spotify track ID for tracking
                'name': name,
                'artists': artists,
                'duration_ms': duration_ms,
                'search_query': f"{name} {artists}"
            })
        return tracks, playlist_download_dir
    except Exception as e:
        print(f"Error fetching playlist tracks: {e}")
        return [], DOWNLOAD_DIR

# Download tracking system
def get_tracking_file_path(download_dir):
    """Get the path to the tracking JSON file for a specific playlist folder"""
    return os.path.join(download_dir, '.download_tracking.json')

def load_download_tracking(download_dir):
    """Load the download tracking data from JSON file"""
    tracking_file = get_tracking_file_path(download_dir)
    try:
        if os.path.exists(tracking_file):
            with open(tracking_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load tracking file: {e}")
    return {}

def save_download_tracking(download_dir, tracking_data):
    """Save the download tracking data to JSON file"""
    tracking_file = get_tracking_file_path(download_dir)
    try:
        with open(tracking_file, 'w', encoding='utf-8') as f:
            json.dump(tracking_data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Warning: Could not save tracking file: {e}")

def is_track_downloaded(track_info, download_dir, tracking_data):
    """Check if a track has already been downloaded"""
    track_id = track_info['id']
    
    # Check if track ID exists in tracking data
    if track_id in tracking_data:
        tracked_file = tracking_data[track_id]['file_path']
        # Verify the file still exists
        if os.path.exists(tracked_file):
            return True, tracked_file
        else:
            # File was deleted, remove from tracking
            del tracking_data[track_id]
            save_download_tracking(download_dir, tracking_data)
    
    return False, None

def add_track_to_tracking(track_info, file_path, download_dir, tracking_data):
    """Add a successfully downloaded track to the tracking system"""
    track_id = track_info['id']
    tracking_data[track_id] = {
        'name': track_info['name'],
        'artists': track_info['artists'],
        'file_path': file_path,
        'download_date': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    save_download_tracking(download_dir, tracking_data)

# Download MP3 from YouTube
def download_mp3(track_info, track_number, total_tracks, download_dir, tracking_data):
    # Check if track is already downloaded
    is_downloaded, existing_file = is_track_downloaded(track_info, download_dir, tracking_data)
    if is_downloaded:
        print(f"[{track_number}/{total_tracks}] ⏭️  Skipping (already downloaded): {track_info['artists']} - {track_info['name']}")
        print(f"    File: {os.path.basename(existing_file)}")
        return True
    
    # Create optimized search query to avoid official videos
    search_query = f"{track_info['search_query']} audio -official -video -mv"
    
    # Get expected duration in seconds for filtering
    expected_duration = track_info['duration_ms'] / 1000
    max_duration = expected_duration + 60  # Allow 60 seconds extra
    
    # Create clean filename with track number to prevent overwrites
    clean_filename = f"{track_number:02d}. {track_info['artists']} - {track_info['name']}"
    clean_filename = sanitize_filename(clean_filename)
    
    # Handle existing files by adding incremental numbers
    base_path = os.path.join(download_dir, clean_filename)
    final_path = base_path
    counter = 1
    while os.path.exists(f"{final_path}.mp3"):
        final_path = f"{base_path} ({counter})"
        counter += 1
    
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',  # Prefer audio-only formats
        'outtmpl': f'{final_path}.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'match_filter': lambda info: None if info.get('duration', 0) <= max_duration else "Too long"
    }
    
    print(f"[{track_number}/{total_tracks}] 🔄 Downloading: {os.path.basename(final_path)}")
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([f"ytsearch:{search_query}"])
            final_file_path = f"{final_path}.mp3"
            if os.path.exists(final_file_path):
                print(f"✓ Successfully downloaded: {os.path.basename(final_path)}")
                # Add to tracking system
                add_track_to_tracking(track_info, final_file_path, download_dir, tracking_data)
                return True
        except Exception as e:
            print(f"✗ Failed to download {os.path.basename(final_path)}: {e}")
            # Fallback: try with just "audio" keyword
            fallback_query = f"{track_info['search_query']} audio"
            print(f"  Trying fallback search: {fallback_query}")
            try:
                ydl.download([f"ytsearch:{fallback_query}"])
                final_file_path = f"{final_path}.mp3"
                if os.path.exists(final_file_path):
                    print(f"✓ Fallback successful: {os.path.basename(final_path)}")
                    # Add to tracking system
                    add_track_to_tracking(track_info, final_file_path, download_dir, tracking_data)
                    return True
            except Exception as e2:
                print(f"✗ Fallback also failed: {e2}")
    
    return False

def sanitize_filename(filename):
    """Remove or replace characters that are problematic in filenames"""
    import re
    # Remove/replace problematic characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace multiple spaces with single space
    filename = re.sub(r'\s+', ' ', filename)
    # Remove leading/trailing spaces
    filename = filename.strip()
    # Limit length to avoid filesystem issues
    if len(filename) > 200:
        filename = filename[:200]
    return filename

def prepare_for_car_audio(source_dir, output_dir=None):
    """
    Prepare downloaded music for car audio systems (VW Passat CC compatible)
    
    Creates properly formatted MP3s with:
    - ID3v2.3 tags (UTF-16)
    - Car-friendly folder structure
    - Numbered filenames for proper ordering
    - FAT32 compatible names
    """
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(source_dir), "CarAudio")
    
    print("\n🚗 Preparing music for car audio system...")
    print(f"📂 Source: {source_dir}")
    print(f"📂 Output: {output_dir}")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all MP3 files
    mp3_files = []
    for file in os.listdir(source_dir):
        if file.lower().endswith('.mp3'):
            mp3_files.append(file)
    
    if not mp3_files:
        print("❌ No MP3 files found in source directory")
        return False
    
    # Sort files to maintain order
    mp3_files.sort()
    
    # Extract playlist/album name from folder
    folder_name = os.path.basename(source_dir)
    if " - " in folder_name:
        album_name = folder_name.split(" - ")[0]  # Get playlist name part
    else:
        album_name = folder_name
    
    # Create album folder
    album_folder = os.path.join(output_dir, sanitize_car_filename(album_name))
    os.makedirs(album_folder, exist_ok=True)
    
    success_count = 0
    
    for i, filename in enumerate(mp3_files, 1):
        try:
            source_path = os.path.join(source_dir, filename)
            
            # Parse filename to extract artist and title
            # Expected format: "NN. Artist - Title.mp3"
            base_name = os.path.splitext(filename)[0]
            
            if ". " in base_name and " - " in base_name:
                # Remove track number
                after_number = base_name.split(". ", 1)[1]
                if " - " in after_number:
                    artist, title = after_number.split(" - ", 1)
                else:
                    artist = "Unknown Artist"
                    title = after_number
            else:
                artist = "Unknown Artist"
                title = base_name
            
            # Create car-friendly filename
            car_filename = f"{i:02d} - {sanitize_car_filename(title)}.mp3"
            output_path = os.path.join(album_folder, car_filename)
            
            # Copy file
            shutil.copy2(source_path, output_path)
            
            # Update metadata for car compatibility
            try:
                audio = MP3(output_path, ID3=ID3)
                
                # Remove existing tags and add new ones (silently handle warnings)
                try:
                    audio.delete()
                except Exception:
                    pass  # Ignore if no tags exist
                
                # Add new tags
                audio.add_tags()
                
                # Add ID3v2.3 tags (car-compatible)
                audio.tags.add(TIT2(encoding=1, text=title))  # Title
                audio.tags.add(TPE1(encoding=1, text=artist))  # Artist
                audio.tags.add(TALB(encoding=1, text=album_name))  # Album
                audio.tags.add(TRCK(encoding=1, text=str(i)))  # Track number
                audio.tags.add(TCON(encoding=1, text="World Music"))  # Genre
                
                audio.save(v2_version=3)  # Save as ID3v2.3
                
                print(f"✓ [{i:02d}/{len(mp3_files)}] {car_filename}")
                success_count += 1
                
            except Exception as e:
                print(f"⚠️  Metadata error for {car_filename}: {e}")
                success_count += 1  # Still count as success since file was copied
                
        except Exception as e:
            print(f"❌ Failed to process {filename}: {e}")
    
    print("\n🎵 Car audio preparation complete!")
    print(f"✅ {success_count}/{len(mp3_files)} files processed")
    print(f"📁 Files ready for USB: {album_folder}")
    print("\n💡 USB Stick Tips:")
    print("   • Format as FAT32")
    print("   • Use USB 2.0 stick (≤32GB)")
    print(f"   • Copy entire '{album_name}' folder to USB root")
    
    return True

def sanitize_car_filename(filename):
    """Create car audio system friendly filenames"""
    import re
    # More aggressive sanitization for car systems
    filename = re.sub(r'[<>:"/\\|?*&%#@!]', '', filename)
    filename = re.sub(r'[áàâãäå]', 'a', filename)
    filename = re.sub(r'[éèêë]', 'e', filename)
    filename = re.sub(r'[íìîï]', 'i', filename)
    filename = re.sub(r'[óòôõö]', 'o', filename)
    filename = re.sub(r'[úùûü]', 'u', filename)
    filename = re.sub(r'[ñ]', 'n', filename)
    filename = re.sub(r'[ç]', 'c', filename)
    filename = re.sub(r'\s+', ' ', filename)
    filename = filename.strip()
    # Limit to 50 chars for car systems
    if len(filename) > 50:
        filename = filename[:50]
    return filename

if __name__ == "__main__":
    import sys
    
    # Check if user wants to prepare existing downloads for car audio
    if len(sys.argv) > 1 and sys.argv[1] == "--car-audio":
        if len(sys.argv) > 2:
            source_folder = sys.argv[2]
        else:
            # Use the most recent playlist folder
            download_folders = [f for f in os.listdir(DOWNLOAD_DIR) 
                              if os.path.isdir(os.path.join(DOWNLOAD_DIR, f))]
            if not download_folders:
                print("❌ No download folders found")
                exit(1)
            source_folder = os.path.join(DOWNLOAD_DIR, download_folders[-1])
        
        prepare_for_car_audio(source_folder)
        exit(0)
    
    print("Connecting to Spotify...")
    try:
        tracks, playlist_download_dir = get_playlist_tracks(PLAYLIST_ID)
        if not tracks:
            print("No tracks found. Please check your playlist ID and credentials.")
            exit(1)
        
        # Load tracking data for this playlist
        tracking_data = load_download_tracking(playlist_download_dir)
        
        total_tracks = len(tracks)
        new_tracks = []
        skipped_tracks = 0
        
        # Check which tracks are new
        for track in tracks:
            is_downloaded, _ = is_track_downloaded(track, playlist_download_dir, tracking_data)
            if not is_downloaded:
                new_tracks.append(track)
            else:
                skipped_tracks += 1
        
        print(f"Found {total_tracks} tracks in playlist.")
        print(f"Already downloaded: {skipped_tracks} tracks")
        print(f"New tracks to download: {len(new_tracks)} tracks")
        print(f"Download directory: {playlist_download_dir}")
        
        if new_tracks:
            print("Starting downloads...\n")
            success_count = 0
            
            for i, track in enumerate(tracks, 1):
                success = download_mp3(track, i, total_tracks, playlist_download_dir, tracking_data)
                if success:
                    success_count += 1
                print()  # Empty line for better readability
            
            print(f"Downloads complete! Successfully downloaded {success_count} new tracks.")
            print(f"Total tracks in playlist: {total_tracks}")
            print(f"Files saved to: {playlist_download_dir}")
        else:
            print("✅ All tracks already downloaded! No new downloads needed.")
        
        # Ask if user wants to prepare for car audio
        print("\n🚗 Prepare music for car audio system? (y/n): ", end="")
        if input().lower() in ['y', 'yes']:
            prepare_for_car_audio(playlist_download_dir)
            
    except KeyboardInterrupt:
        print("\nDownload interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please check your internet connection and Spotify credentials.")
