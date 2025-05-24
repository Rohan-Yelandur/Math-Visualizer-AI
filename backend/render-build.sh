#!/usr/bin/env bash
# Install system dependencies for Manim
set -o errexit

# Update package lists
apt-get update -y

# Install FFmpeg
apt-get install -y ffmpeg

# Install minimal LaTeX distribution (much faster than full texlive)
apt-get install -y texlive-latex-base texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra

# Install Cairo and other Manim dependencies
apt-get install -y libcairo2-dev libpango1.0-dev ffmpeg

# Make the script executable
chmod +x build.sh