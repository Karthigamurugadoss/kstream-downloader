# 🎬 K Downloader – Video & Audio Downloader with Bulk Downloads and Transcript Support

A modern, lightweight **Python Flask-based video and audio downloader** with a clean web interface. K Downloader allows users to enter video URLs, choose video or audio format, select quality, download multiple URLs in bulk, and download available video transcripts/subtitles.

Built with **Python, Flask, HTML, CSS, JavaScript, yt-dlp, FFmpeg, and Deno**.

> ⚠️ **Important:** Use K Downloader only for content that you own or have permission to download, and only where downloading is permitted by the relevant platform's terms.

---

## ✨ Features

### 🎥 Video Download

Download supported online video content in different quality levels:

- Best Available Quality
- 1080p
- 720p
- 480p
- 360p

The application uses FFmpeg to combine separate video and audio streams when required.

---

### 🎵 Audio Download

Extract audio from supported videos and save it as MP3.

Available audio quality options:

- 320 kbps
- 192 kbps
- 128 kbps

---

### 📦 Bulk Video & Audio Downloads

K Downloader supports multiple URLs at the same time.

Simply enter multiple URLs, one per line:

```text
https://example.com/video1
https://example.com/video2
https://example.com/video3
