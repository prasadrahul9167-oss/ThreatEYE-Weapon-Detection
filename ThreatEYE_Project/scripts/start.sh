#!/bin/bash

# ThreatEYE Start Script
# Starts both backend and frontend in separate processes

echo "Starting ThreatEYE Weapon Detection System..."

# Kill any existing processes
echo "Checking for existing processes..."
pkill -f "uvicorn server:app"
pkill -f "react-scripts start"

sleep 2

# Start backend
echo "Starting backend..."
cd backend || exit
source venv/bin/activate 2>/dev/null || true
uvicorn server:app --host 0.0.0.0 --port 8001 > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend started (PID: $BACKEND_PID)"

cd ..

# Wait for backend to be ready
echo "Waiting for backend to start..."
sleep 5

# Start frontend
echo "Starting frontend..."
cd frontend || exit
yarn start > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend started (PID: $FRONTEND_PID)"

cd ..

echo ""
echo "========================================"
echo "   ThreatEYE is now running!"
echo "========================================"
echo ""
echo "Backend:  http://localhost:8001"
echo "Frontend: http://localhost:3000"
echo ""
echo "Backend PID:  $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Logs:"
echo "  Backend:  tail -f logs/backend.log"
echo "  Frontend: tail -f logs/frontend.log"
echo ""
echo "To stop:"
echo "  kill $BACKEND_PID $FRONTEND_PID"
echo "  or run: ./scripts/stop.sh"
echo ""
