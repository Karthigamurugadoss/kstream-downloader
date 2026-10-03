<p align="center">
  <img src="screenshots/banner.png" alt="KStream — Smart Media Downloader" width="100%">
</p>

<p align="center">
  <strong>Open-source video downloader, audio extractor, and transcript downloader.</strong><br>
  Built with Python Flask and yt-dlp. Self-hosted. No limits.
</p>

<p align="center">
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white" alt="Python"></a>
  <a href="https://flask.palletsprojects.com"><img src="https://img.shields.io/badge/Flask-Web_Framework-000000?logo=flask&logoColor=white" alt="Flask"></a>
  <a href="https://github.com/yt-dlp/yt-dlp"><img src="https://img.shields.io/badge/yt--dlp-Media_Engine-FF0000?logo=youtube&logoColor=white" alt="yt-dlp"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License"></a>
  <a href="https://github.com/Karthigamurugadoss/kstream-downloader/stargazers"><img src="https://img.shields.io/github/stars/Karthigamurugadoss/kstream-downloader?style=social" alt="Stars"></a>
  <a href="https://karthigamurugadoss.github.io/kstream-downloader/"><img src="https://img.shields.io/badge/Website-Live_Demo-e8a03e?logo=googlechrome&logoColor=white" alt="Website"></a>
</p>

<p align="center">
  <a href="https://karthigamurugadoss.github.io/kstream-downloader/">Website</a> &nbsp;&middot;&nbsp;
  <a href="#features">Features</a> &nbsp;&middot;&nbsp;
  <a href="#getting-started">Getting Started</a> &nbsp;&middot;&nbsp;
  <a href="#usage">Usage</a> &nbsp;&middot;&nbsp;
  <a href="#supported-platforms">Platforms</a> &nbsp;&middot;&nbsp;
  <a href="#contributing">Contributing</a>
</p>

---

KStream is a modern, self-hosted web application that lets you download videos, extract audio as MP3, bulk download multiple URLs as a ZIP archive, and grab video transcripts — all from a clean, responsive browser interface. Powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp), it supports **YouTube, Instagram, Twitter/X, Facebook, and 1000+ websites**.

> **Disclaimer:** Only download content you own or have permission to use. Respect platform terms of service and copyright law.

---

## Screenshots

| Video / Audio Download | Transcript Download |
|:---:|:---:|
| ![Video Download](screenshots/kstream-hero.png) | ![Transcript](screenshots/kstream-transcript.png) |

<details>
<summary><strong>Mobile View</strong></summary>
<br>
<p align="center">
  <img src="screenshots/kstream-mobile.png" alt="KStream - Mobile View" width="300">
</p>
</details>

---

## Features

### Video Download

Download videos in multiple quality options with automatic video+audio merging via FFmpeg:

| Quality | Description |
|---------|-------------|
| Best | Highest available resolution |
| 1080p | Full HD |
| 720p | HD |
| 480p | Standard |
| 360p | Low bandwidth |

### Audio Extraction

Extract audio from any supported video and convert to MP3:

- **320 kbps** — Studio quality
- **192 kbps** — High quality
- **128 kbps** — Standard quality

### Bulk Download

Download multiple videos or audio files at once:

1. Paste multiple URLs (one per line)
2. Select format and quality
3. All files are packaged into a single ZIP download
4. Up to 3 concurrent downloads for speed

### Transcript / Subtitle Download

Download video transcripts and subtitles in VTT format:

- Supports manual subtitles and auto-generated captions
- Available languages: English, Tamil, Hindi, Telugu, Malayalam

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Python, Flask |
| Frontend | HTML5, CSS3, JavaScript |
| Media Engine | yt-dlp |
| Audio/Video Processing | FFmpeg |
| Concurrency | Python ThreadPoolExecutor |

---

## Getting Started

### Prerequisites

- **Python 3.8+** — [Download Python](https://www.python.org/downloads/)
- **FFmpeg** — [Download FFmpeg](https://ffmpeg.org/download.html) (must be in your system PATH)

### Installation

```bash
# Clone the repository
git clone https://github.com/Karthigamurugadoss/kstream-downloader.git
cd kstream-downloader

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Open your browser and go to **http://127.0.0.1:5000**

---

## Usage

### Download a Video

1. Open KStream in your browser
2. Paste a video URL into the text area
3. Select **Video (MP4)** and your preferred quality
4. Click **Download**

### Extract Audio

1. Paste a video URL
2. Switch format to **Audio (MP3)**
3. Choose bitrate (128 / 192 / 320 kbps)
4. Click **Download**

### Bulk Download

1. Paste multiple URLs, one per line
2. Select format and quality
3. Click **Download** — all files arrive as a single ZIP

### Get a Transcript

1. Switch to the **Transcript** tab
2. Paste the video URL
3. Select the language
4. Click **Get transcript** — downloads as a VTT file

---

## KSpotify — Spotify Downloader

This repo also includes **KSpotify**, a Spotify song and playlist downloader with the same design language.

### Features

- Download individual **tracks** from Spotify
- Download entire **playlists** and **albums** as a ZIP archive
- Multiple audio formats: **MP3**, **FLAC**, **OGG**
- Quality options: **320 kbps**, **192 kbps**, **128 kbps**
- Live link preview with track metadata
- Automatic album art and metadata embedding

### Run KSpotify

```bash
cd spotify
pip install -r ../requirements.txt
python app.py
```

Open your browser and go to **http://127.0.0.1:5100**

### How It Works

1. Paste a Spotify track, playlist, or album URL
2. Choose your preferred audio format and quality
3. Click **Download** — single tracks download directly, playlists arrive as a ZIP

> KSpotify uses [spotdl](https://github.com/spotDL/spotify-downloader) under the hood, which finds matching audio on YouTube and downloads it with proper Spotify metadata.

---

## Project Structure

```
kstream-downloader/
├── app.py              # Flask backend — video/audio/transcript routes
├── templates/
│   └── index.html      # KStream frontend UI
├── spotify/
│   ├── app.py          # Flask backend — Spotify download routes
│   └── templates/
│       └── index.html  # KSpotify frontend UI
├── screenshots/        # App screenshots
├── requirements.txt    # Python dependencies (Flask, yt-dlp, spotdl)
├── downloads/          # Temporary download directory (auto-created)
├── LICENSE
└── README.md
```

---

## Supported Platforms

KStream uses yt-dlp under the hood, which supports **1000+ websites** including:

YouTube, Instagram, Twitter/X, Facebook, Vimeo, Dailymotion, SoundCloud, TikTok, Reddit, Twitch, and [many more](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).

---

## Roadmap

- [ ] Download progress bar in the UI
- [ ] Playlist support
- [ ] Docker container for one-command deployment
- [ ] Dark/light theme toggle
- [ ] Download history

---

## Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

## Author

Built by **[Karthigamurugadoss](https://github.com/Karthigamurugadoss)**

---

<p align="center">
  <br>
  <a href="https://github.com/Karthigamurugadoss/kstream-downloader/stargazers"><img src="https://img.shields.io/github/stars/Karthigamurugadoss/kstream-downloader?style=for-the-badge&logo=github&label=Star%20this%20repo&color=e8a03e" alt="Star"></a>
  <br><br>
  <sub>If KStream saved you time, a star helps others find it too.</sub>
</p>
