import sys
import os
import yt_dlp
import dotenv
import whisper
import datetime
import subprocess

def download_video(url:str,session_id:str):
    v_path = None
    try:
        yt_dlp.YoutubeDL({}).cache.remove()
        print(f"Cleared yt-dlp cache.")
    except Exception as e:
        # It's not a critical error if cache can't be cleared, so we just warn.
        print(f"Warning: Could not clear yt-dlp cache. {e}")

    try:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': rf'temp\{session_id}\%(id)s.%(ext)s',
            'noplaylist': True,
            'cookies_from_browser': ('chrome',)    #fix required
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Fetching video info from: {url}")
            info = ydl.extract_info(url, download=True)
            video_id = info.get('id', 'N/A')
            print(f"Directory created {session_id} for video ID: {video_id}")
            print(f"Starting download...")
            ydl.download([url])
            v_path = rf'temp\{session_id}\{video_id}.mp4'
            print(f"Download complete! Video saved in {v_path}")

    except yt_dlp.utils.DownloadError as e:
        print(f"\nError: Could not download the video. Please check the URL and your connection.")
        print(f"Details: {e}")

    return v_path,video_id

def extract_audio(video_path:str):
    print(f"Extracting Audio")
    FFMPEG_BINARY = rf"C:\Program Files\ffmpeg-2025-09-15-git-16b8a7805b-essentials_build\bin\ffmpeg.exe"
    a_path = video_path.replace('.mp4', '.mp3')
    command = [
        FFMPEG_BINARY,
        '-i', video_path,
        '-vn',
        '-ab', '192k',
        a_path
    ]

    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True
        )
        
        print(f"Audio extracted successfully.")
        print(f"FFmpeg Output: {result.stdout.strip()}")
        print(f"Saved to: {a_path}")
        
        return a_path, True
        
    except FileNotFoundError:
        print(f"Error: FFmpeg binary not found. Check your PATH or FFMPEG_BINARY environment variable.")
        return None, False
        
    except subprocess.CalledProcessError as e:
        print(f"Error extracting audio: FFmpeg command failed with code {e.returncode}.")
        print(f"FFmpeg Error Output: {e.stderr.strip()}")
        return None, False
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None, False

def audio_to_text(audio_path: str):
    print(f"Converting Audio To Text..")
    t_path = audio_path.replace(".mp3", ".txt")
    model = whisper.load_model("small")
    result = model.transcribe(audio_path, word_timestamps=True)
    output_text = ""
    for segment in result["segments"]:
        for word in segment["words"]:
            start_time = word["start"]
            end_time = word["end"]

            # Format the timestamps
            start_str = (str(datetime.timedelta(seconds=start_time)).split(".")[0] + "." + str(int(str(start_time).split(".")[1][:3])))
            end_str = (str(datetime.timedelta(seconds=end_time)).split(".")[0] + "." + str(int(str(end_time).split(".")[1][:3])))

            line = f"[{start_str} --> {end_str}] {word['word']}"
            # print(line)
            output_text += line + "\n"

    # Save the word-level transcription
    with open(t_path, "w", encoding="utf-8") as f:
        f.write(output_text)
    print(f"Transcript saved in {t_path}")
    return t_path

if __name__ == "__main__":
    video_path,video_id = download_video("https://youtu.be/wYYgHwX6txk?si=2Fy55GVxesPgA7sS")
    audio_path,status = extract_audio(video_path)
    text_path = audio_to_text(audio_path)