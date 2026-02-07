// Initialization
document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();
    initTheme();
    initAnimations();
});

// --- Theme Management ---
const themeToggle = document.getElementById('theme-toggle');
const themeIcon = document.getElementById('theme-icon');
const htmlElement = document.documentElement;

function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    htmlElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

themeToggle.addEventListener('click', () => {
    const currentTheme = htmlElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    htmlElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
});

function updateThemeIcon(theme) {
    const iconName = theme === 'dark' ? 'sun' : 'moon';
    themeIcon.setAttribute('data-lucide', iconName);
    lucide.createIcons(); // Re-render icon
}

// --- Smooth Scrolling ---
document.querySelectorAll('.start-free-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.getElementById('tool').scrollIntoView({ behavior: 'smooth' });
    });
});

// --- Video Logic & Validation ---
const previewBtn = document.getElementById('preview-btn');
const urlInput = document.getElementById('youtube-url');
const videoContainer = document.getElementById('video-preview-container');
const errorMsg = document.getElementById('error-msg');
const playerDiv = document.getElementById('player');

previewBtn.addEventListener('click', () => {
    const url = urlInput.value.trim();
    const videoId = extractVideoID(url);

    if (videoId) {
        errorMsg.classList.add('hidden');
        videoContainer.classList.remove('hidden');
        // Future backend integration: Pass videoId to backend API here
        playerDiv.innerHTML = `<iframe src="https://www.youtube.com/embed/${videoId}" allowfullscreen></iframe>`;
        videoContainer.scrollIntoView({ behavior: 'smooth' });
    } else {
        errorMsg.classList.remove('hidden');
        videoContainer.classList.add('hidden');
    }
});

function extractVideoID(url) {
    const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
    const match = url.match(regExp);
    return (match && match[2].length === 11) ? match[2] : null;
}

// --- Theme Selection ---
const themeCards = document.querySelectorAll('.theme-card');
let selectedTheme = "Minimal";

themeCards.forEach(card => {
    card.addEventListener('click', () => {
        themeCards.forEach(c => c.classList.remove('active'));
        card.classList.add('active');
        selectedTheme = card.dataset.themeName;
    });
});

// --- Processing Simulation ---
const createBtn = document.getElementById('create-reel-btn');
const processingContainer = document.getElementById('processing-container');
const mainTool = document.querySelector('.main-tool');

createBtn.addEventListener('click', () => {
    // Hide previous UI
    videoContainer.classList.add('hidden');
    urlInput.parentElement.classList.add('hidden');
    processingContainer.classList.remove('hidden');

    simulateProgress();
});

function simulateProgress() {
    const fill = document.getElementById('progress-fill');
    const statusText = document.getElementById('status-text');
    let progress = 0;

    const interval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress > 100) progress = 100;
        
        fill.style.width = `${progress}%`;

        // Update Step Highlights
        if (progress > 20) {
            document.getElementById('step-1').classList.add('active');
            statusText.innerText = "Detecting high-energy moments...";
        }
        if (progress > 50) {
            document.getElementById('step-2').classList.add('active');
            statusText.innerText = `Applying ${selectedTheme} template...`;
        }
        if (progress > 80) {
            document.getElementById('step-3').classList.add('active');
            statusText.innerText = "Syncing AI captions...";
        }

        if (progress === 100) {
            clearInterval(interval);
            setTimeout(() => {
                processingContainer.classList.add('hidden');
                document.getElementById('success-container').classList.remove('hidden');
            }, 800);
        }
    }, 600);
}

// --- FAQ Accordion ---
document.querySelectorAll('.faq-question').forEach(button => {
    button.addEventListener('click', () => {
        const answer = button.nextElementSibling;
        const icon = button.querySelector('i');
        
        const isOpen = answer.style.display === 'block';
        answer.style.display = isOpen ? 'none' : 'block';
        icon.style.transform = isOpen ? 'rotate(0deg)' : 'rotate(180deg)';
    });
});

// --- Scroll Reveal Animation ---
function initAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
}
/* create Session ID for video processing */
function createSessionId() {
    return 'sess_' + crypto.randomUUID();
}

/* Preview Reel Logic */
async function preview_reel(sessionId = videolink) {
    const videoUrl = `http://127.0.0.1:5501/output/${sessionId}.mp4`;
    const pendingPageUrl = `/output/${sessionId}.mp4`;

    try {
        const res = await fetch(videoUrl, { method: "HEAD" });

        if (res.ok) {
            // ✅ File exists → open video in NEW TAB
            window.open(videoUrl, "_blank");
            return;
        }
    } catch (err) {
        console.warn("Video not ready yet");
    }

    // ❌ File missing → open CUSTOM PAGE in new tab
    window.open(pendingPageUrl, `Your reel is being processed. Please check back later.\nVideo Link: http://127.0.0.1:5501/output/${sessionId}.mp4`);
}


/*API Call*/
async function callTemplateAPI({ template, youtubeUrl }) {
    const sessionId = createSessionId();
    let endpoint = template; // template1, template2, template3

    const apiUrl = new URL(`http://127.0.0.1:8000/${endpoint}`);
    apiUrl.searchParams.append("url", youtubeUrl);
    apiUrl.searchParams.append("session_id", sessionId);

    const response = await fetch(apiUrl.toString(), {
        method: "POST"
    });

    if (!response.ok) {
        throw new Error("API request failed");
    }

    videolink = response.text(); // returns: output/{session_id}.mp4
}
