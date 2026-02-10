from fastapi import FastAPI
from pathlib import Path
import shutil
import os

from backend.editing_engine.template1 import Temp1
from backend.editing_engine.template2 import Temp2
from backend.editing_engine.template3 import Temp3

app = FastAPI()

@app.post("/template1")
def get_template1(url: str, session_id: str):
    file_path = rf'temp\{session_id}\combined_video_bgm.mp4' 
    print(f"Received request for Template 1 with URL: {url} and Session ID: {session_id}")
    try:
        video_path, file_path = Temp1(url,session_id)
        video_path = Path(video_path)
        file_path = Path(file_path)
        shutil.copy(video_path, f"output/{session_id}.mp4")
        if file_path.exists() and file_path.is_dir():
            shutil.rmtree(file_path)
        return f"output/{session_id}.mp4"
    except Exception as e:
        if file_path.exists() and file_path.is_dir():
            shutil.rmtree(file_path)
        print(f"Error processing Template 1: {e}")

@app.post("/template2")
def get_template2(url: str, session_id: str): 
    file_path = rf'temp\{session_id}\combined_video_bgm.mp4'
    print(f"Received request for Template 2 with URL: {url} and Session ID: {session_id}")
    try:
        video_path, file_path = Temp2(url,session_id)
        video_path = Path(video_path)
        file_path = Path(file_path)
        shutil.copy(video_path, f"output/{session_id}.mp4")
        if file_path.exists() and file_path.is_dir():
            shutil.rmtree(file_path)
        return f"output/{session_id}.mp4"
    except Exception as e:
        if file_path.exists() and file_path.is_dir():
            shutil.rmtree(file_path)
        print(f"Error processing Template 2: {e}")

@app.post("/template3")
def get_template3(url: str, session_id: str): 
    file_path = rf'temp\{session_id}\combined_video_bgm.mp4'
    print(f"Received request for Template 3 with URL: {url} and Session ID: {session_id}")
    try:
        video_path, file_path = Temp3(url,session_id)
        video_path = Path(video_path)
        file_path = Path(file_path)
        shutil.copy(video_path, f"output/{session_id}.mp4")
        if file_path.exists() and file_path.is_dir():
            shutil.rmtree(file_path)
        return f"output/{session_id}.mp4"
    except Exception as e:
        if file_path.exists() and file_path.is_dir():
            shutil.rmtree(file_path)
        print(f"Error processing Template 3: {e}")