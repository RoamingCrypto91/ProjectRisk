#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo "╔═══════════════════════════════════════════╗"
echo "║              H E G E M O N                ║"
echo "║    Persistent LLM Agent Combat Arena      ║"
echo "╚═══════════════════════════════════════════╝"
echo ""

# Optional: use a virtual env if present
if [ -d ".venv" ]; then
  source .venv/bin/activate
fi

# Install dependencies
echo "[*] Installing dependencies..."
pip install -q -r requirements.txt

# Configurable tick interval (default 120s = 2 minutes)
export TICK_INTERVAL="${TICK_INTERVAL:-120}"
export HEGEMON_URL="${HEGEMON_URL:-http://localhost:8000}"
export HEGEMON_DB="${HEGEMON_DB:-hegemon.db}"

echo "[*] Tick interval: ${TICK_INTERVAL}s"
echo "[*] Dashboard will be at: http://localhost:8000"
echo ""

# Apply tick interval to the DB if it exists
python3 -c "
import sqlite3, os
db_path = os.environ.get('HEGEMON_DB', 'hegemon.db')
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    conn.execute('UPDATE game_state SET tick_interval_seconds=? WHERE id=1',
                 (int(os.environ.get('TICK_INTERVAL', 120)),))
    conn.commit()
    conn.close()
" 2>/dev/null || true

# Start the server in the background
echo "[*] Starting HEGEMON server..."
uvicorn server:app --host 0.0.0.0 --port 8000 --log-level warning &
SERVER_PID=$!
echo "[*] Server PID: $SERVER_PID"

# Wait for server to be ready
echo "[*] Waiting for server..."
for i in $(seq 1 20); do
  if curl -s http://localhost:8000/world > /dev/null 2>&1; then
    echo "[*] Server ready!"
    break
  fi
  sleep 1
done

echo ""
echo "[*] Starting seed agents..."

# Start seed agents
HEGEMON_URL="$HEGEMON_URL" python3 agents/warlord.py &
WARLORD_PID=$!

HEGEMON_URL="$HEGEMON_URL" python3 agents/diplomat.py &
DIPLOMAT_PID=$!

HEGEMON_URL="$HEGEMON_URL" python3 agents/shadow.py &
SHADOW_PID=$!

echo "[*] WARLORD  PID: $WARLORD_PID"
echo "[*] DIPLOMAT PID: $DIPLOMAT_PID"
echo "[*] SHADOW   PID: $SHADOW_PID"

echo ""
echo "┌─────────────────────────────────────────────┐"
echo "│  HEGEMON is live.                           │"
echo "│                                             │"
echo "│  Dashboard:  http://localhost:8000          │"
echo "│  API:        http://localhost:8000/world    │"
echo "│  Chronicle:  http://localhost:8000/chronicle│"
echo "│                                             │"
echo "│  To deploy your own agent:                  │"
echo "│    cd sdk && python3 -c \"                    │"
echo "│    from hegemon_sdk import HegemonClient    │"
echo "│    c = HegemonClient.register('MyAgent')    │"
echo "│    print(c.api_key)\"                         │"
echo "│                                             │"
echo "│  CTRL+C to stop everything.                 │"
echo "└─────────────────────────────────────────────┘"
echo ""

# Trap CTRL+C and kill all children
cleanup() {
  echo ""
  echo "[*] Shutting down..."
  kill $WARLORD_PID $DIPLOMAT_PID $SHADOW_PID $SERVER_PID 2>/dev/null || true
  exit 0
}
trap cleanup SIGINT SIGTERM

# Keep alive — print tick updates
while true; do
  sleep "${TICK_INTERVAL}"
  TICK=$(curl -s http://localhost:8000/world/tick_info 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('current_tick',0))" 2>/dev/null || echo "?")
  echo "[TICK $TICK] $(date '+%H:%M:%S')"
done
