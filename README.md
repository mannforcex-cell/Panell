# 🤖 TeleBot Panel v2.1
**Termux Telegram Bot Manager — Hacker Edition**

---

## 📁 Senarai Fail

| Fail | Fungsi |
|---|---|
| `index.html` | Panel UI (hacker dark theme) |
| `server.py`  | Flask backend — semua API endpoints |
| `start.sh`   | Script mudah untuk jalankan panel |
| `install.sh` | Setup pertama kali — pasang semua pakej |

---

## 🚀 Setup (Pertama Kali)

```bash
# 1. Clone atau copy folder ke Termux
# 2. Masuk ke folder
cd TeleBotPanel

# 3. Jalankan installer
bash install.sh

# 4. Start panel
bash start.sh
```

Kemudian buka browser: **http://localhost:5000**

---

## ⚡ Jalankan Terus

```bash
python3 server.py
```

---

## 🔧 API Endpoints

| Method | Endpoint | Fungsi |
|---|---|---|
| GET  | `/api/browse` | Browse folder |
| GET  | `/api/locations` | Quick locations |
| POST | `/api/file/read` | Baca fail |
| POST | `/api/file/save` | Simpan fail |
| POST | `/api/file/new`  | Cipta fail baru |
| POST | `/api/file/delete` | Padam fail |
| POST | `/api/bot/run`   | Jalankan bot |
| POST | `/api/bot/stop`  | Hentikan bot |
| GET  | `/api/bot/status` | Status semua bot |
| POST | `/api/bot/logs`  | Ambil log bot |
| POST | `/api/terminal`  | Terminal command |

---

## 🌟 Ciri-ciri

- ✅ Browse fail `.py`, `.js`, `.sh`
- ✅ Editor dengan nombor baris
- ✅ Jalankan & hentikan bot
- ✅ Log output realtime
- ✅ Terminal panel bawah
- ✅ Language nodes indicator (PY3 · NODE · SH)
- ✅ Dark hacker UI dengan CRT scanlines
- ✅ Sokongan `.py` (python3), `.js` (node), `.sh` (bash)

---

## 📦 Keperluan

```
Python 3.x
flask
flask-cors
pyTelegramBotAPI  (untuk bot Telegram)
node              (optional, untuk .js bots)
```

Install manual:
```bash
pip install flask flask-cors pyTelegramBotAPI
```
