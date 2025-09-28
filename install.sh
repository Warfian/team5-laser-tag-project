#!/bin/bash

echo "Updating list of software packages..."
sudo apt update

echo "Installing prerequisites, python, and pip..."
sudo apt install -y build-essential cmake libx11-dev libgl1-mesa-dev libglu1-mesa-dev libxi-dev libxcursor-dev libxrandr-dev python3-dev
sudo apt install -y libxinerama-dev
sudo apt install -y python3-pip

echo "Using pip to install modules needed for program..."
pip install git+https://github.com/hoffstadt/DearPyGui.git
pip install psycopg2-binary
pip install pygame

echo "Install complete. Running program..."
make