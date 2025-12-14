#!/usr/bin/env python3
"""
Basic usage examples for mandelbrot_fast
"""

from mandelbrot_fast import render_mandelbrot

# Example 1: Quick preview
print("Rendering 640x480 preview...")
img = render_mandelbrot(width=640, height=480, max_iter=1000)
img.save("mandelbrot_preview.png")

# Example 2: High-detail region
print("\nRendering zoomed region at 1080p...")
img = render_mandelbrot(
    width=1920,
    height=1080,
    max_iter=32768,
    x_min=-0.178,
    x_max=-0.148,
    y_min=-1.0409375,
    y_max=-1.0240625
)
img.save("mandelbrot_zoomed.png")

print("\nDone! Check the generated PNG files.")
