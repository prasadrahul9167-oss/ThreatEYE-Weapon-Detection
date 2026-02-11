#!/bin/bash

# ThreatEYE Setup Script
# This script automates the installation and setup process

echo "========================================"
echo "   ThreatEYE Setup Script v1.1.0"
echo "========================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 not found. Please install Python 3.11+${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python found: $(python3 --version)${NC}"

# Check Node.js
echo "Checking Node.js installation..."
if ! command -v node &> /dev/null; then
    echo -e "${RED}✗ Node.js not found. Please install Node.js 18+${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Node.js found: $(node --version)${NC}"

# Check Yarn
echo "Checking Yarn installation..."
if ! command -v yarn &> /dev/null; then
    echo -e "${YELLOW}! Yarn not found. Installing...${NC}"
    npm install -g yarn
fi
echo -e "${GREEN}✓ Yarn found: $(yarn --version)${NC}"

# Check MongoDB
echo "Checking MongoDB..."
if ! pgrep -x mongod > /dev/null; then
    echo -e "${YELLOW}! MongoDB not running. Please start MongoDB service.${NC}"
    echo "  Ubuntu: sudo systemctl start mongod"
    echo "  macOS: brew services start mongodb-community"
else
    echo -e "${GREEN}✓ MongoDB is running${NC}"
fi

echo ""
echo "========================================"
echo "   Installing Backend Dependencies"
echo "========================================"
echo ""

cd backend || exit

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${GREEN}✓ Backend dependencies installed${NC}"

# Setup environment file
if [ ! -f ".env" ]; then
    echo "Creating backend .env file..."
    cp .env.example .env
    echo -e "${YELLOW}! Please edit backend/.env with your settings${NC}"
fi

cd ..

echo ""
echo "========================================"
echo "   Installing Frontend Dependencies"
echo "========================================"
echo ""

cd frontend || exit

echo "Installing Node packages..."
yarn install

echo -e "${GREEN}✓ Frontend dependencies installed${NC}"

# Setup environment file
if [ ! -f ".env" ]; then
    echo "Creating frontend .env file..."
    cp .env.example .env
    echo -e "${YELLOW}! Please edit frontend/.env with your settings${NC}"
fi

cd ..

echo ""
echo "========================================"
echo "   Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env with your MongoDB URL"
echo "2. Edit frontend/.env with your backend URL"
echo ""
echo "To start the application:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  uvicorn server:app --host 0.0.0.0 --port 8001"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  yarn start"
echo ""
echo "Then open: http://localhost:3000"
echo ""
echo -e "${GREEN}Happy detecting! 🎯${NC}"
