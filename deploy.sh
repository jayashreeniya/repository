#!/bin/bash

# Niya Sales Agent - Deployment Script
# This script automates the setup and deployment process

set -e  # Exit on any error

echo "🚀 Niya Sales Agent - Deployment Script"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

print_status "Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not installed. Please install pip."
    exit 1
fi

print_status "pip3 found: $(pip3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
print_status "Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Creating from template..."
    if [ -f "env_template.txt" ]; then
        cp env_template.txt .env
        print_status ".env file created from template"
        print_warning "Please edit .env file with your actual API keys"
    else
        print_error "env_template.txt not found. Please create .env file manually."
        exit 1
    fi
else
    print_status ".env file found"
fi

# Check if Gmail service account file exists
if [ ! -f "gmail-service.json" ]; then
    print_warning "gmail-service.json not found"
    print_warning "Please download your Gmail service account JSON file and place it in the project directory"
fi

# Run setup test
print_status "Running setup tests..."
python test_setup.py

# Check if Docker is available
if command -v docker &> /dev/null; then
    print_status "Docker found. You can also deploy using Docker:"
    echo "  docker-compose up -d"
else
    print_warning "Docker not found. You can install Docker for containerized deployment."
fi

echo ""
echo "🎉 Deployment completed!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Add your gmail-service.json file"
echo "3. Run: python niya_agent.py"
echo ""
echo "For testing: python test_setup.py"
echo "For help: python niya_agent.py --help" 