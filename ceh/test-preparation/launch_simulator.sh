#!/usr/bin/env bash
# ==============================================================================
# CEH v13 (312-50) Web Exam Simulator Launcher
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_FILE="$SCRIPT_DIR/data/exam_data.js"
HTML_FILE="$SCRIPT_DIR/exam-simulator.html"

echo "================================================================="
echo "   🛡️ EC-Council CEH v13 (312-50) Mock Examination Simulator     "
echo "================================================================="

# Check if data file exists; if not, compile it
if [ ! -f "$DATA_FILE" ]; then
    echo "[*] Compiling question bank from comprehensive master notes..."
    python3 "$SCRIPT_DIR/scripts/compile_exam_db.py"
fi

echo "[+] Exam simulator ready: $HTML_FILE"
echo ""
echo "Select Launch Mode:"
echo "  1) Open directly in default web browser (file://)"
echo "  2) Launch local HTTP server (http://localhost:8080/exam-simulator.html)"
echo "  3) Exit"
echo ""

read -rp "Enter choice [1-3] (Default: 1): " choice
choice="${choice:-1}"

case "$choice" in
    1)
        echo "[+] Opening simulator in browser..."
        if command -v xdg-open &>/dev/null; then
            xdg-open "$HTML_FILE" &>/dev/null &
        elif command -v sensible-browser &>/dev/null; then
            sensible-browser "$HTML_FILE" &>/dev/null &
        elif command -v google-chrome &>/dev/null; then
            google-chrome "$HTML_FILE" &>/dev/null &
        elif command -v firefox &>/dev/null; then
            firefox "$HTML_FILE" &>/dev/null &
        else
            echo "[!] No default browser detected. Please open this path manually:"
            echo "    file://$HTML_FILE"
        fi
        ;;
    2)
        PORT=8080
        echo "[+] Starting local HTTP server on port $PORT..."
        echo "👉 Open your browser at: http://localhost:$PORT/exam-simulator.html"
        echo "Press Ctrl+C to terminate the server when finished."
        cd "$SCRIPT_DIR" && python3 -m http.server "$PORT"
        ;;
    3)
        echo "Exiting."
        exit 0
        ;;
    *)
        echo "[!] Invalid choice. Opening in default browser..."
        xdg-open "$HTML_FILE" &>/dev/null &
        ;;
esac
