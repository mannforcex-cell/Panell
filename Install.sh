#!/data/data/com.termux/files/usr/bin/bash
# ─────────────────────────────────────────────────────────────
#  TeleBot Panel v2.1 — Install Script (Pertama Kali)
#  Jalankan: bash install.sh
# ─────────────────────────────────────────────────────────────

CYAN='\033[0;96m'
GREEN='\033[0;92m'
YELLOW='\033[0;93m'
RED='\033[0;91m'
DIM='\033[2m'
BOLD='\033[1m'
RESET='\033[0m'

clear

echo ""
echo -e "${CYAN}${BOLD}"
echo "  ╔══════════════════════════════════════════╗"
echo "  ║     TELEBOT PANEL v2.1 — INSTALLER       ║"
echo "  ║     Termux Bot Manager Setup              ║"
echo "  ╚══════════════════════════════════════════╝"
echo -e "${RESET}"
echo ""

step() { echo -e "  ${CYAN}[${1}/${TOTAL}]${RESET} ${2}"; }
ok()   { echo -e "       ${GREEN}✓ ${1}${RESET}"; }
warn() { echo -e "       ${YELLOW}⚠ ${1}${RESET}"; }
fail() { echo -e "       ${RED}✗ ${1}${RESET}"; exit 1; }

TOTAL=6

# ── Step 1: Update pakej ──────────────────────────────────────
step 1 "Update Termux pakej..."
pkg update -y -q 2>/dev/null || warn "Update gagal, teruskan..."
ok "Pakej dikemaskini"

# ── Step 2: Python ────────────────────────────────────────────
step 2 "Pasang Python 3..."
if command -v python3 &>/dev/null; then
  ok "Python3 sudah ada ($(python3 --version 2>&1 | awk '{print $2}'))"
else
  pkg install python -y -q || fail "Gagal pasang Python3"
  ok "Python3 berjaya dipasang"
fi

# ── Step 3: pip packages ──────────────────────────────────────
step 3 "Pasang Flask + Flask-CORS..."
pip install flask flask-cors --quiet --upgrade || fail "Gagal pasang Flask"
ok "Flask & Flask-CORS berjaya dipasang"

# ── Step 4: Node.js (optional) ───────────────────────────────
step 4 "Node.js (optional untuk .js bots)..."
if command -v node &>/dev/null; then
  ok "Node.js sudah ada ($(node --version))"
else
  echo -ne "       Pasang Node.js? (y/N): "
  read -r ans
  if [[ "$ans" == "y" || "$ans" == "Y" ]]; then
    pkg install nodejs -y -q && ok "Node.js berjaya dipasang" || warn "Gagal pasang Node.js"
  else
    warn "Langkau Node.js — hanya fail .py boleh dijalankan"
  fi
fi

# ── Step 5: Telebot library ───────────────────────────────────
step 5 "Pasang pyTelegramBotAPI (telebot)..."
if python3 -c "import telebot" &>/dev/null; then
  ok "telebot sudah ada"
else
  pip install pyTelegramBotAPI --quiet || warn "Gagal pasang telebot — pasang manual: pip install pyTelegramBotAPI"
  ok "pyTelegramBotAPI berjaya dipasang"
fi

# ── Step 6: chmod start.sh ───────────────────────────────────
step 6 "Set permission fail..."
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
chmod +x "${DIR}/start.sh" 2>/dev/null && ok "start.sh boleh dijalankan"
chmod +x "${DIR}/install.sh" 2>/dev/null

echo ""
echo -e "  ${DIM}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo ""
echo -e "  ${GREEN}${BOLD}✅  PEMASANGAN SELESAI!${RESET}"
echo ""
echo -e "  ${CYAN}Cara jalankan panel:${RESET}"
echo -e "  ${DIM}  bash start.sh${RESET}"
echo -e "  ${DIM}  atau${RESET}"
echo -e "  ${DIM}  python3 server.py${RESET}"
echo ""
echo -e "  ${CYAN}Kemudian buka browser:${RESET}"
echo -e "  ${DIM}  http://localhost:5000${RESET}"
echo ""
echo -e "  ${DIM}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo ""
p
