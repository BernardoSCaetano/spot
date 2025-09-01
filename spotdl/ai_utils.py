#!/usr/bin/env python3
"""
AI Utility Module for Spotify Downloader

Centralizes all AI functionality using Ollama:
- Filename generation and cleaning
- Metadata standardization
- Artist name normalization
- Track title optimization

This module handles all AI interactions and provides fallbacks
when AI is not available.
"""

import json
import re
import time
from typing import Dict, Optional

import requests


class AIManager:
    """Centralized AI manager for all Spotify downloader AI features"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "gpt-oss"):
        self.base_url = base_url
        self.model = model
        self.session = requests.Session()
        self._available = None
        self._last_check = 0
        
        # AI prompts for different tasks
        self.filename_prompt = """Clean this music track information for a filename:
Artist: {artist}
Title: {title}

Rules:
1. Standardize artist names (e.g., "Beatles, The" → "The Beatles")
2. Clean track titles (remove "(Remastered)", version info, etc.)
3. Use format: "Artist - Title"
4. Remove special characters that cause file issues
5. Keep essential information only
6. Max 80 characters total

Respond with just the clean filename (no quotes, no extension):"""

        self.metadata_prompt = """Clean and standardize this music metadata:
Artist: {artist}
Title: {title}
Album: {album}

Rules:
1. Standardize artist names using music knowledge
2. Clean track titles while preserving essential information
3. Fix capitalization and formatting
4. Remove problematic characters for file systems
5. Add genre if determinable from the track info

Respond with JSON only:
{{"artist": "Clean Artist Name", "title": "Clean Track Title", "album": "Album Name", "genre": "Genre if known"}}"""
    
    def is_available(self) -> bool:
        """Check if Ollama is available (cached for 30 seconds)"""
        current_time = time.time()
        if self._available is not None and (current_time - self._last_check) < 30:
            return self._available
        
        try:
            response = self.session.get(f"{self.base_url}/api/tags", timeout=3)
            self._available = response.status_code == 200
            self._last_check = current_time
            return self._available
        except Exception:
            self._available = False
            self._last_check = current_time
            return False
    
    def _generate(self, prompt: str, timeout: int = 15) -> Optional[str]:
        """Generate response from Ollama with timeout"""
        if not self.is_available():
            return None
        
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
            
            response = self.session.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=timeout
            )
            
            if response.status_code == 200:
                result = response.json().get('response', '').strip()
                return result if result else None
        except Exception:
            pass
        return None
    
    def generate_clean_filename(self, artist: str, title: str) -> str:
        """Generate clean filename using AI or fallback"""
        # Try AI first
        if self.is_available():
            try:
                prompt = self.filename_prompt.format(artist=artist, title=title)
                ai_response = self._generate(prompt, timeout=10)
                
                if ai_response and len(ai_response) < 120:  # Reasonable filename length
                    # Validate AI response doesn't have problematic characters
                    clean_response = re.sub(r'[<>:"/\\|?*]', '', ai_response)
                    if clean_response.strip() and ' - ' in clean_response:
                        return clean_response.strip()
            except Exception:
                pass
        
        # Fallback to rule-based cleaning
        return self._fallback_clean_filename(artist, title)
    
    def clean_metadata(self, artist: str, title: str, album: str = "") -> Dict[str, str]:
        """Clean and standardize metadata using AI or fallback"""
        # Try AI first
        if self.is_available():
            try:
                prompt = self.metadata_prompt.format(artist=artist, title=title, album=album)
                ai_response = self._generate(prompt, timeout=15)
                
                if ai_response:
                    # Extract JSON from response
                    json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
                    if json_match:
                        try:
                            metadata = json.loads(json_match.group(0))
                            if isinstance(metadata, dict) and 'artist' in metadata and 'title' in metadata:
                                # Ensure all values are strings and clean
                                return {
                                    'artist': str(metadata.get('artist', artist))[:100],
                                    'title': str(metadata.get('title', title))[:100],
                                    'album': str(metadata.get('album', album))[:100],
                                    'genre': str(metadata.get('genre', ''))[:50]
                                }
                        except json.JSONDecodeError:
                            pass
            except Exception:
                pass
        
        # Fallback to rule-based cleaning
        return self._fallback_clean_metadata(artist, title, album)
    
    def _fallback_clean_filename(self, artist: str, title: str) -> str:
        """Fallback filename cleaning without AI"""
        # Basic cleaning rules
        artist = re.sub(r'\s*\(.*?\)\s*', '', artist)  # Remove (Remastered) etc
        title = re.sub(r'\s*\(.*?\)\s*', '', title)
        artist = re.sub(r'\s*-\s*\d{4}\s*.*', '', artist)  # Remove year info
        title = re.sub(r'\s*-\s*\d{4}\s*.*', '', title)
        
        # Handle "Artist, The" → "The Artist"
        if artist.endswith(', The'):
            artist = 'The ' + artist[:-5]
        elif artist.endswith(', A'):
            artist = 'A ' + artist[:-3]
        
        # Clean up whitespace
        artist = re.sub(r'\s+', ' ', artist).strip()
        title = re.sub(r'\s+', ' ', title).strip()
        
        return f"{artist} - {title}"
    
    def _fallback_clean_metadata(self, artist: str, title: str, album: str) -> Dict[str, str]:
        """Fallback metadata cleaning without AI"""
        cleaned_filename = self._fallback_clean_filename(artist, title)
        
        if ' - ' in cleaned_filename:
            clean_artist, clean_title = cleaned_filename.split(' - ', 1)
        else:
            clean_artist, clean_title = artist, title
        
        # Basic album cleaning
        clean_album = re.sub(r'\s*\(.*?\)\s*', '', album)
        clean_album = re.sub(r'\s+', ' ', clean_album).strip()
        
        return {
            'artist': clean_artist[:100],
            'title': clean_title[:100], 
            'album': clean_album[:100],
            'genre': ''
        }
    
    def get_status(self) -> Dict[str, str]:
        """Get AI system status information"""
        if self.is_available():
            try:
                # Get model info
                response = self.session.get(f"{self.base_url}/api/tags")
                if response.status_code == 200:
                    models = response.json().get('models', [])
                    model_names = [m['name'] for m in models]
                    current_model = self.model if self.model in model_names else 'Not found'
                    
                    return {
                        'status': 'Available',
                        'url': self.base_url,
                        'current_model': current_model,
                        'available_models': ', '.join(model_names[:3])  # Show first 3
                    }
            except Exception:
                pass
        
        return {
            'status': 'Unavailable',
            'url': self.base_url,
            'current_model': 'N/A',
            'available_models': 'N/A'
        }


# Global AI manager instance
ai = AIManager()


def get_ai_manager() -> AIManager:
    """Get the global AI manager instance"""
    return ai


def generate_clean_filename(artist: str, title: str) -> str:
    """Generate clean filename using AI (convenience function)"""
    return ai.generate_clean_filename(artist, title)


def clean_metadata(artist: str, title: str, album: str = "") -> Dict[str, str]:
    """Clean metadata using AI (convenience function)"""
    return ai.clean_metadata(artist, title, album)


def is_ai_available() -> bool:
    """Check if AI is available (convenience function)"""
    return ai.is_available()


def get_ai_status() -> Dict[str, str]:
    """Get AI status (convenience function)"""
    return ai.get_status()


def sanitize_for_filesystem(text: str) -> str:
    """Sanitize text for filesystem compatibility"""
    # Remove/replace problematic characters
    text = re.sub(r'[<>:"/\\|?*]', '', text)
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    # Remove leading/trailing spaces
    text = text.strip()
    # Limit length to avoid filesystem issues
    if len(text) > 200:
        text = text[:200]
    return text
