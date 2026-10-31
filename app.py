from flask import Flask, request, redirect, session, render_template_string
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]

ADMIN_PASSWORD = os.environ["ADMIN_PASSWORD"]
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

site = {
    "baslik": "ASLANLAR BOYACILIK",
    "sehir": "DİYARBAKIR",
    "hizmet": "Boya - Badana - Dekorasyon",
    "telefon": "0532 289 82 71"
}

@app.route("/")
def home():
    return f"""
    <html><meta charset="UTF-8">
    <meta name="viewport" content="width=device-width">
    <body style="background:black;color:white;text-align:center;padding:30px;font-family:Arial">
    <h1 style="color:gold">🦁 {site['baslik']}</h1>
    <h2>{site['sehir']}</h2>
    <h3>{site['hizmet']}</h3>
    <p>İç Cephe Boya</p><p>Dış Cephe Boya</p>
    <p>Profesyonel Boya Hizmetleri</p>
    <h2>{site['telefon']}</h2>
    <a style="color:gold" href="tel:+90{site['telefon'].replace(' ','')}">HEMEN ARA</a>
    <p><a style="color:gold" href="/admin">Yönetici Girişi</a></p>
    </body></html>
    """

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST" and not session.get("giris"):
        if request.form.get("sifre") == ADMIN_PASSWORD:
            session["giris"] = True
            return redirect("/admin")
        return "Şifre yanlış. Geri dönüp tekrar deneyin."

    if not session.get("giris"):
        return """
        <html><meta charset="UTF-8"><body style="background:black;color:white;text-align:center;padding:40px">
        <h2 style="color:gold">ASLANLAR YÖNETİCİ PANELİ</h2>
        <form method="post">
        <input name="sifre" type="password" placeholder="Yönetici şifresi" required>
        <button type="submit">Giriş</button>
        </form></body></html>
        """

    if request.method == "POST":
        site["baslik"] = request.form.get("baslik", site["baslik"])
        site["sehir"] = request.form.get("sehir", site["sehir"])
        site["hizmet"] = request.form.get("hizmet", site["hizmet"])
        site["telefon"] = request.form.get("telefon", site["telefon"])
        return redirect("/admin")

    return render_template_string("""
    <html><meta charset="UTF-8"><body style="background:#111;color:white;text-align:center;padding:25px;font-family:Arial">
    <h2 style="color:gold">🦁 YÖNETİCİ PANELİ</h2>
    <form method="post">
    <p>Site başlığı</p><input name="baslik" value="{{s.baslik}}">
    <p>Şehir</p><input name="sehir" value="{{s.sehir}}">
    <p>Hizmet açıklaması</p><input name="hizmet" value="{{s.hizmet}}">
    <p>Telefon</p><input name="telefon" value="{{s.telefon}}">
    <p><button type="submit">Değişiklikleri Kaydet</button></p>
    </form>
    <p><a style="color:gold" href="/">Siteyi Gör</a></p>
    <p><a style="color:gold" href="/cikis">Çıkış Yap</a></p>
    </body></html>
    """, s=site)

@app.route("/cikis")
def cikis():
    session.clear()
    return redirect("/admin")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5002)))
