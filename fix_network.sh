#!/bin/bash
echo "🚨 STARTING EMERGENCY NETWORK FIX..."

# 1. Kill old processes strongly
echo "💀 Killing all old Python/Streamlit processes..."
sudo pkill -9 -f python3
sudo pkill -9 -f streamlit
sudo pkill -9 -f run_ids.sh

# 2. Check for port 8080 users
echo "🔍 Checking port 8080..."
sudo lsof -i :8080 | awk 'NR!=1 {print $2}' | xargs sudo kill -9 2>/dev/null

# 3. Disable macOS Firewall (The most common blocker)
echo "🔥 Disabling macOS Firewall (Temporary for Demo)..."
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate off

# 4. Success Message
echo "✅ CLEANUP COMPLETE."
echo "   - Firewall should be OFF."
echo "   - Port 8080 should be FREE."
echo ""
echo "👉 NOW RUN: sudo ./run_ids.sh"
