import os
import numpy as np
from PIL import Image, UnidentifiedImageError
import matplotlib.pyplot as plt
from typing import Tuple, Union

# --- Standardized Helper Functions ---

def load_pil_image(file_path: str) -> Union[Image.Image, None]:
    """
    Loads an image from the specified file path using Pillow.

    Args:
        file_path: Path to the image file.

    Returns:
        A PIL Image object if successful, None otherwise.
    """
    try:
        img = Image.open(file_path)
        return img
    except FileNotFoundError:
        print(f"Error: Image file not found at '{file_path}'.")
    except UnidentifiedImageError:
        print(f"Error: Cannot identify image file. It may be corrupted or not a supported format: '{file_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred while loading image '{file_path}': {e}")
    return None

def pil_to_numpy_array(image: Image.Image) -> np.ndarray:
    """
    Converts a PIL Image object to a NumPy array.

    Args:
        image: The PIL Image object.

    Returns:
        A NumPy array representing the image.
    """
    return np.array(image)

def numpy_to_pil_image(array: np.ndarray) -> Image.Image:
    """
    Converts a NumPy array to a PIL Image object.
    Handles grayscale (2D array) and RGB (3D array).

    Args:
        array: The NumPy array, expected to be uint8.

    Returns:
        A PIL Image object.
    """
    if array.ndim == 2:
        return Image.fromarray(array.astype(np.uint8), 'L')  # Grayscale
    elif array.ndim == 3 and array.shape[2] == 3:
        return Image.fromarray(array.astype(np.uint8), 'RGB') # Color
    elif array.ndim == 3 and array.shape[2] == 4:
        return Image.fromarray(array.astype(np.uint8), 'RGBA') # Color with Alpha
    else:
        raise ValueError(f"Unsupported NumPy array shape for PIL conversion: {array.shape}")

def save_numpy_as_image(array: np.ndarray, file_path: str) -> None:
    """
    Saves a NumPy array as an image file using Pillow.

    Args:
        array: The NumPy array representing the image.
        file_path: Path to save the image file.
    """
    try:
        image = numpy_to_pil_image(array)
        image.save(file_path)
        print(f"Image saved successfully to '{file_path}'.")
    except Exception as e:
        print(f"Error saving image to '{file_path}': {e}")

def convert_pil_to_grayscale(image: Image.Image) -> Image.Image:
    """
    Converts a PIL Image to grayscale.

    Args:
        image: The input PIL Image object.

    Returns:
        A new PIL Image object in grayscale ('L' mode).
    """
    return image.convert('L')

# --- Core Reduction Function (Refactored) ---

def bilinear_interpolation(pixels: np.ndarray, new_size_wh: Tuple[int, int]) -> np.ndarray:
    """
    Reduces an image to new_size_wh using a manual pixel neighborhood averaging method.

    The function iterates through each pixel of the target (reduced) image. For each
    target pixel, it maps its coordinates back to the source (original) image.
    It then takes four pixels from the source image: the pixel at the mapped
    top-left coordinate, and its neighbors to the right, below, and diagonally
    bottom-right. These four source pixels are averaged to compute the value
    for the target pixel.

    When new_size_wh is exactly half the original dimensions (2x reduction),
    this method effectively averages 2x2 blocks of pixels from the original image.

    Note: The name 'bilinear_interpolation' is retained from the original script.
    However, this implementation is a specific form of neighborhood averaging.
    For true bilinear interpolation (which involves weighted averages based on
    sub-pixel distances), consider using established library functions, e.g.,
    `PIL.Image.Image.resize(new_size_wh, Image.Resampling.BILINEAR)`.

    Args:
        pixels: NumPy array representing the source image (H x W for grayscale,
                H x W x C for color). Expected dtype is uint8 or similar.
        new_size_wh: Tuple (new_width, new_height) for the output image.

    Returns:
        NumPy array of the reduced image, with dtype uint8.
    """
    original_height, original_width = pixels.shape[:2]
    
    is_color = pixels.ndim == 3
    if is_color:
        num_channels = pixels.shape[2]
    
    new_width, new_height = new_size_wh

    if new_width <= 0 or new_height <= 0:
        raise ValueError("New dimensions (width and height) must be positive.")

    # Initialize the output array for reduced pixels
    if is_color:
        reduced_pixels = np.zeros((new_height, new_width, num_channels), dtype=np.float32)
    else:
        reduced_pixels = np.zeros((new_height, new_width), dtype=np.float32)

    for r_new in range(new_height):  # Index for rows in the new image
        for c_new in range(new_width):   # Index for columns in the new image
            
            # Map new pixel's top-left corresponding coordinate in original image
            r_orig_tl = r_new * original_height // new_height
            c_orig_tl = c_new * original_width // new_width

            # Define the four source pixels (top-left, top-right, bottom-left, bottom-right of a 2x2-like region)
            # Ensure indices are within bounds of the original image
            r_orig_br = min(r_orig_tl + 1, original_height - 1)
            c_orig_br = min(c_orig_tl + 1, original_width - 1)

            if is_color:
                p_tl = pixels[r_orig_tl, c_orig_tl, :].astype(np.float32)
                p_tr = pixels[r_orig_tl, c_orig_br, :].astype(np.float32)
                p_bl = pixels[r_orig_br, c_orig_tl, :].astype(np.float32)
                p_br = pixels[r_orig_br, c_orig_br, :].astype(np.float32)
            else: # Grayscale
                p_tl = float(pixels[r_orig_tl, c_orig_tl])
                p_tr = float(pixels[r_orig_tl, c_orig_br])
                p_bl = float(pixels[r_orig_br, c_orig_tl])
                p_br = float(pixels[r_orig_br, c_orig_br])
            
            # Average the four points
            average_value = (p_tl + p_tr + p_bl + p_br) / 4.0
            reduced_pixels[r_new, c_new] = average_value
            
    return np.clip(reduced_pixels, 0, 255).astype(np.uint8)

# --- Plotting Function ---

def plot_reduction_comparison(
    original_array: np.ndarray,
    reduced_array: np.ndarray,
    title_original: str = "Original Image",
    title_reduced: str = "Reduced Image",
    output_path: Union[str, None] = None
) -> None:
    """
    Plots the original and reduced images side-by-side using Matplotlib.

    Args:
        original_array: NumPy array of the original image.
        reduced_array: NumPy array of the reduced image.
        title_original: Title for the original image plot.
        title_reduced: Title for the reduced image plot.
        output_path: If provided, saves the plot to this file path.
    """
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    
    # Determine cmap for grayscale or color
    cmap_orig = 'gray' if original_array.ndim == 2 else None
    cmap_reduced = 'gray' if reduced_array.ndim == 2 else None

    axes[0].imshow(original_array, cmap=cmap_orig, vmin=0, vmax=255 if cmap_orig else None)
    axes[0].set_title(f"{title_original}\\nShape: {original_array.shape}")
    axes[0].axis('off')

    axes[1].imshow(reduced_array, cmap=cmap_reduced, vmin=0, vmax=255 if cmap_reduced else None)
    axes[1].set_title(f"{title_reduced}\\nShape: {reduced_array.shape}")
    axes[1].axis('off')

    plt.tight_layout()
    
    if output_path:
        try:
            plt.savefig(output_path)
            print(f"Plot saved successfully to '{output_path}'.")
        except Exception as e:
            print(f"Error saving plot to '{output_path}': {e}")
    plt.show()

# --- Main Execution Block ---

if __name__ == '__main__':
    # Determine the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Input image details
    input_image_filename = "brat.jpeg"
    input_image_path = os.path.join(script_dir, input_image_filename)

    # Output directory details
    output_dir_name = "resultados_reducao_bilinear"
    output_dir_path = os.path.join(script_dir, output_dir_name)
    
    try:
        os.makedirs(output_dir_path, exist_ok=True)
        print(f"Output directory '{output_dir_path}' ensured.")
    except OSError as e:
        print(f"Error creating output directory '{output_dir_path}': {e}")
        # Optionally, exit if directory creation fails and is critical
        # exit(1)

    # 1. Load the image
    print(f"Loading image: '{input_image_path}'...")
    pil_image = load_pil_image(input_image_path)

    if pil_image:
        # 2. Convert to grayscale (as per original script's behavior)
        print("Converting image to grayscale...")
        pil_gray_image = convert_pil_to_grayscale(pil_image)
        original_numpy_gray = pil_to_numpy_array(pil_gray_image)
        print(f"Original grayscale image shape: {original_numpy_gray.shape}")

        # 3. Define new size (reducing by half)
        # PIL image.size is (width, height)
        new_width = pil_gray_image.size[0] // 2
        new_height = pil_gray_image.size[1] // 2
        target_size_wh: Tuple[int, int] = (new_width, new_height)
        print(f"Target reduced size (width, height): {target_size_wh}")

        # 4. Perform the reduction
        print("Performing image reduction...")
        reduced_numpy_gray = bilinear_interpolation(original_numpy_gray, target_size_wh)
        print(f"Reduced image shape: {reduced_numpy_gray.shape}")

        # 5. Save the reduced image
        output_image_filename = f"{os.path.splitext(input_image_filename)[0]}_reducao_bilinear.jpeg"
        output_image_path = os.path.join(output_dir_path, output_image_filename)
        save_numpy_as_image(reduced_numpy_gray, output_image_path)

        # 6. Plot and save comparison
        plot_filename = f"plot_{os.path.splitext(input_image_filename)[0]}_reduction_comparison.png"
        plot_output_path = os.path.join(output_dir_path, plot_filename)
        
        plot_reduction_comparison(
            original_numpy_gray,
            reduced_numpy_gray,
            title_original=f"Original Grayscale ({input_image_filename})",
            title_reduced=f"Reduced (Custom Method, Factor 0.5)",
            output_path=plot_output_path
        )
        print("Processing complete.")
    else:
        print(f"Could not load image '{input_image_path}'. Halting script.")
