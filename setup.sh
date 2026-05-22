#!/bin/bash
echo "=== AI Lead Hunter Setup ==="

# Create venv if not exists
if [ ! -d "venv" ]; then
    echo "→ Creating virtual environment..."
    python3 -m venv venv
fi

# Activate
source venv/bin/activate

# Install deps
echo "→ Installing dependencies..."
pip install -r requirements.txt -q

# Install Playwright Chromium
echo "→ Installing Playwright Chromium..."
playwright install chromium

# Copy .env if not exists
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "→ Created .env (edit if needed)"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Run: streamlit run app.py"
