"""
Tile-Based Mandelbrot Renderer for Termux
Memory-efficient with progress tracking
"""
import numpy as np
from PIL import Image
import time
import os
from tqdm import tqdm


def mandelbrot_tile(c_real, c_imag, max_iter):
    """
    Process a single tile (optimized for small arrays).
    """
    height, width = c_real.shape
    divtime = np.zeros((height, width), dtype=np.int32)
    
    # Local variables for speed
    threshold = 4.0
    
    for i in range(height):
        for j in range(width):
            cr = c_real[i, j]
            ci = c_imag[i, j]
            zr = zi = 0.0
            
            # Optimized escape loop
            for k in range(max_iter):
                zr2 = zr * zr
                zi2 = zi * zi
                if zr2 + zi2 > threshold:
                    divtime[i, j] = k
                    break
                zi = 2.0 * zr * zi + ci
                zr = zr2 - zi2 + cr
            else:
                divtime[i, j] = max_iter - 1
    
    return divtime


def render_mandelbrot_tiled(width=1280, height=720, max_iter=8192,
                           x_min=-0.178, x_max=-0.148,
                           y_min=-1.0409375, y_max=-1.0240625,
                           tile_size=256):
    """
    Render using tiles to manage memory on Termux.
    """
    print(f"Rendering {width}x{height} with {max_iter} iterations...")
    print(f"Tile size: {tile_size}x{tile_size}")
    
    # Pre-calculate scales
    x_scale = (x_max - x_min) / width
    y_scale = (y_max - y_min) / height
    
    # Create output array
    result = np.zeros((height, width), dtype=np.int32)
    
    # Calculate tile grid
    tiles_x = (width + tile_size - 1) // tile_size
    tiles_y = (height + tile_size - 1) // tile_size
    total_tiles = tiles_x * tiles_y
    
    print(f"Processing {total_tiles} tiles...")
    
    # Progress bar
    pbar = tqdm(total=total_tiles, desc="Tiles", unit="tile")
    
    start_time = time.time()
    
    # Process each tile
    for ty in range(tiles_y):
        for tx in range(tiles_x):
            # Tile coordinates
            x_start = tx * tile_size
            y_start = ty * tile_size
            x_end = min(x_start + tile_size, width)
            y_end = min(y_start + tile_size, height)
            tile_width = x_end - x_start
            tile_height = y_end - y_start
            
            # Generate coordinates for this tile
            x_indices = np.arange(x_start, x_end)
            y_indices = np.arange(y_start, y_end)
            
            X_tile, Y_tile = np.meshgrid(
                x_min + x_indices * x_scale,
                y_min + y_indices * y_scale
            )
            
            # Render tile
            tile_result = mandelbrot_tile(X_tile, Y_tile, max_iter)
            
            # Place in main result
            result[y_start:y_end, x_start:x_end] = tile_result
            
            # Update progress
            pbar.update(1)
    
    pbar.close()
    render_time = time.time() - start_time
    
    # Apply coloring
    mandelbrot_set = np.log(result + 1)
    mandelbrot_set = (mandelbrot_set / np.max(mandelbrot_set)) * 255
    mandelbrot_set = np.uint8(mandelbrot_set)
    
    # Create image
    img = Image.fromarray(mandelbrot_set, mode='L')
    
    # Performance stats
    megapixels = (width * height) / 1e6
    pixels_per_sec = megapixels / render_time if render_time > 0 else 0
    
    print(f"\n{'='*60}")
    print(f"RENDER COMPLETE!")
    print(f"Resolution: {width}x{height}")
    print(f"Iterations: {max_iter}")
    print(f"Tiles: {tiles_x}x{tiles_y} ({tile_size}x{tile_size})")
    print(f"Render time: {render_time:.2f} seconds")
    print(f"Speed: {pixels_per_sec:.2f} megapixels/sec")
    print(f"{'='*60}")
    
    return img, render_time


def quick_test_tiled():
    """Quick test with tiled rendering."""
    print("Running tiled quick test...")
    
    img, time_taken = render_mandelbrot_tiled(
        width=640,
        height=480,
        max_iter=256,
        x_min=-2.0,
        x_max=0.5,
        y_min=-1.25,
        y_max=1.25,
        tile_size=128
    )
    
    print(f"Tiled test completed in {time_taken:.2f} seconds")
    
    # Save
    downloads_path = os.path.join(os.path.expanduser('~'), 'mandelbrot_tiled.png')
    img.save(downloads_path)
    print(f"Saved to: {downloads_path}")
    
    # ASCII preview
    print("\nASCII Preview (40x20):")
    data = np.array(img.resize((40, 20), Image.Resampling.LANCZOS))
    chars = " .:-=+*#%@"
    for row in data:
        line = "".join(chars[pixel // 26] for pixel in row)
        print(line)
    
    return img


# Run the tiled version
if __name__ == "__main__":
    # First, run a quick test to verify it works
    quick_test_tiled()
    
    # If that works, try the full render
    print("\n" + "="*60)
    print("STARTING TILED FULL RENDER")
    print("="*60)
    
    img, render_time = render_mandelbrot_tiled(
        width=1280,
        height=720,
        max_iter=8192,
        x_min=-0.178,
        x_max=-0.148,
        y_min=-1.0409375,
        y_max=-1.0240625,
        tile_size=128  # Smaller tiles for less memory
    )
    
    # Save
    downloads_path = os.path.join(os.path.expanduser('~'), 'mandelbrot_final_tiled.png')
    img.save(downloads_path)
    print(f"\nImage saved to: {downloads_path}")