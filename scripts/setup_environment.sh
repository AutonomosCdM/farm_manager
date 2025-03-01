#!/bin/bash

# Farm Manager Environment Setup Script

set -e  # Exit immediately if a command exits with a non-zero status

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}Python 3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

# Project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Virtual environment name
VENV_NAME="venv_farm_manager"

# Create virtual environment
echo -e "${GREEN}Creating virtual environment...${NC}"
python3 -m venv "${PROJECT_ROOT}/${VENV_NAME}"

# Activate virtual environment
source "${PROJECT_ROOT}/${VENV_NAME}/bin/activate"

# Upgrade pip
pip install --upgrade pip

# Install project dependencies
echo -e "${GREEN}Installing project dependencies...${NC}"
pip install -r "${PROJECT_ROOT}/requirements.txt"
pip install -e "${PROJECT_ROOT}"

# Create necessary data directories
echo -e "${GREEN}Creating data directories...${NC}"
mkdir -p "${PROJECT_ROOT}/data/resources"
mkdir -p "${PROJECT_ROOT}/data/knowledge_base"
mkdir -p "${PROJECT_ROOT}/data/backups"

# Set up initial configuration
echo -e "${GREEN}Setting up initial configuration...${NC}"
cp "${PROJECT_ROOT}/.env.example" "${PROJECT_ROOT}/.env"

# Run initial database setup
echo -e "${GREEN}Initializing database...${NC}"
python3 -m farm_manager.knowledge.base init

echo -e "${GREEN}Environment setup complete!${NC}"
echo -e "${YELLOW}Activate the virtual environment with:${NC}"
echo "source ${VENV_NAME}/bin/activate"
