#!/bin/bash

# ThreatEYE Test Script
# Runs tests for backend and frontend

echo "========================================"
echo "   Running ThreatEYE Tests"
echo "========================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Test backend
echo "Testing Backend..."
cd backend || exit

# Check if backend is running
if curl -s http://localhost:8001/api/ > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Backend is running${NC}"
else
    echo -e "${RED}✗ Backend is not running${NC}"
    echo "Please start backend: uvicorn server:app --host 0.0.0.0 --port 8001"
    exit 1
fi

# Test API endpoints
echo "Testing API endpoints..."

echo "  Testing /api/ ..."
if curl -s http://localhost:8001/api/ | grep -q "Weapon Detection"; then
    echo -e "    ${GREEN}✓ Passed${NC}"
else
    echo -e "    ${RED}✗ Failed${NC}"
fi

echo "  Testing /api/stats ..."
if curl -s http://localhost:8001/api/stats | grep -q "total_detections"; then
    echo -e "    ${GREEN}✓ Passed${NC}"
else
    echo -e "    ${RED}✗ Failed${NC}"
fi

cd ..

# Test frontend
echo ""
echo "Testing Frontend..."
cd frontend || exit

if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Frontend is running${NC}"
else
    echo -e "${RED}✗ Frontend is not running${NC}"
    echo "Please start frontend: yarn start"
fi

cd ..

echo ""
echo "========================================"
echo "   Tests Complete"
echo "========================================"
echo ""
