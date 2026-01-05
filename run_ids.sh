#!/bin/bash

echo "🚀 Starting SecureNet Hybrid AI IDS..."

# Check for sudo
if [ "$EUID" -ne 0 ]
  then echo "❌ Please run as root (sudo ./run_ids.sh)"
  exit
fi

# Trap Ctrl+C to kill child processes
trap "kill 0" EXIT

# Start IDS Engine in background
echo "📡 Starting Detection Engine (realtime_ids.py)..."
python3 realtime_ids.py &

# Start Dummy HTTP Server (Victim)
echo "🌐 Starting Victim Web Server on Port 8080..."
python3 dummy_server.py &

# Wait a moment for models to load
sleep 3

# Start Dashboard
# Start Dashboard
echo "📊 Starting Dashboard (dashboard.py)..."
if [ -n "$SUDO_USER" ]; then
    # Run as original user to prevent permission/MIME errors with static assets
    sudo -u $SUDO_USER streamlit run dashboard.py &
else
    streamlit run dashboard.py &
fi

# Wait
wait
