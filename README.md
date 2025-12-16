# Fast Mandelbrot Set Renderer

A highly optimized Mandelbrot set renderer using NumPy and Numba for CPU parallelization, featuring real-time progress tracking.

## Features
- **Fast CPU rendering** using Numba's parallel JIT compilation
- **Real-time progress bar** with ETA estimation
- **Efficient memory usage** with NumPy vectorization
- **Adjustable parameters**: resolution, iterations, zoom region
- **Clean grayscale output** ready for post-processing
- **New Mandelbrot code** for use in termux or device which cannot support numba (still requires pillow(PIL), NumPy, tqdm, Python 3.x

## Installation

```bash
git clone https://github.com/icannotcodeijuststartmynewaccount/fast-mandelbrot.git
cd fast-mandelbrot
pip install -r requirements.txt
