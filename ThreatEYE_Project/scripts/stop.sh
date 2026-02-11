#!/bin/bash

# ThreatEYE Stop Script
# Stops all ThreatEYE processes

echo "Stopping ThreatEYE Weapon Detection System..."

# Kill backend
echo "Stopping backend..."
pkill -f "uvicorn server:app"

# Kill frontend
echo "Stopping frontend..."
pkill -f "react-scripts start"
pkill -f "node.*react-scripts"

sleep 2

echo ""
echo "ThreatEYE stopped successfully."
echo ""
