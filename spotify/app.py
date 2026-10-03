from flask import Flask, render_template, request, send_file, jsonify, after_this_request
import subprocess
import os
import uuid
import zipfile
import json
import re

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# --------------------------------------------------
# URL VALIDATION
# --------------------------------------------------

def is_spotify_url(url):
    return bool(re.match(
        r"https?://open\.spotify\.com/(track|playlist|album)/[a-zA-Z0-9]+",
        url
    ))


def get_link_type(url):
    if "/track/" in url:
        return "track"
    elif "/playlist/" in url:
        return "playlist"
    elif "/album/" in url:
        return "album"
    return "unknown"


# --------------------------------------------------
# METADATA ROUTE
# --------------------------------------------------

@app.route("/metadata", methods=["POST"])
def metadata():
    url = request.json.get("url", "").strip()

    if not url or not is_spotify_url(url):
        return jsonify({"error": "Invalid Spotify URL"}), 400

    link_type = get_link_type(url)

    try:
        result = subprocess.run(
            ["spotdl", "save", url, "--save-file", "-"],
            capture_output=True, text=True, timeout=30
        )

        if result.returncode != 0:
            return jsonify({
                "type": link_type,
                "name": link_type.capitalize(),
                "count": "?"
            })

        try:
            data = json.loads(result.stdout)
            count = len(data) if isinstance(data, list) else 1
            name = data[0].get("name", link_type.capitalize()) if data else link_type.capitalize()
            artist = data[0].get("artists", [""])[0] if data else ""
            return jsonify({
                "type": link_type,
                "name": name if link_type == "track" else f"{count} tracks",
                "artist": artist,
                "count": count
            })
        except (json.JSONDecodeError, IndexError, KeyError):
            return jsonify({
                "type": link_type,
                "name": link_type.capitalize(),
                "count": "?"
            })

    except subprocess.TimeoutExpired:
        return jsonify({
            "type": link_type,
            "name": link_type.capitalize(),
            "count": "?"
        })
    except FileNotFoundError:
        return jsonify({
            "error": "spotdl is not installed. Run: pip install spotdl"
        }), 500


# --------------------------------------------------
# DOWNLOAD ROUTE
# --------------------------------------------------

@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("spotify_url", "").strip()
    audio_format = request.form.get("format", "mp3")
    quality = request.form.get("quality", "best")

    if not url:
        return """
        <h2>No URL entered</h2>
        <p>Please enter a Spotify URL.</p>
        <a href="/">Go Back</a>
        """

    if not is_spotify_url(url):
        return """
        <h2>Invalid URL</h2>
        <p>Please enter a valid Spotify track, playlist, or album URL.</p>
        <a href="/">Go Back</a>
        """

    session_id = str(uuid.uuid4())
    output_dir = os.path.join(DOWNLOAD_FOLDER, session_id)
    os.makedirs(output_dir, exist_ok=True)

    link_type = get_link_type(url)

    print()
    print("==============================")
    print("K SPOTIFY DOWNLOADER")
    print("==============================")
    print("URL:", url)
    print("Type:", link_type)
    print("Format:", audio_format)
    print("Quality:", quality)
    print("==============================")
    print()

    bitrate = "320k" if quality == "320" else "192k" if quality == "192" else "128k"

    cmd = [
        "spotdl", "download", url,
        "--output", output_dir,
        "--format", audio_format,
        "--bitrate", bitrate
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600
        )

        print("spotdl stdout:", result.stdout)
        if result.stderr:
            print("spotdl stderr:", result.stderr)

    except subprocess.TimeoutExpired:
        return """
        <h2>Download Timed Out</h2>
        <p>The download took too long. Try a smaller playlist.</p>
        <a href="/">Go Back</a>
        """
    except FileNotFoundError:
        return """
        <h2>spotdl Not Installed</h2>
        <p>Please install spotdl: <code>pip install spotdl</code></p>
        <a href="/">Go Back</a>
        """

    downloaded_files = []
    for f in os.listdir(output_dir):
        full_path = os.path.join(output_dir, f)
        if os.path.isfile(full_path):
            downloaded_files.append(full_path)

    if not downloaded_files:
        return """
        <h2>Download Failed</h2>
        <p>No files were downloaded. Check the URL and try again.</p>
        <a href="/">Go Back</a>
        """

    # --------------------------------------------------
    # SINGLE FILE
    # --------------------------------------------------

    if len(downloaded_files) == 1:

        file_path = downloaded_files[0]
        file_name = os.path.basename(file_path)

        @after_this_request
        def cleanup_single(response):
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                if os.path.exists(output_dir):
                    os.rmdir(output_dir)
            except Exception as e:
                print("Cleanup error:", e)
            return response

        return send_file(
            file_path,
            as_attachment=True,
            download_name=file_name
        )

    # --------------------------------------------------
    # MULTIPLE FILES — ZIP
    # --------------------------------------------------

    zip_name = os.path.join(
        DOWNLOAD_FOLDER,
        f"KSpotify_{session_id}.zip"
    )

    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in downloaded_files:
            zf.write(f, os.path.basename(f))

    @after_this_request
    def cleanup_bulk(response):
        try:
            for f in downloaded_files:
                if os.path.exists(f):
                    os.remove(f)
            if os.path.exists(output_dir):
                os.rmdir(output_dir)
            if os.path.exists(zip_name):
                os.remove(zip_name)
        except Exception as e:
            print("Cleanup error:", e)
        return response

    return send_file(
        zip_name,
        as_attachment=True,
        download_name="KSpotify_Playlist.zip"
    )


# --------------------------------------------------
# RUN FLASK
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5100
    )
