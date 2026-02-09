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
    print(f"Received request for Template 1 with URL: {url} and Session ID: {session_id}")
    file_path = Path(Temp1(url))
    shutil.copy(file_path, f"output/{session_id}.mp4")
    os.remove(file_path)
    return f"output/{session_id}.mp4"

@app.post("/template2")
def get_template2(url: str, session_id: str): 
    print(f"Received request for Template 2 with URL: {url} and Session ID: {session_id}")
    file_path = Path(Temp2(url))
    shutil.copy(file_path, f"output/{session_id}.mp4")
    os.remove(file_path)
    return f"output/{session_id}.mp4"

@app.post("/template3")
def get_template3(url: str, session_id: str): 
    print(f"Received request for Template 3 with URL: {url} and Session ID: {session_id}")
    file_path = Path(Temp3(url))
    shutil.copy(file_path, f"output/{session_id}.mp4")
    os.remove(file_path)
    return f"output/{session_id}.mp4"





