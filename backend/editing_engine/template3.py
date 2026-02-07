import json
import os
from video_downloader import *
from highlight_finder import *
from video_editing import *
FFMPEG_BINARY = rf"C:\Program Files\ffmpeg-2025-09-15-git-16b8a7805b-essentials_build\bin\ffmpeg.exe"
def Temp3(video_url:str):
    global FFMPEG_BINARY
    
    video_path,video_id = download_video(video_url)
    audio_path,status = extract_audio(video_path)

    if(status):
     text_path = audio_to_text(audio_path)
    FindHighlights(text_path)
    file = json.load(open(rf'temp\{video_id}\{video_id}.json', 'r'))
    count = 0
    list = ""
    for i in file:
      starttime = i['startTime']
      endtime = i['endTime']
      clip = rf'clip_{count}.mp4'
      file_name = rf'temp\{video_id}\{clip}'
      video_trim(starttime,endtime,video_path,file_name)
      list = list + f"file '{clip}'\n"
      count += 1
    
    text_file = rf'temp\{video_id}\list.txt'
    try:
      with open(text_file, 'w') as file:
        # writes all strings in the iterable to the file
        file.writelines(list)
        print(rf"Successfully saved strings using writelines() to '{file_name}'")
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")

    list_path = rf'temp\{video_id}\list.txt'
    concat_file_name = rf'temp\{video_id}\concat.mp4'
    video_concat(list_path,concat_file_name)
    len = get_video_length(concat_file_name)
    video_path = rf'assests\gameplay.mp4'
    file_name = rf'temp\{video_id}\gameplay_trim.mp4'
    video_trim(0,len,video_path,file_name)

    crop_game_cmd = [
       FFMPEG_BINARY,
        '-y','-i',
        file_name,
        '-vf',
        'scale=-1:960,crop=1080:960', 
        '-c:v', 'libx264', '-crf', '18', '-preset', 'slow',
        '-an', 
        rf'temp/{video_id}/cropped_gameplay.mp4'
    ]
    try:
      subprocess.run(crop_game_cmd,check = True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      print("Cropped gameplay video successfully.")

    except subprocess.CalledProcessError as e:
        print(f"Error during croping game:")
        print(f"Command: {' '.join(crop_game_cmd)}")
        print(f"Error: {e.stderr.decode()}")
        
    except FileNotFoundError:
        print(f"Error: '{FFMPEG_BINARY}' not found.")
        print("Please ensure ffmpeg is installed and in your system's PATH,")
        print(f"or set the 'FFMPEG_BINARY' environment variable.")

    crop_video_cmd = [
       FFMPEG_BINARY,
        '-y','-i',
        concat_file_name,
        '-vf',
        'scale=-1:960,crop=1080:960', 
        '-c:v', 'libx264', '-crf', '18', '-preset', 'slow',
        '-c:a', 'copy', 
        rf'temp/{video_id}/cropped_video.mp4'
    ]
    try:
      subprocess.run(crop_video_cmd,check = True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      print("Cropped video successfully.")

    except subprocess.CalledProcessError as e:
        print(f"Error during croping video:")
        print(f"Command: {' '.join(crop_video_cmd)}")
        print(f"Error: {e.stderr.decode()}")
        
    except FileNotFoundError:
        print(f"Error: '{FFMPEG_BINARY}' not found.")
        print("Please ensure ffmpeg is installed and in your system's PATH,")
        print(f"or set the 'FFMPEG_BINARY' environment variable.")

    combine_video = [
    FFMPEG_BINARY,
    '-y', 
    '-i', rf'temp/{video_id}/cropped_video.mp4', 
    '-i', rf'temp/{video_id}/cropped_gameplay.mp4', 
    '-filter_complex', 
    '[0:v]pad=1080:960:(1080-iw)/2:0[top];[top][1:v]vstack=inputs=2', 
    '-c:v', 'libx264', 
    '-crf', '18',
    '-preset', 'slow',     
    rf'temp/{video_id}/combined_video_no_bgm.mp4'
    ]
    try:
      subprocess.run(combine_video,check = True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      print("Video combined successfully.")

    except subprocess.CalledProcessError as e:
        print(f"Error during combining video:")
        print(f"Command: {' '.join(combine_video)}")
        print(f"Error: {e.stderr.decode()}")
        
    except FileNotFoundError:
        print(f"Error: '{FFMPEG_BINARY}' not found.")
        print("Please ensure ffmpeg is installed and in your system's PATH,")
        print(f"or set the 'FFMPEG_BINARY' environment variable.")

    bgm_path = rf'assests\bgm.mp3' 
    add_bgm(rf'temp/{video_id}/combined_video_no_bgm.mp4', bgm_path, rf'temp/{video_id}/combined_video_bgm.mp4')

    return rf'temp\{video_id}\combined_video_bgm.mp4'
#Temp3("https://youtu.be/s01QuLpjISc?si=A8kfXWteA-ew4e9K")



