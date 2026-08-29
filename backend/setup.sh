#!/bin/bash

echo "🚀 Setting up Hook Page Builder Backend..."

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
cp .env.example .env

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Add your OpenAI API key to backend/.env"
echo "2. Run: source venv/bin/activate"
echo "3. Run: python app.py"
echo ""
