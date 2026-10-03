from flask import Flask, render_template, request, send_file, after_this_request
import yt_dlp
import os
import uuid
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed

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
# COMMON OPTIONS
# --------------------------------------------------

def get_common_options():

    return {
        "noplaylist": True,
        "concurrent_fragment_downloads": 8,
        "retries": 10,
        "fragment_retries": 10,
        "buffersize": 1024 * 1024,
        "js_runtimes": {
            "deno": {}
        },
        "quiet": False,
        "no_warnings": False,
        "extract_flat": False
    }


# --------------------------------------------------
# VIDEO OPTIONS
# --------------------------------------------------

def get_video_options(quality, output_template):

    options = get_common_options()

    if quality == "best":

        video_format = (
            "bv*+ba/"
            "b"
        )

    elif quality == "1080":

        video_format = (
            "bv*[height<=1080]+ba/"
            "b[height<=1080]"
        )

    elif quality == "720":

        video_format = (
            "bv*[height<=720]+ba/"
            "b[height<=720]"
        )

    elif quality == "480":

        video_format = (
            "bv*[height<=480]+ba/"
            "b[height<=480]"
        )

    elif quality == "360":

        video_format = (
            "bv*[height<=360]+ba/"
            "b[height<=360]"
        )

    else:

        video_format = "bv*+ba/b"

    options.update({

        "format": video_format,

        "outtmpl": output_template,

        # FFmpeg combines video + audio
        "merge_output_format": "mp4"
    })

    return options


# --------------------------------------------------
# AUDIO OPTIONS
# --------------------------------------------------

def get_audio_options(quality, output_template):

    options = get_common_options()

    if quality == "320":

        audio_quality = "320"

    elif quality == "192":

        audio_quality = "192"

    else:

        audio_quality = "128"

    options.update({

        # Select the best available audio stream
        "format": "bestaudio/best",

        "outtmpl": output_template,

        # Convert to MP3 using FFmpeg
        "postprocessors": [

            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": audio_quality
            }

        ]
    })

    return options


# --------------------------------------------------
# SINGLE DOWNLOAD
# --------------------------------------------------

def download_single(url, mode, quality):

    file_id = str(uuid.uuid4())

    output_template = os.path.join(
        DOWNLOAD_FOLDER,
        file_id + ".%(ext)s"
    )

    # Select options
    if mode == "audio":

        options = get_audio_options(
            quality,
            output_template
        )

    else:

        options = get_video_options(
            quality,
            output_template
        )

    try:

        print()
        print("--------------------------------")
        print("Downloading:")
        print(url)
        print("Mode:", mode)
        print("Quality:", quality)
        print("--------------------------------")

        with yt_dlp.YoutubeDL(options) as ydl:

            info = ydl.extract_info(
                url,
                download=True
            )

            downloaded_file = ydl.prepare_filename(
                info
            )

        # Original file without extension
        base_name = os.path.splitext(
            downloaded_file
        )[0]

        possible_files = [

            downloaded_file,

            base_name + ".mp4",

            base_name + ".mp3",

            base_name + ".mkv",

            base_name + ".webm",

            base_name + ".m4a",

            base_name + ".opus"

        ]

        for file in possible_files:

            if os.path.exists(file):

                print(
                    "Download completed:",
                    file
                )

                return file

        # Extra safety check
        for file in os.listdir(
            DOWNLOAD_FOLDER
        ):

            if file.startswith(file_id):

                full_path = os.path.join(
                    DOWNLOAD_FOLDER,
                    file
                )

                if os.path.isfile(full_path):

                    print(
                        "Download completed:",
                        full_path
                    )

                    return full_path

        print(
            "Downloaded file could not be found."
        )

        return None

    except Exception as e:

        print()
        print("Download error:")
        print(e)
        print()

        return None


# --------------------------------------------------
# MAIN DOWNLOAD ROUTE
# --------------------------------------------------

@app.route(
    "/download",
    methods=["POST"]
)
def download():

    urls_text = request.form.get(
        "video_urls",
        ""
    ).strip()

    mode = request.form.get(
        "mode",
        "video"
    )

    quality = request.form.get(
        "quality",
        "best"
    )

    # Check URL
    if not urls_text:

        return """
        <h2>No URL entered</h2>

        <p>
        Please enter at least one video URL.
        </p>

        <a href="/">
        Go Back
        </a>
        """

    # Get URLs line by line
    urls = [

        url.strip()

        for url in urls_text.splitlines()

        if url.strip()

    ]

    print()
    print("==============================")
    print("K DOWNLOADER")
    print("==============================")
    print("Mode:", mode)
    print("Quality:", quality)
    print("Number of URLs:", len(urls))
    print("==============================")
    print()

    # --------------------------------------------------
    # BULK DOWNLOAD
    # --------------------------------------------------

    if len(urls) > 1:

        # FIXED: initialize list
        downloaded_files = []

        # Maximum 3 videos at once
        with ThreadPoolExecutor(
            max_workers=3
        ) as executor:

            tasks = {

                executor.submit(
                    download_single,
                    url,
                    mode,
                    quality
                ): url

                for url in urls

            }

            for task in as_completed(tasks):

                url = tasks[task]

                try:

                    result = task.result()

                    if result:

                        downloaded_files.append(
                            result
                        )

                        print(
                            "Completed:",
                            url
                        )

                    else:

                        print(
                            "Failed:",
                            url
                        )

                except Exception as e:

                    print(
                        "Error:",
                        url,
                        e
                    )

        # No successful downloads
        if not downloaded_files:

            return """
            <h2>Download Failed</h2>

            <p>
            None of the videos could be downloaded.
            </p>

            <a href="/">
            Go Back
            </a>
            """

        # --------------------------------------------------
        # CREATE ZIP
        # --------------------------------------------------

        zip_name = os.path.join(
            DOWNLOAD_FOLDER,
            "K_Downloader_Bulk.zip"
        )

        with zipfile.ZipFile(
            zip_name,
            "w",
            zipfile.ZIP_DEFLATED
        ) as zip_file:

            for file in downloaded_files:

                zip_file.write(
                    file,
                    os.path.basename(file)
                )

        # --------------------------------------------------
        # CLEANUP
        # --------------------------------------------------

        @after_this_request
        def cleanup(response):

            try:

                for file in downloaded_files:

                    if os.path.exists(file):

                        os.remove(file)

                if os.path.exists(zip_name):

                    os.remove(zip_name)

            except Exception as e:

                print(
                    "Cleanup error:",
                    e
                )

            return response

        return send_file(

            zip_name,

            as_attachment=True,

            download_name=(
                "K_Downloader_Bulk.zip"
            )

        )

    # --------------------------------------------------
    # SINGLE DOWNLOAD
    # --------------------------------------------------

    else:

        file = download_single(
            urls[0],
            mode,
            quality
        )

        if not file:

            return """
            <h2>Download Failed</h2>

            <p>
            The selected video could not be downloaded.
            </p>

            <p>
            Please check the URL and try again.
            </p>

            <br>

            <a href="/">
            Go Back
            </a>
            """

        # Download name
        if mode == "audio":

            download_name = (
                "K_Downloader_Audio.mp3"
            )

        else:

            download_name = (
                "K_Downloader_Video.mp4"
            )

        # Delete server copy after download
        @after_this_request
        def cleanup(response):

            try:

                if os.path.exists(file):

                    os.remove(file)

            except Exception as e:

                print(
                    "Cleanup error:",
                    e
                )

            return response

        return send_file(

            file,

            as_attachment=True,

            download_name=download_name

        )


# --------------------------------------------------
# TRANSCRIPT DOWNLOAD
# --------------------------------------------------

@app.route(
    "/transcript",
    methods=["POST"]
)
def transcript():

    video_url = request.form.get(
        "transcript_url",
        ""
    ).strip()

    language = request.form.get(
        "language",
        "en"
    )

    if not video_url:

        return """
        <h2>Please enter a video URL.</h2>

        <a href="/">
        Go Back
        </a>
        """

    file_id = str(uuid.uuid4())

    output_template = os.path.join(
        DOWNLOAD_FOLDER,
        file_id + ".%(ext)s"
    )

    options = get_common_options()

    options.update({

        # Don't download the video
        "skip_download": True,

        # Download manually added subtitles
        "writesubtitles": True,

        # Download automatic captions
        "writeautomaticsubs": True,

        # Requested language
        "subtitleslangs": [
            language
        ],

        # VTT transcript
        "subtitlesformat": "vtt",

        "outtmpl": output_template
    })

    try:

        with yt_dlp.YoutubeDL(options) as ydl:

            ydl.download([
                video_url
            ])

        transcript_file = None

        # Find transcript file
        for file in os.listdir(
            DOWNLOAD_FOLDER
        ):

            if file.startswith(file_id):

                if (
                    file.endswith(".vtt")
                    or
                    file.endswith(".srt")
                ):

                    transcript_file = os.path.join(
                        DOWNLOAD_FOLDER,
                        file
                    )

                    break

        if not transcript_file:

            return """
            <h2>Transcript Not Available</h2>

            <p>
            A transcript could not be found
            for this video or selected language.
            </p>

            <br>

            <a href="/">
            Go Back
            </a>
            """

        # Cleanup after sending
        @after_this_request
        def cleanup(response):

            try:

                if os.path.exists(
                    transcript_file
                ):

                    os.remove(
                        transcript_file
                    )

            except Exception as e:

                print(
                    "Transcript cleanup error:",
                    e
                )

            return response

        return send_file(

            transcript_file,

            as_attachment=True,

            download_name=(
                "K_Downloader_Transcript.vtt"
            )

        )

    except Exception as e:

        print()
        print(
            "Transcript error:",
            e
        )
        print()

        return f"""
        <h2>Transcript Download Failed</h2>

        <p>
        {str(e)}
        </p>

        <br>

        <a href="/">
        Go Back
        </a>
        """


# --------------------------------------------------
# RUN FLASK
# --------------------------------------------------

if __name__ == "__main__":

    app.run(

        debug=True,

        host="127.0.0.1",

        port=5000

    )