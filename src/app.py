import webview
import threading
import src.core as core

class Api:
    def speak(self, text):
        threading.Thread(target=core.speak, args=(text,), daemon=True).start()
        return "ok"


html = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

<title>TTS</title>

<style>
body {
    background: linear-gradient(135deg, #0f172a, #1e293b, #334155);
    color: white;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    transition: background 0.5s ease;
}

.card {
    border-radius: 20px;
    background: rgba(30, 41, 59, 0.95);
    backdrop-filter: blur(15px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    border: 1px solid rgba(255,255,255,0.1);
    animation: fadeIn 0.8s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

textarea {
    resize: none;
    background: rgba(15, 23, 42, 0.8);
    color: white;
    border: 2px solid #334155;
    border-radius: 10px;
    transition: all 0.3s ease;
}

textarea:focus {
    background: rgba(15, 23, 42, 0.9);
    color: white;
    border-color: #6366f1;
    box-shadow: 0 0 10px rgba(99, 102, 241, 0.3);
}

.btn-primary {
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    border: none;
    border-radius: 25px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
}

.btn-primary:hover {
    background: linear-gradient(135deg, #4f46e5, #3730a3);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
}

.btn-outline-light {
    border-radius: 25px;
    transition: all 0.3s ease;
}

.btn-outline-light:hover {
    background: rgba(255,255,255,0.1);
    transform: translateY(-1px);
}

.logo {
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

#status {
    font-weight: 500;
    transition: color 0.3s ease;
}

/* Light theme */
body.light-theme {
    background: linear-gradient(135deg, #e0e7ff, #f8fafc);
    color: #1e293b;
}

body.light-theme .card {
    background: rgba(248, 250, 252, 0.95);
    border: 1px solid rgba(0,0,0,0.1);
}

body.light-theme textarea {
    background: rgba(241, 245, 249, 0.8);
    color: #1e293b;
    border: 2px solid #cbd5e1;
}

body.light-theme textarea:focus {
    border-color: #4f46e5;
    box-shadow: 0 0 10px rgba(79, 70, 229, 0.2);
}

body.light-theme .btn-outline-light {
    border-color: #cbd5e1;
    color: #475569;
}

body.light-theme .btn-outline-light:hover {
    background: rgba(203, 213, 225, 0.1);
    color: #334155;
}

body.light-theme #status {
    color: #64748b;
}

</style>
</head>
<body>

<div class="container d-flex justify-content-center align-items-center vh-100">
    <div class="card shadow-lg p-4" style="width: 520px;">
        
        <div class="text-center mb-3">
            <div class="logo mb-2">
                <svg width="60" height="60" viewBox="0 0 60 60" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="30" cy="30" r="28" fill="url(#gradient)" stroke="#6366f1" stroke-width="2"/>
                    <path d="M20 25 L25 20 L30 25 L35 20 L40 25 L35 30 L40 35 L35 40 L30 35 L25 40 L20 35 L25 30 Z" fill="white"/>
                    <defs>
                        <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" style="stop-color:#6366f1;stop-opacity:1" />
                            <stop offset="100%" style="stop-color:#4f46e5;stop-opacity:1" />
                        </linearGradient>
                    </defs>
                </svg>
            </div>
            <h3>🎙️ AI TTS</h3>
        </div>

        <div class="d-flex justify-content-end mb-2">
            <button class="btn btn-sm btn-outline-light" onclick="toggleTheme()" id="themeToggle">
                <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M8 11a3 3 0 1 1 0-6 3 3 0 0 1 0 6zm0 1a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM8 0a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 0zm0 13a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 0zm8-5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2a.5.5 0 0 1 .5.5zM3 8a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2A.5.5 0 0 1 3 8zm10.657-5.657a.5.5 0 0 1 0 .707l-1.414 1.415a.5.5 0 1 1-.707-.708l1.414-1.414a.5.5 0 0 1 .707 0zm-9.193 9.193a.5.5 0 0 1 0 .707L3.05 13.657a.5.5 0 0 1-.707-.707l1.414-1.414a.5.5 0 0 1 .707 0zm9.193 2.121a.5.5 0 0 1-.707 0l-1.414-1.414a.5.5 0 1 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .707zM4.464 4.465a.5.5 0 0 1-.707 0L2.343 3.05a.5.5 0 1 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .708z"/>
                </svg>
            </button>
        </div>

        <textarea id="text" class="form-control mb-3" rows="8" placeholder="텍스트를 입력하세요..."></textarea>

        <div class="progress mb-3" style="display: none;" id="progressContainer">
            <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" style="width: 0%" id="progressBar"></div>
        </div>

        <div class="row g-2">
            <div class="col-8">
                <button class="btn btn-primary w-100" onclick="send()" id="playBtn">
                    <svg width="20" height="20" fill="currentColor" class="me-2" viewBox="0 0 16 16">
                        <path d="M11.536 14.01A8.473 8.473 0 0 0 14.026 8a8.473 8.473 0 0 0-2.49-6.01l-.708.707A7.476 7.476 0 0 1 13.025 8c0 2.071-.84 3.946-2.197 5.303l.708.707z"/>
                        <path d="M10.121 12.596A6.948 6.948 0 0 0 12.025 8a6.948 6.948 0 0 0-1.904-4.596l-.707.707A5.958 5.958 0 0 1 11.025 8a5.958 5.958 0 0 1-1.61 4.293l.707.707z"/>
                        <path d="M8.707 11.889a4.924 4.924 0 0 0 1.618-3.889 4.924 4.924 0 0 0-1.618-3.889l-.707.707A3.928 3.928 0 0 1 9 8a3.928 3.928 0 0 1-1.01 2.596l.707.707z"/>
                        <path d="M0 5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v6a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V5zm4 0H2v6h2V5z"/>
                    </svg>
                    재생
                </button>
            </div>
            <div class="col-4">
                <button class="btn btn-outline-light w-100" onclick="clearText()">
                    <svg width="16" height="16" fill="currentColor" class="me-2" viewBox="0 0 16 16">
                        <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z"/>
                    </svg>
                    지우기
                </button>
            </div>
        </div>

        <div class="text-center mt-3">
            <span id="status" class="text-secondary">대기 중</span>
        </div>

    </div>
</div>

<script>
let isDark = true;

function toggleTheme() {
    isDark = !isDark;
    document.body.classList.toggle('light-theme', !isDark);
    const icon = document.querySelector('#themeToggle svg');
    if (isDark) {
        icon.innerHTML = '<path d="M8 11a3 3 0 1 1 0-6 3 3 0 0 1 0 6zm0 1a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM8 0a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 0zm0 13a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 0zm8-5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2a.5.5 0 0 1 .5.5zM3 8a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2A.5.5 0 0 1 3 8zm10.657-5.657a.5.5 0 0 1 0 .707l-1.414 1.415a.5.5 0 0 1-.707-.708l1.414-1.414a.5.5 0 0 1 .707 0zm-9.193 9.193a.5.5 0 0 1 0 .707L3.05 13.657a.5.5 0 0 1-.707-.707l1.414-1.414a.5.5 0 0 1 .707 0zm9.193 2.121a.5.5 0 0 1-.707 0l-1.414-1.414a.5.5 0 0 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .707zM4.464 4.465a.5.5 0 0 1-.707 0L2.343 3.05a.5.5 0 0 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .708z"/>';
    } else {
        icon.innerHTML = '<path d="M6 .278a.768.768 0 0 1 .08.858 7.208 7.208 0 0 0-.878 3.46c0 4.021 3.278 7.277 7.318 7.277.527 0 1.04-.055 1.533-.16a.787.787 0 0 1 .81.316.733.733 0 0 1-.031.893A8.349 8.349 0 0 1 8.344 16C3.734 16 0 12.286 0 7.71 0 4.266 2.114 1.312 5.124.06A.752.752 0 0 1 6 .278z"/>';
    }
}

function showProgress() {
    document.getElementById('progressContainer').style.display = 'block';
    const progressBar = document.getElementById('progressBar');
    progressBar.style.width = '0%';
    let progress = 0;
    const interval = setInterval(() => {
        progress += 10;
        progressBar.style.width = progress + '%';
        if (progress >= 100) {
            clearInterval(interval);
            setTimeout(() => {
                document.getElementById('progressContainer').style.display = 'none';
            }, 500);
        }
    }, 100);
}

function send() {
    let text = document.getElementById("text").value;

    if (!text.trim()) {
        alert("텍스트를 입력하세요");
        return;
    }

    document.getElementById("status").innerText = "음성 생성 중...";
    document.getElementById("playBtn").disabled = true;

    showProgress();

    window.pywebview.api.speak(text);

    setTimeout(() => {
        document.getElementById("status").innerText = "재생 완료";
        document.getElementById("playBtn").disabled = false;
    }, 2000);
}

function clearText() {
    document.getElementById("text").value = "";
}
</script>

</body>
</html>
"""


if __name__ == "__main__":
    api = Api()

    webview.create_window(
        "TTS",
        html=html,
        js_api=api,
        width=600,
        height=520
    )

    webview.start(gui='qt')