import os
import numpy as np
from PIL import Image, UnidentifiedImageError
import matplotlib.pyplot as plt
from typing import Tuple, Union, Dict

# --- Funções Auxiliares Padronizadas (Reutilizadas de gradiente.py) ---

def load_pil_image(file_path: str) -> Union[Image.Image, None]:
    """
    Carrega uma imagem a partir do caminho do arquivo usando Pillow.
    """
    try:
        img = Image.open(file_path)
        return img
    except FileNotFoundError:
        print(f"Erro: Arquivo de imagem não encontrado em '{file_path}'.")
    except UnidentifiedImageError:
        print(f"Erro: Não foi possível identificar o arquivo de imagem: '{file_path}'.")
    except Exception as e:
        print(f"Um erro inesperado ocorreu ao carregar a imagem '{file_path}': {e}")
    return None

def pil_to_numpy_array(image: Image.Image, dtype: type = np.uint8) -> np.ndarray:
    """
    Converte uma imagem PIL para um array NumPy.
    """
    return np.array(image, dtype=dtype)

def numpy_to_pil_image(array: np.ndarray) -> Image.Image:
    """
    Converte um array NumPy para uma imagem PIL.
    """
    if array.ndim == 2:
        return Image.fromarray(array.astype(np.uint8), 'L')
    elif array.ndim == 3 and array.shape[2] == 3:
        return Image.fromarray(array.astype(np.uint8), 'RGB')
    elif array.ndim == 3 and array.shape[2] == 4:
        return Image.fromarray(array.astype(np.uint8), 'RGBA')
    else:
        raise ValueError(f"Formato de array NumPy não suportado: {array.shape}")

def save_numpy_as_image(array: np.ndarray, file_path: str) -> None:
    """
    Salva um array NumPy como um arquivo de imagem.
    """
    try:
        image = numpy_to_pil_image(array)
        image.save(file_path)
        print(f"Imagem salva com sucesso em '{file_path}'.")
    except Exception as e:
        print(f"Erro ao salvar imagem em '{file_path}': {e}")

def convert_pil_to_grayscale_numpy(image: Image.Image) -> np.ndarray:
    """
    Converte uma imagem PIL para um array NumPy em escala de cinza.
    """
    if image.mode == 'L':
        return pil_to_numpy_array(image)
    return pil_to_numpy_array(image.convert('L'))

def apply_convolution(image_array: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """
    Aplica uma convolução 2D a uma imagem.
    """
    kernel_height, kernel_width = kernel.shape
    if kernel_height % 2 == 0 or kernel_width % 2 == 0:
        raise ValueError("O kernel deve ter dimensões ímpares.")
    pad_h, pad_w = kernel_height // 2, kernel_width // 2
    padded_image = np.pad(image_array, ((pad_h, pad_h), (pad_w, pad_w)), mode='edge')
    output_image = np.zeros_like(image_array, dtype=np.float32)
    image_height, image_width = image_array.shape
    for r in range(image_height):
        for c in range(image_width):
            region = padded_image[r : r + kernel_height, c : c + kernel_width]
            output_image[r, c] = np.sum(region * kernel)
    return output_image

def normalize_to_uint8(array: np.ndarray) -> np.ndarray:
    """
    Normaliza um array NumPy para o intervalo 0-255 e converte para uint8.
    """
    min_val, max_val = np.min(array), np.max(array)
    if max_val == min_val:
        return np.full_like(array, 128 if -1e-6 < min_val < 1e-6 else np.clip(min_val,0,255) , dtype=np.uint8)
    normalized = 255 * (array - min_val) / (max_val - min_val)
    return normalized.astype(np.uint8)

# --- Funções Principais do Filtro Laplaciano ---

def laplacian_filter_manual(image_gray_numpy: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """
    Aplica um filtro Laplaciano a uma imagem em escala de cinza usando um kernel específico.

    Args:
        image_gray_numpy: Array NumPy 2D representando a imagem em escala de cinza.
        kernel: Array NumPy 2D representando o kernel Laplaciano.

    Returns:
        Array NumPy 2D da imagem após a aplicação do filtro Laplaciano.
        O resultado é float32 e pode precisar ser normalizado para visualização.
    """
    if image_gray_numpy.ndim != 2:
        raise ValueError("A imagem de entrada para o filtro Laplaciano deve ser 2D (escala de cinza).")
    if kernel.ndim != 2 or kernel.shape[0] % 2 == 0 or kernel.shape[1] % 2 == 0:
        raise ValueError("O kernel Laplaciano deve ser 2D e ter dimensões ímpares.")
        
    return apply_convolution(image_gray_numpy.astype(np.float32), kernel)

# --- Função de Plotagem ---

def plot_laplacian_results(
    original_gray_numpy: np.ndarray,
    filtered_images_dict: Dict[str, np.ndarray],
    main_title: str = "Resultados do Filtro Laplaciano",
    output_path: Union[str, None] = None
) -> None:
    """
    Plota a imagem original em cinza e os resultados de diferentes filtros Laplacianos.

    Args:
        original_gray_numpy: Imagem original em escala de cinza (NumPy array).
        filtered_images_dict: Dicionário onde as chaves são nomes dos filtros (ex: "Máscara 1")
                              e os valores são os arrays NumPy das imagens filtradas.
        main_title: Título principal para o plot.
        output_path: Caminho opcional para salvar o plot.
    """
    num_filters = len(filtered_images_dict)
    num_plots = num_filters + 1 # +1 para a imagem original
    
    # Ajusta o layout de subplots dinamicamente
    # Tenta fazer uma grade o mais quadrada possível
    cols = int(np.ceil(np.sqrt(num_plots)))
    rows = int(np.ceil(num_plots / cols))
    
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 5, rows * 4))
    fig.suptitle(main_title, fontsize=16)
    axes = axes.flatten() # Facilita a iteração

    # Plot da imagem original
    axes[0].imshow(original_gray_numpy, cmap='gray', vmin=0, vmax=255)
    axes[0].set_title(f"Original em Cinza\nShape: {original_gray_numpy.shape}")
    axes[0].axis('off')

    # Plot das imagens filtradas
    idx = 1
    for filter_name, filtered_array in filtered_images_dict.items():
        if idx < len(axes):
            vis_filtered = normalize_to_uint8(filtered_array)
            axes[idx].imshow(vis_filtered, cmap='gray', vmin=0, vmax=255)
            axes[idx].set_title(f"{filter_name}\nShape: {vis_filtered.shape}")
            axes[idx].axis('off')
            idx += 1
            
    # Desliga eixos não utilizados
    for i in range(idx, len(axes)):
        axes[i].axis('off')

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    if output_path:
        try:
            plt.savefig(output_path)
            print(f"Plot salvo com sucesso em '{output_path}'.")
        except Exception as e:
            print(f"Erro ao salvar o plot em '{output_path}': {e}")
    plt.show()

# --- Bloco de Execução Principal ---

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    input_image_filename = "centavos.jpeg"  # Exemplo, pode ser alterado
    input_image_path = os.path.join(script_dir, input_image_filename)

    output_dir_name = "resultados_laplaciano"
    output_dir_path = os.path.join(script_dir, output_dir_name)

    try:
        os.makedirs(output_dir_path, exist_ok=True)
        print(f"Diretório de saída '{output_dir_path}' assegurado.")
    except OSError as e:
        print(f"Erro ao criar diretório de saída '{output_dir_path}': {e}")
        # exit(1)

    print(f"Carregando imagem: '{input_image_path}'...")
    pil_image_original = load_pil_image(input_image_path)

    if pil_image_original:
        print("Convertendo imagem para array NumPy em escala de cinza...")
        numpy_image_gray = convert_pil_to_grayscale_numpy(pil_image_original)
        
        original_gray_filename = f"{os.path.splitext(input_image_filename)[0]}_gray_numpy.jpeg"
        original_gray_output_path = os.path.join(output_dir_path, original_gray_filename)
        save_numpy_as_image(numpy_image_gray, original_gray_output_path)

        # Definição dos kernels Laplacianos
        kernels_laplacianos = {
            "Máscara Laplaciana 1 (Centro -4)": np.array([[ 0,  1,  0],
                                                          [ 1, -4,  1],
                                                          [ 0,  1,  0]], dtype=np.float32),
            "Máscara Laplaciana 2 (Centro -8)": np.array([[ 1,  1,  1],
                                                          [ 1, -8,  1],
                                                          [ 1,  1,  1]], dtype=np.float32),
            "Máscara Laplaciana 3 (Centro 4)":  np.array([[ 0, -1,  0],
                                                          [-1,  4, -1],
                                                          [ 0, -1,  0]], dtype=np.float32),
            "Máscara Laplaciana 4 (Centro 8)":  np.array([[-1, -1, -1],
                                                          [-1,  8, -1],
                                                          [-1, -1, -1]], dtype=np.float32)
        }

        filtered_laplacian_images = {}
        print("Aplicando filtros Laplacianos...")
        for name, kernel in kernels_laplacianos.items():
            print(f"  Aplicando {name}...")
            filtered_image = laplacian_filter_manual(numpy_image_gray, kernel)
            filtered_laplacian_images[name] = filtered_image
            
            # Salva cada imagem filtrada (normalizada)
            filter_output_filename = f"{os.path.splitext(input_image_filename)[0]}_laplaciano_{name.lower().replace(' ', '_').replace('(', '').replace(')', '')}.jpeg"
            save_numpy_as_image(normalize_to_uint8(filtered_image), os.path.join(output_dir_path, filter_output_filename))

        # Plotar e salvar resultados
        plot_filename = f"plot_{os.path.splitext(input_image_filename)[0]}_laplaciano_results.png"
        plot_output_path = os.path.join(output_dir_path, plot_filename)

        plot_laplacian_results(
            original_gray_numpy=numpy_image_gray,
            filtered_images_dict=filtered_laplacian_images,
            main_title=f"Filtros Laplacianos - {input_image_filename}",
            output_path=plot_output_path
        )
        print("Processamento com filtros Laplacianos concluído.")
    else:
        print(f"Não foi possível carregar a imagem '{input_image_path}'. O script será interrompido.")
