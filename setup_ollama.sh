#!/bin/bash
# Ollama Setup Script for AI Metadata Fixing
# This script helps install and set up Ollama for use with the metadata fixer

echo "🤖 Ollama Setup for AI Metadata Fixing"
echo "======================================"

# Check if Ollama is already installed
if command -v ollama &> /dev/null; then
    echo "✅ Ollama is already installed"
    ollama --version
else
    echo "📥 Installing Ollama..."
    
    # Install Ollama (macOS/Linux)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Installing on macOS..."
        curl -fsSL https://ollama.ai/install.sh | sh
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "Installing on Linux..."
        curl -fsSL https://ollama.ai/install.sh | sh
    else
        echo "❌ Unsupported OS. Please install Ollama manually from https://ollama.ai"
        exit 1
    fi
fi

echo ""
echo "🚀 Starting Ollama service..."
ollama serve &
OLLAMA_PID=$!

# Wait a moment for service to start
sleep 3

echo ""
echo "📦 Installing recommended model (gpt-oss - optimized for reasoning tasks)..."
ollama pull gpt-oss

echo ""
echo "📦 Installing backup model (qwen2.5 - fast and efficient)..."
ollama pull qwen2.5:7b

echo ""
echo "🧪 Testing the setup..."
if curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "✅ Ollama is running successfully!"
    echo ""
    echo "🎵 You can now use AI metadata fixing with:"
    echo "   python spotdl/main.py --car-audio --fix-metadata"
    echo "   python spotdl/metadata_fixer.py <music_folder>"
    echo ""
    echo "📚 Available commands:"
    echo "   • Interactive mode: python spotdl/metadata_fixer.py --interactive <folder>"
    echo "   • Different model: python spotdl/metadata_fixer.py --model llama3.2 <folder>"
else
    echo "❌ Ollama service is not responding"
    echo "Try running 'ollama serve' manually"
fi

echo ""
echo "💡 Tips:"
echo "   • Keep the terminal with 'ollama serve' running while using AI features"
echo "   • You can install other models with: ollama pull <model_name>"
echo "   • Recommended models for metadata fixing:"
echo "     - gpt-oss (best reasoning, default)"
echo "     - qwen2.5:7b (fast, efficient)"
echo "     - deepseek-r1:7b (excellent reasoning)"
echo "     - llama3.1 (reliable fallback)"
