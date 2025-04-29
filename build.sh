#!/bin/bash
echo "Installing Python packages..."
pip install -r requirements.txt

echo "Installing Firebase CLI..."
npm install -g firebase-tools
