#!/usr/bin/env python3
"""
Telegram Bot Panel - Backend Server
Run: python server.py
Browser: http://localhost:5000
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess, os, threading, time

app = Flask(__name__, static_folder='.')
CORS(app)

running_bots = {}   # key = full_path, value = process
bot_logs    = {}    # key = full_path, value = list of log lines

HOME = os.path.expanduser("~")

# ── helpers ──────────────────────────────────────────────────
def safe_path(path):
    return os.path.realpath(os.path.expanduser(path or HOME))

def read_output(key, process):
    while True:
        if key not in running_bots:
            break
        try:
            line = process.stdout.readline()
            if line:
                bot_logs.setdefault(key, []).append({
                    "time": time.strftime("%H:%M:%S"),
                    "msg": line.decode('utf-8', errors='replace').strip()
                })
                if len(bot_logs[key]) > 300:
                    bot_logs[key] = bot_logs[key][-300:]
            elif process.poll() is not None:
                bot_logs.setdefault(key, []).append({
                    "time": time.strftime("%H:%M:%S"),
                    "msg": "⚠️ Bot process ended."
                })
                running_bots.pop(key, None)
                break
        except:
            break

# ── static ───────────────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# ── BROWSE ───────────────────────────────────────────────────
@app.route('/api/browse', methods=['GET'])
def browse():
    req_path = request.args.get('path', HOME)
    path = safe_path(req_path)

    if not os.path.isdir(path):
        return jsonify({"error": "Bukan folder"}), 400

    items = []
    try:
        entries = sorted(os.scandir(path), key=lambda e: (not e.is_dir(), e.name.lower()))
        for e in entries:
            if e.name.startswith('.'):
                continue
            try:
                is_dir = e.is_dir(follow_symlinks=True)
                if is_dir:
                    items.append({"name": e.name, "path": e.path, "type": "dir"})
                elif e.name.endswith('.py'):
                    st = e.stat()
                    items.append({
                        "name": e.name,
                        "path": e.path,
                        "type": "file",
                        "size": st.st_size,
                        "modified": time.strftime("%d/%m %H:%M", time.localtime(st.st_mtime))
                    })
            except PermissionError:
                continue
    except PermissionError:
        return jsonify({"error": "Tiada permission untuk buka folder ini"}), 403

    parent = str(os.path.dirname(path)) if path != "/" else None

    return jsonify({
        "current": path,
        "parent": parent,
        "home": HOME,
        "items": items
    })

@app.route('/api/locations', methods=['GET'])
def locations():
    locs = [
        {"label": "🏠 Home (~)",           "path": HOME},
        {"label": "📥 Downloads",           "path": os.path.join(HOME, "downloads")},
        {"label": "📂 storage/shared",      "path": os.path.expanduser("~/storage/shared")},
        {"label": "📂 storage/downloads",   "path": os.path.expanduser("~/storage/downloads")},
        {"label": "📂 storage/dcim",        "path": os.path.expanduser("~/storage/dcim")},
    ]
    return jsonify({"locations": [l for l in locs if os.path.isdir(l["path"])]})

# ── READ / SAVE / NEW / DELETE FILE ──────────────────────────
@app.route('/api/file/read', methods=['POST'])
def read_file():
    data = request.get_json()
    fpath = safe_path(data.get('path', ''))
    if not os.path.isfile(fpath):
        return jsonify({"error": "Fail tidak dijumpai"}), 404
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({"content": content, "path": fpath, "name": os.path.basename(fpath)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/file/save', methods=['POST'])
def save_file():
    data = request.get_json()
    fpath = safe_path(data.get('path', ''))
    content = data.get('content', '')
    try:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        return jsonify({"success": True, "message": "Fail disimpan!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/file/new', methods=['POST'])
def new_file():
    data = request.get_json()
    folder = safe_path(data.get('folder', HOME))
    name = data.get('name', 'bot.py').strip()
    if not name.endswith('.py'):
        name += '.py'
    fpath = os.path.join(folder, name)
    template = f'''# Bot Telegram - {name}
import telebot

TOKEN = "ISI_TOKEN_BOT_DI_SINI"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Bot aktif! 🤖")

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.reply_to(message, message.text)

print("Bot sedang berjalan...")
bot.polling(none_stop=True)
'''
    try:
        with open(fpath, 'w') as f:
            f.write(template)
        return jsonify({"success": True, "path": fpath, "name": name})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/file/delete', methods=['POST'])
def delete_file():
    data = request.get_json()
    fpath = safe_path(data.get('path', ''))
    if not os.path.isfile(fpath):
        return jsonify({"error": "Fail tidak dijumpai"}), 404
    running_bots.pop(fpath, None)
    try:
        os.remove(fpath)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ── RUN / STOP / STATUS / LOGS ───────────────────────────────
@app.route('/api/bot/run', methods=['POST'])
def run_bot():
    data = request.get_json()
    fpath = safe_path(data.get('path', ''))
    if not os.path.isfile(fpath):
        return jsonify({"error": "Fail tidak dijumpai"}), 404
    if fpath in running_bots:
        return jsonify({"error": "Bot sudah berjalan!"}), 400
    try:
        process = subprocess.Popen(
            ['python3', fpath],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=os.path.dirname(fpath)
        )
        running_bots[fpath] = process
        bot_logs[fpath] = [{"time": time.strftime("%H:%M:%S"), "msg": f"🚀 Menjalankan {os.path.basename(fpath)}..."}]
        t = threading.Thread(target=read_output, args=(fpath, process), daemon=True)
        t.start()
        return jsonify({"success": True, "pid": process.pid})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/bot/stop', methods=['POST'])
def stop_bot():
    data = request.get_json()
    fpath = safe_path(data.get('path', ''))
    if fpath not in running_bots:
        return jsonify({"error": "Bot tidak sedang berjalan"}), 400
    try:
        running_bots[fpath].kill()
        running_bots.pop(fpath, None)
        bot_logs.setdefault(fpath, []).append({"time": time.strftime("%H:%M:%S"), "msg": "🛑 Bot dihentikan."})
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/bot/status', methods=['GET'])
def bot_status():
    result = {}
    for fpath, proc in list(running_bots.items()):
        if proc.poll() is None:
            result[fpath] = "running"
        else:
            running_bots.pop(fpath, None)
    return jsonify({"running": result})

@app.route('/api/bot/logs', methods=['POST'])
def get_logs():
    data = request.get_json()
    fpath = safe_path(data.get('path', ''))
    return jsonify({"logs": bot_logs.get(fpath, [])})

# ── TERMINAL ─────────────────────────────────────────────────
@app.route('/api/terminal', methods=['POST'])
def terminal():
    data    = request.get_json()
    cmd     = data.get('cmd', '').strip()
    cwd_req = data.get('cwd', HOME)

    # Resolve cwd — fallback to HOME kalau tak valid
    cwd = cwd_req.replace('~', HOME)
    if not os.path.isdir(cwd):
        cwd = HOME

    # Blok arahan berbahaya
    BLOCKED = ['rm -rf /', 'mkfs', ':(){:|:&};:', 'dd if=']
    for b in BLOCKED:
        if b in cmd:
            return jsonify({"error": "Arahan ini disekat.", "cwd": cwd_req}), 403

    # Handle 'cd' manual sebab subprocess tak boleh tukar cwd parent
    if cmd.startswith('cd'):
        parts = cmd.split(None, 1)
        target = parts[1] if len(parts) > 1 else HOME
        target = target.replace('~', HOME)
        new_dir = os.path.realpath(os.path.join(cwd, target))
        if os.path.isdir(new_dir):
            # Return ~ format kalau dalam HOME
            display = new_dir.replace(HOME, '~') if new_dir.startswith(HOME) else new_dir
            return jsonify({"output": "", "cwd": display})
        else:
            return jsonify({"output": f"cd: {target}: No such file or directory", "cwd": cwd_req, "error": True})

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            timeout=15
        )
        output = result.stdout.decode('utf-8', errors='replace')
        err    = result.stderr.decode('utf-8', errors='replace')
        combined = (output + err).rstrip()
        return jsonify({
            "output": combined,
            "cwd": cwd_req,
            "error": result.returncode != 0
        })
    except subprocess.TimeoutExpired:
        return jsonify({"output": "Timeout: arahan ambil masa terlalu lama.", "cwd": cwd_req, "error": True})
    except Exception as e:
        return jsonify({"error": str(e), "cwd": cwd_req})

# ── MAIN ─────────────────────────────────────────────────────
if __name__ == '__main__':
    print("=" * 50)
    print("  🤖 Telegram Bot Panel")
    print(f"  Home: {HOME}")
    print("  URL : http://localhost:5000")
    print("  Ctrl+C untuk berhenti")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=False)
