#!/bin/bash
echo "Installing Python packages..."
pip install -r requirements.txt

echo "Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
apt-get install -y nodejs

echo "Installing Firebase CLI..."
npm install -g firebase-tools
