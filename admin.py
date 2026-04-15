from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>접속 정보 확인</title>
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
        .row {
            margin: 12px 0;
            font-size: 1.05rem;
            line-height: 1.6;
        }
        .label {
            color: #cbd5e1;
            font-weight: bold;
        }
        .value {
            color: #f8fafc;
            word-break: break-all;
        }
        .notice {
            margin-top: 24px;
            padding: 14px;
            border-radius: 12px;
            background: #334155;
            color: #e2e8f0;
            font-size: 0.95rem;
        }
    </style>
</head>
<body>
    <div class="box">
        <h1>접속 정보</h1>

        <div class="row"><span class="label">IP 주소:</span> <span class="value">{{ ip }}</span></div>
        <div class="row"><span class="label">국가:</span> <span class="value">{{ country }}</span></div>
        <div class="row"><span class="label">지역:</span> <span class="value">{{ region }}</span></div>
        <div class="row"><span class="label">도시:</span> <span class="value">{{ city }}</span></div>
        <div class="row"><span class="label">ISP:</span> <span class="value">{{ isp }}</span></div>

        <div class="notice">
            위치 정보는 IP 기반 추정값이라 실제 위치와 다를 수 있습니다.
        </div>
    </div>
</body>
</html>
"""


def get_real_ip() -> str:
    """
    Render 같은 프록시 환경에서는 X-Forwarded-For를 우선 사용.
    여러 IP가 있으면 첫 번째가 원래 클라이언트 IP인 경우가 많음.
    """
    x_forwarded_for = request.headers.get("X-Forwarded-For", "")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()

    x_real_ip = request.headers.get("X-Real-IP", "")
    if x_real_ip:
        return x_real_ip.strip()

    return request.remote_addr or "UNKNOWN"


def get_ip_info(ip: str) -> dict:
    """
    무료 IP 위치 조회 API 사용.
    """
    default_data = {
        "country": "알 수 없음",
        "region": "알 수 없음",
        "city": "알 수 없음",
        "isp": "알 수 없음",
    }

    try:
        # ip-api.com의 단순 조회 형식
        url = f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,isp,message"
        response = requests.get(url, timeout=5)
        data = response.json()

        if data.get("status") != "success":
            return default_data

        return {
            "country": data.get("country", "알 수 없음"),
            "region": data.get("regionName", "알 수 없음"),
            "city": data.get("city", "알 수 없음"),
            "isp": data.get("isp", "알 수 없음"),
        }
    except Exception:
        return default_data


@app.route("/")
def home():
    ip = get_real_ip()
    info = get_ip_info(ip)

    return render_template_string(
        HTML,
        ip=ip,
        country=info["country"],
        region=info["region"],
        city=info["city"],
        isp=info["isp"],
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)