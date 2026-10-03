from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download_video():

    video_url = request.form.get("video_url", "").strip()

    if not video_url:
        return "Please enter a video URL."

    file_id = str(uuid.uuid4())

    output_template = os.path.join(
        DOWNLOAD_FOLDER,
        file_id + ".%(ext)s"
    )

    ydl_options = {
        # Automatically choose an available format
        "format": "bv*+ba/b",

        "outtmpl": output_template,

        "noplaylist": True,

        # Merge video and audio into MP4 when possible
        "merge_output_format": "mp4",

        # Use Deno for YouTube JavaScript processing
        "js_runtimes": {
            "deno": {}
        },

        "quiet": False,
        "no_warnings": False
    }

    try:

        print("\nStarting download...")
        print("Video URL:", video_url)

        with yt_dlp.YoutubeDL(ydl_options) as ydl:

            info = ydl.extract_info(
                video_url,
                download=True
            )

            downloaded_file = ydl.prepare_filename(info)

        # After merging, yt-dlp may change the extension to mp4
        possible_files = [
            downloaded_file,
            os.path.splitext(downloaded_file)[0] + ".mp4",
            os.path.splitext(downloaded_file)[0] + ".mkv",
            os.path.splitext(downloaded_file)[0] + ".webm"
        ]

        final_file = None

        for file in possible_files:

            if os.path.exists(file):
                final_file = file
                break

        if final_file:

            print("Download completed!")
            print("File:", final_file)

            return send_file(
                final_file,
                as_attachment=True,
                download_name="video.mp4"
            )

        return """
        <h2>Download Failed</h2>
        <p>The video was downloaded, but the file could not be located.</p>
        <br>
        <a href="/">Go Back</a>
        """

    except yt_dlp.utils.DownloadError as e:

        print("\nyt-dlp error:")
        print(e)

        return f"""
        <h2>Video Download Failed</h2>

        <p>yt-dlp could not download this video.</p>

        <p><b>Error:</b></p>

        <p>{str(e)}</p>

        <br>

        <a href="/">Go Back</a>
        """

    except Exception as e:

        print("\nUnexpected error:")
        print(e)

        return f"""
        <h2>An Error Occurred</h2>

        <p>{str(e)}</p>

        <br>

        <a href="/">Go Back</a>
        """


if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )