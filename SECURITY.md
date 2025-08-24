# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability within this project, please follow these steps:

1. **DO NOT** disclose the vulnerability publicly
2. Create a private GitHub security advisory or email the maintainer
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will acknowledge receipt within 48 hours and work with you to address the issue promptly.

## Security Considerations

This project handles Spotify API credentials and downloads content from the internet. Please:

- Never commit `.env` files with real credentials
- Keep your Spotify API credentials secure
- Be aware of copyright laws when downloading music
- Regularly update dependencies to patch security vulnerabilities
- Run the project in a sandboxed environment if handling untrusted playlists
