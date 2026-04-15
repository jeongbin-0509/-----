from flask import Flask, request, render_template_string
from datetime import datetime
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>접속 정보 안내</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #0f172a;
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .box {
            width: 90%;
            max-width: 700px;
            background: #1e293b;
            padding: 32px;
            border-radius: 18px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        h1 {
            margin-top: 0;
            color: #93c5fd;
        }
        p {
            line-height: 1.7;
            color: #e5e7eb;
        }
        .notice {
            margin-top: 20px;
            padding: 16px;
            border-radius: 12px;
            background: #334155;
            color: #f8fafc;
        }
        .small {
            font-size: 0.95rem;
            color: #cbd5e1;
            margin-top: 18px;
        }
    </style>
</head>
<body>
    <div class="box">
        <h1>접속 정보 안내</h1>
        <p>
            이 페이지에 접속하면 서버 보안 및 서비스 운영을 위해 귀하의 정보가 기록될 수 있습니다.
        </p>
        <div class="notice">
            현재 페이지는 안내용 예시 페이지입니다.
        </div>
        <p class="small">
            기록되는 정보: IP 주소, User-Agent, 접속 시각
        </p>
    </div>
</body>
</html>
"""

LOG_FILE = "access_log.txt"


def get_real_ip() -> str:
    x_forwarded_for = request.headers.get("X-Forwarded-For", "")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.remote_addr or "UNKNOWN"


def save_log(ip: str, user_agent: str) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{now}] IP={ip} | User-Agent={user_agent}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_line)


@app.route("/")
def home():
    ip = get_real_ip()
    user_agent = request.headers.get("User-Agent", "UNKNOWN")
    save_log(ip, user_agent)
    return render_template_string(HTML)


@app.route("/logs")
def logs():
    # 아주 간단한 관리자 확인용 예시
    if not os.path.exists(LOG_FILE):
        return "<pre>아직 로그가 없습니다.</pre>"

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    return f"<pre>{content}</pre>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)