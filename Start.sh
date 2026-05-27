#!/data/data/com.termux/files/usr/bin/bash
# ─────────────────────────────────────────────────────────────
#  TeleBot Panel v2.1 — Start Script
#  Jalankan: bash start.sh
# ─────────────────────────────────────────────────────────────

CYAN='\033[0;96m'
GREEN='\033[0;92m'
YELLOW='\033[0;93m'
RED='\033[0;91m'
DIM='\033[2m'
BOLD='\033[1m'
RESET='\033[0m'

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT=5000

clear

echo ""
echo -e "${CYAN}${BOLD}"
echo "  ████████╗███████╗██╗     ███████╗██████╗  ██████╗ ████████╗"
echo "     ██╔══╝██╔════╝██║     ██╔════╝██╔══██╗██╔═══██╗╚══██╔══╝"
echo "     ██║   █████╗  ██║     █████╗  ██████╔╝██║   ██║   ██║   "
echo "     ██║   ██╔══╝  ██║     ██╔══╝  ██╔══██╗██║   ██║   ██║   "
echo "     ██║   ███████╗███████╗███████╗██████╔╝╚██████╔╝   ██║   "
echo "     ╚═╝   ╚══════╝╚══════╝╚══════╝╚═════╝  ╚═════╝    ╚═╝   "
echo -e "${RESET}"
echo -e "  ${DIM}${CYAN}TeleBot Panel v2.1 · Termux Bot Manager${RESET}"
echo ""
echo -e "  ${DIM}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo ""

# ── Semak Python ──────────────────────────────────────────────
echo -ne "  ${DIM}[CHECK]${RESET} Python3 ... "
if ! command -v python3 &>/dev/null; then
  echo -e "${RED}TIDAK JUMPA${RESET}"
  echo -e "  ${YELLOW}Pasang dengan: pkg install python${RESET}"
  exit 1
fi
PY_VER=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}OK${RESET} ${DIM}(${PY_VER})${RESET}"

# ── Semak pip packages ────────────────────────────────────────
echo -ne "  ${DIM}[CHECK]${RESET} Flask    ... "
if python3 -c "import flask" &>/dev/null; then
  echo -e "${GREEN}OK${RESET}"
else
  echo -e "${YELLOW}MEMASANG...${RESET}"
  pip install flask flask-cors -q
fi

echo -ne "  ${DIM}[CHECK]${RESET} Flask-CORS ... "
if python3 -c "import flask_cors" &>/dev/null; then
  echo -e "${GREEN}OK${RESET}"
else
  echo -e "${YELLOW}MEMASANG...${RESET}"
  pip install flask-cors -q
fi

# ── Semak port ────────────────────────────────────────────────
echo -ne "  ${DIM}[CHECK]${RESET} Port ${PORT} ... "
if lsof -i :${PORT} &>/dev/null 2>&1; then
  echo -e "${RED}SUDAH DIGUNAKAN${RESET}"
  echo -e "  ${YELLOW}Hentikan proses lain atau ubah PORT dalam server.py${RESET}"
  echo ""
  echo -ne "  Teruskan juga? (y/N): "
  read -r ans
  [[ "$ans" != "y" && "$ans" != "Y" ]] && exit 1
else
  echo -e "${GREEN}BEBAS${RESET}"
fi

# ── Semak server.py ───────────────────────────────────────────
if [ ! -f "${DIR}/server.py" ]; then
  echo -e "  ${RED}[ERROR] server.py tidak dijumpai di ${DIR}${RESET}"
  exit 1
fi
if [ ! -f "${DIR}/index.html" ]; then
  echo -e "  ${YELLOW}[WARN] index.html tidak dijumpai — panel UI tidak akan muncul${RESET}"
fi

echo ""
echo -e "  ${DIM}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo ""
echo -e "  ${GREEN}${BOLD}PANEL SEDANG DIMUATKAN...${RESET}"
echo ""
echo -e "  ${CYAN}🌐 URL   : http://localhost:${PORT}${RESET}"
echo -e "  ${DIM}📁 Dir   : ${DIR}${RESET}"
echo -e "  ${DIM}🛑 Stop  : Tekan Ctrl+C${RESET}"
echo ""
echo -e "  ${DIM}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo ""

# ── Jalankan server ───────────────────────────────────────────
cd "${DIR}" && python3 server.py
