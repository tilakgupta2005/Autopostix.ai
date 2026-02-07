import os
import subprocess

def video_trim(starttime:str,endtime:str,video_path:str,file_name:str):
    print(F"Triming Video..")
    starttime_str = str(starttime)
    endtime_str = str(endtime)
    FFMPEG_BINARY = rf"C:\Program Files\ffmpeg-2025-09-15-git-16b8a7805b-essentials_build\bin\ffmpeg.exe"
    command = [
    FFMPEG_BINARY,
    '-i', video_path,
    '-ss', starttime_str,
    '-to', endtime_str,
    '-c:v', 'libx264',
    '-crf', '23',
    '-preset', 'fast',
    '-c:a', 'copy',      
    '-y',
    file_name
]
    try:
        subprocess.run(
            command,
            check = True,stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        print(f"Successfully trimmed video and saved to: {file_name}")
        return True

    except subprocess.CalledProcessError as e:
        # This catches errors from ffmpeg (e.g., file not found, bad time)
        print(f"Error during ffmpeg execution:")
        print(f"Command: {' '.join(command)}")
        print(f"Error: {e.stderr.decode()}")
        return False
        
    except FileNotFoundError:
        # This catches the error if 'ffmpeg' isn't installed or not in PATH
        print(f"Error: '{FFMPEG_BINARY}' not found.")
        print("Please ensure ffmpeg is installed and in your system's PATH,")
        print(f"or set the 'FFMPEG_BINARY' environment variable.")
        return False

def video_concat(list_path:str,file_name:str):
    print(f"Concating Videos..")
    FFMPEG_BINARY = rf"C:\Program Files\ffmpeg-2025-09-15-git-16b8a7805b-essentials_build\bin\ffmpeg.exe"
# Assuming you want H.264 video and AAC audio (standard for MP4)

    command = [
    FFMPEG_BINARY,
    '-f', 'concat', 
    '-safe', '0', 
    '-i', list_path, 
    '-c:v', 'libx264',
    '-crf', '23',
    '-preset', 'fast',
    '-c:a', 'aac',
    '-b:a', '128k',
    '-map', '0',
    '-y', file_name
]

    try:
        subprocess.run(
            command,
            check = True,stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        print(f"Successfully Concated video and saved to: {file_name}")
        return True

    except subprocess.CalledProcessError as e:
        # This catches errors from ffmpeg (e.g., file not found, bad time)
        print(f"Error during ffmpeg execution:")
        print(f"Command: {' '.join(command)}")
        print(f"Error: {e.stderr.decode()}")
        return False
        
    except FileNotFoundError:
        # This catches the error if 'ffmpeg' isn't installed or not in PATH
        print(f"Error: '{FFMPEG_BINARY}' not found.")
        print("Please ensure ffmpeg is installed and in your system's PATH,")
        print(f"or set the 'FFMPEG_BINARY' environment variable.")
        return False

def get_video_length(video_path: str):
    cmd = [
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        video_path
    ]

    try:
        # Run ffprobe command
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )

        # Decode output and convert to float
        duration_seconds = float(result.stdout.decode().strip())

        # Convert to HH:MM:SS format
        hours = int(duration_seconds // 3600)
        minutes = int((duration_seconds % 3600) // 60)
        seconds = int(duration_seconds % 60)
        formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"

        print(f"🎞️ Video length: {formatted_time} ({duration_seconds:.2f} seconds)")
        return formatted_time

    except subprocess.CalledProcessError as e:
        print("❌ Error while running ffprobe.")
        print(e.stderr.decode())
        return None, None
    except ValueError:
        print("⚠️ Could not parse video duration.")
        return None, None

def add_bgm(video_path: str, bgm_path: str, file_name:str):
    print(f"Adding BGM..")
    FFMPEG_BINARY = rf"C:\Program Files\ffmpeg-2025-09-15-git-16b8a7805b-essentials_build\bin\ffmpeg.exe"
# Assuming the problem is in the python function that builds this command
    cmd = [
    FFMPEG_BINARY,
    '-y',
    '-i', video_path,
    '-i', bgm_path,
    '-filter_complex',
    '[0:a]volume=1.0[v_aud];[1:a]volume=0.04[bgm];[v_aud][bgm]amix=inputs=2:duration=first[aout]',
    '-map', '0:v',
    '-map', '[aout]',
    '-c:v', 'copy',
    '-c:a', 'aac',
    '-b:a', '320k',
    file_name
]
    try:
        subprocess.run(cmd,check = True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Successfully added BGM and saved to: {file_name}")
        return True

    except subprocess.CalledProcessError as e:
        # This catches errors from ffmpeg (e.g., file not found, bad time)
        print(f"Error during ffmpeg execution:")
        print(f"Command: {' '.join(cmd)}")
        print(f"Error: {e.stderr.decode()}")
        return False
        
    except FileNotFoundError:
        # This catches the error if 'ffmpeg' isn't installed or not in PATH
        print(f"Error: '{FFMPEG_BINARY}' not found.")
        print("Please ensure ffmpeg is installed and in your system's PATH,")
        print(f"or set the 'FFMPEG_BINARY' environment variable.")
        return False



# --- This is how you would USE the function ---
if __name__ == "__main__":
    
    # # 1. Define your files and times
    # input_video = "temp/s01QuLpjISc/s01QuLpjISc.mp4"  # CHANGE THIS to your video's path
    # output_video = "temp/s01QuLpjISc/clip1.mp4" # The name of the file to create
    # start = "00:00:30"
    # end = "00:00:41"

    # if os.path.exists(input_video):
    #     video_trim(start, end, input_video, output_video)
    # else:
    #     print(f"Input file not found: {input_video}")
        
    video_list = "temp/s01QuLpjISc/list.txt"
    conact_video = "temp/s01QuLpjISc/concat.mp4"
    video_concat(video_list, conact_video)