#!/data/data/com.termux/files/usr/bin/bash
echo "=== Setting up Mandelbrot Termux ==="

# Update Termux
pkg update -y && pkg upgrade -y

# Install core packages
pkg install -y python python-numpy clang git

# Install Python packages
pip install --upgrade pip
pip install numpy Pillow tqdm

# Test
echo "Testing installation..."
python -c "
import numpy as np
from PIL import Image
from tqdm import tqdm
print('✅ All dependencies installed!')
print(f'NumPy: {np.__version__}')
print(f'PIL: {Image.__version__}')
"

echo "Setup complete! Run: python mandelbrot_tiled.py"