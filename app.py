from flask import Flask, request, render_template_string
from collections import defaultdict
from time import time

app = Flask(__name__)

attempts = defaultdict(list)

PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Brute Force Lab</title>
<style>
body {
    font-family: Arial;
    background: #101827;
    color: white;
    text-align: center;
    padding: 30px;
}
.box {
    max-width: 360px;
    margin: 50px auto;
    padding: 25px;
    background: #1e293b;
    border-radius: 15px;
}
input, button {
    box-sizing: border-box;
    width: 100%;
    padding: 12px;
    margin: 8px 0;
    border-radius: 8px;
}
button {
    background: #38bdf8;
    cursor: pointer;
}
</style>
</head>
<body>
<div class="box">
<h1>🔐 مختبر الحماية</h1>
<p>تجربة تعليمية لأمان تسجيل الدخول</p>
<form method="post">
<input name="username" placeholder="اسم المستخدم" required>
<input name="password" type="password"
placeholder="كلمة المرور" required>
<button type="submit">تسجيل الدخول</button>
</form>
<p>{{ message }}</p>
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        now = time()
        ip = request.remote_addr or "unknown"

        attempts[ip] = [
            t for t in attempts[ip]
            if now - t < 60
        ]

        if len(attempts[ip]) >= 5:
            message = "تم إيقاف المحاولات مؤقتًا."
        else:
            attempts[ip].append(now)

            username = request.form.get("username", "")
            password = request.form.get("password", "")

            if username == "labuser" and password == "Demo-2026!":
                message = "نجح تسجيل الدخول التجريبي!"
            else:
                message = "بيانات الدخول غير صحيحة."

    return render_template_string(PAGE, message=message)

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run()
