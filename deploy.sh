#!/bin/bash

# Telegram Bot Deployment Script
# This script helps deploy the Telegram bot to your server

echo "🚀 Starting Telegram Bot Deployment..."

# Check if we're in the right directory
if [ ! -f "Dockerfile" ]; then
    echo "❌ Error: Dockerfile not found. Please run this script from the project root directory."
    exit 1
fi

# Check if docker-compose.yml exists
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: docker-compose.yml not found."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Creating from env.example..."
    if [ -f "env.example" ]; then
        cp env.example .env
        echo "📝 Please edit .env file with your configuration before running docker compose."
        exit 1
    else
        echo "❌ Error: Neither .env nor env.example found."
        exit 1
    fi
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs

# Build and start the containers
echo "🔨 Building and starting containers..."
docker compose up -d --build

# Check if containers are running
echo "🔍 Checking container status..."
docker compose ps

echo "✅ Deployment completed!"
echo "📋 To view logs: docker compose logs -f"
echo "🛑 To stop: docker compose down"
