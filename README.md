# 🎬 Autopostix.ai

Autopostix.ai is an open-source project that converts long-form YouTube videos into **short, viral reels** using AI-powered highlight detection and automated video templates.

The project combines:
- 🎥 Video downloading & processing (FFmpeg)
- 🧠 AI highlight extraction (Gemini + Whisper)
- ⚡ FastAPI backend
- 🎨 Lightweight frontend (HTML, CSS, Vanilla JS)

This repository is open for **learning, experimentation, and community contributions**.

Input:- [https://youtu.be/kxRZkJidkMM?si=GvPAHIhQ5HGE8y79](https://youtu.be/kxRZkJidkMM?si=GvPAHIhQ5HGE8y79)

Output:- [https://drive.google.com/file/d/1PoF7OW4K6SWhEF_b4oDybwpQH1fP0ued/view?usp=drive_link](https://drive.google.com/file/d/1PoF7OW4K6SWhEF_b4oDybwpQH1fP0ued/view?usp=drive_link)

---

## ✨ Features

- Paste a YouTube link and preview the video
- AI-based highlight detection from transcripts
- Multiple reel templates
- Fire-and-forget video processing API
- FFmpeg-based video editing pipeline
- Clean separation of backend and frontend

---

## 🧱 Project Structure
```
Autopostix.ai/
├── backend/
│ ├── main.py # FastAPI entry point
│ ├── editing_engine/
│ │ ├── template1.py # Gameplay over video
│ │ ├── template2.py # Focused video
│ │ ├── template3.py # Video over gameplay
│ │ ├── video_downloader.py # yt-dlp + Whisper logic
│ │ ├── highlight_finder.py # Gemini highlight detection
│ │ └── video_editing.py # FFmpeg helpers
│ ├── init.py
│ └── .gitignore
│
├── frontend/
│ ├── index.html # UI
│ ├── style.css # Styling
│ ├── script.js # Client-side logic
│ └── .gitignore
│
├── assests/
│ ├── bgm.mp3 # Background Music
│ ├── gameplay.mp4 # Gameplay Videp
│
├── temp/ # Temporary processing files (ignored)
├── output/ # Generated reels (Important)
├── Requirements.txt
├── .env
├── .gitignore
└── LICENSE
```
---

## 🛠 Tech Stack

### Backend
- Python 3.10+
- FastAPI
- FFmpeg
- yt-dlp
- OpenAI Whisper
- Google Gemini API

### Frontend
- HTML5
- CSS3
- JavaScript

---

## 🚀 Getting Started

### 1️⃣ Clone the repository

```bash
git clone https://github.com/tilakgupta2005/Autopostix.ai.git
cd Autopostix.ai
```

### 2️⃣ Create and activate a virtual environment

```bash
 python -m venv .venv
```
```bash
.venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r Requirements.txt
```

### 4️⃣ Install FFmpeg
FFmpeg is **required** for video and audio processing.  
You must install it **before running the backend**.

**Download:- [https://drive.google.com/file/d/1DbenqIPB2Ke-xsMiPTXtPo3yGSz-LZYb/view?usp=sharing](https://drive.google.com/file/d/1DbenqIPB2Ke-xsMiPTXtPo3yGSz-LZYb/view?usp=sharing)**


**Unzip FFmpeg**
Unzip the downloaded file to any one of these locations (recommended):
```bash
C:\Program Files
```

**Add FFmpeg to PATH (IMPORTANT)**
Add FFmpeg to PATH (IMPORTANT)
Press Windows + R, type sysdm.cpl, press Enter
Go to Advanced → Environment Variables
Under System Variables, find Path
Click Edit → New
Add this path:
```bash
C:\Program Files\ffmpeg-2025-09-15-git-16b8a7805b-essentials_build\bin
```
Click OK → restart your terminal

**Verify Installation**
Open Command Prompt or PowerShell and run:
```bash
ffmpeg -version
ffprobe -version
```

### 5️⃣Configure environment variables

Create a .env file in the project root:
```bash
FFMPEG_BINARY="C:\Program Files\ffmpeg-2025-09-15-git-16b8a7805b-essentials_build\bin\ffmpeg.exe"
GEMINI_API_KEY="your_gemini_api_key_here"
```

### 6️⃣ Run the backend

From the project root:
```bash
uvicorn backend.main:app --reload
```

### 7️⃣ Run the frontend

Open this file directly in your browser:
```bash
frontend/index.html
```

---

## 📄 License

MIT License — Free to use, modify, and distribute.  
Please credit [@tilakgupta2005](https://github.com/tilakgupta2005) in any derivative works.

---

## 👤 Author

**Tilak Gupta**  
🔗 [Linktree](https://linktr.ee/tilakgupta2005)  
📬 [GitHub Profile](https://github.com/tilakgupta2005)

---
