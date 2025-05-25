import os
import numpy as np
from PIL import Image, UnidentifiedImageError
import matplotlib.pyplot as plt
from typing import Union, Tuple

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

def save_pil_image(image: Image.Image, file_path: str) -> None:
    """
    Saves a PIL Image object to a file.

    Args:
        image: The PIL Image object to save.
        file_path: Path to save the image file.
    """
    try:
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

def downsample_nearest_neighbor(pixels: np.ndarray, factor: int = 2) -> np.ndarray:
    """
    Reduces the image size by an integer factor using the nearest neighbor method.
    This is achieved by selecting pixels at intervals defined by the factor.
    For example, a factor of 2 means every other pixel is selected.

    Args:
        pixels: NumPy array representing the image (H x W or H x W x C).
        factor: The integer factor by which to reduce the image dimensions.
                Must be greater than 0.

    Returns:
        NumPy array of the reduced image.

    Raises:
        ValueError: If the factor is not a positive integer.
    """
    if not isinstance(factor, int) or factor <= 0:
        raise ValueError("Reduction factor must be a positive integer.")
    
    if pixels.ndim == 2:  # Grayscale
        reduced_pixels = pixels[::factor, ::factor]
    elif pixels.ndim == 3:  # Color
        reduced_pixels = pixels[::factor, ::factor, :]
    else:
        raise ValueError(f"Unsupported NumPy array ndim for downsampling: {pixels.ndim}")
    return reduced_pixels

# --- Plotting Function ---

def plot_reduction_comparison(
    original_array: np.ndarray,
    reduced_array: np.ndarray,
    title_original: str = "Original Image",
    title_reduced: str = "Reduced Image (Nearest Neighbor)",
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
    input_image_filename = "brat.jpeg" # Original: "brat.jpeg"
    input_image_path = os.path.join(script_dir, input_image_filename)

    # Output directory details
    output_dir_name = "resultados_reducao_vizinho"
    output_dir_path = os.path.join(script_dir, output_dir_name)
    
    try:
        os.makedirs(output_dir_path, exist_ok=True)
        print(f"Output directory '{output_dir_path}' ensured.")
    except OSError as e:
        print(f"Error creating output directory '{output_dir_path}': {e}")
        # exit(1) # Optionally exit if critical

    # 1. Load the image
    print(f"Loading image: '{input_image_path}'...")
    pil_image_original = load_pil_image(input_image_path)

    if pil_image_original:
        # 2. Convert to grayscale (as per original script's behavior)
        print("Converting original image to grayscale...")
        pil_gray_image = convert_pil_to_grayscale(pil_image_original)
        numpy_gray_original = pil_to_numpy_array(pil_gray_image)
        print(f"Original grayscale image shape: {numpy_gray_original.shape}")

        # 3. Perform the reduction (default factor is 2, i.e., by half)
        reduction_factor = 2
        print(f"Performing nearest neighbor downsampling with factor {reduction_factor}...")
        try:
            numpy_gray_reduced = downsample_nearest_neighbor(numpy_gray_original, factor=reduction_factor)
            print(f"Reduced grayscale image shape: {numpy_gray_reduced.shape}")

            # 4. Convert reduced NumPy array back to PIL Image
            pil_image_reduced = numpy_to_pil_image(numpy_gray_reduced)

            # 5. Save the reduced image
            output_image_filename = f"{os.path.splitext(input_image_filename)[0]}_reducao_vizinho.jpeg"
            output_image_path = os.path.join(output_dir_path, output_image_filename)
            save_pil_image(pil_image_reduced, output_image_path)

            # 6. Plot and save comparison
            plot_filename = f"plot_{os.path.splitext(input_image_filename)[0]}_reducao_vizinho_comparison.png"
            plot_output_path = os.path.join(output_dir_path, plot_filename)
            
            plot_reduction_comparison(
                numpy_gray_original,
                numpy_gray_reduced,
                title_original=f"Original Grayscale ({input_image_filename})",
                title_reduced=f"Reduced (Nearest Neighbor, Factor 1/{reduction_factor})",
                output_path=plot_output_path
            )

        except ValueError as ve:
            print(f"Error during reduction: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred during processing: {e}")
        
        print("Processing complete.")
    else:
        print(f"Could not load image '{input_image_path}'. Halting script.")
