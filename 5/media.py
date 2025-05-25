import os
import numpy as np
from PIL import Image, UnidentifiedImageError
import matplotlib.pyplot as plt
from typing import Tuple, Union

# --- Funções Auxiliares Padronizadas (Reutilizadas e adaptadas) ---

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

# --- Função Principal do Filtro da Média ---

def mean_filter_manual(image_gray_numpy: np.ndarray, kernel_size: int) -> np.ndarray:
    """
    Aplica um filtro da média a uma imagem em escala de cinza.
    Trata as bordas replicando os pixels da borda.

    Nota: Para desempenho, considere `scipy.ndimage.uniform_filter` ou `cv2.blur`.

    Args:
        image_gray_numpy: Array NumPy 2D representando a imagem em escala de cinza.
        kernel_size: Tamanho da janela do filtro (deve ser ímpar e positivo).

    Returns:
        Array NumPy 2D da imagem filtrada (dtype original da entrada, usualmente uint8).
    
    Raises:
        ValueError: Se kernel_size não for ímpar ou for não positivo.
    """
    if not isinstance(kernel_size, int) or kernel_size <= 0 or kernel_size % 2 == 0:
        raise ValueError("kernel_size deve ser um inteiro ímpar positivo.")

    if image_gray_numpy.ndim != 2:
        raise ValueError("A imagem de entrada para o filtro da média deve ser 2D (escala de cinza).")

    pad_size = kernel_size // 2
    
    # Adiciona padding replicando as bordas
    padded_image = np.pad(image_gray_numpy, pad_size, mode='edge')
    
    # Prepara o array de saída com o mesmo dtype da entrada para evitar conversões desnecessárias
    # se a entrada já for float. Se for int, a média pode gerar float.
    output_image_dtype = np.float32 if np.issubdtype(image_gray_numpy.dtype, np.integer) else image_gray_numpy.dtype
    filtered_image = np.zeros_like(image_gray_numpy, dtype=output_image_dtype)
    
    image_height, image_width = image_gray_numpy.shape

    for r in range(image_height):
        for c in range(image_width):
            # A região no array com padding corresponde à janela do kernel centrada em (r,c) na imagem original
            region = padded_image[r : r + kernel_size, c : c + kernel_size]
            filtered_image[r, c] = np.mean(region)
    
    # Se a entrada era inteira, a saída float32 deve ser convertida de volta para uint8 após o clipping.
    if np.issubdtype(image_gray_numpy.dtype, np.integer):
        return np.clip(filtered_image, 0, 255).astype(np.uint8)
    return filtered_image # Se a entrada já era float, retorna como está (ou clippar se necessário)


# --- Função de Plotagem ---

def plot_mean_filter_results(
    original_gray_numpy: np.ndarray,
    filtered_numpy: np.ndarray,
    kernel_size: int,
    main_title: str = "Resultado do Filtro da Média",
    output_path: Union[str, None] = None
) -> None:
    """
    Plota a imagem original em cinza e a imagem filtrada pela média.

    Args:
        original_gray_numpy: Imagem original em escala de cinza (NumPy array).
        filtered_numpy: Imagem filtrada pela média (NumPy array).
        kernel_size: Tamanho do kernel usado para o filtro.
        main_title: Título principal para o plot.
        output_path: Caminho opcional para salvar o plot.
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    fig.suptitle(f"{main_title} (Kernel {kernel_size}x{kernel_size})", fontsize=16)

    axes[0].imshow(original_gray_numpy, cmap='gray', vmin=0, vmax=255)
    axes[0].set_title(f"Original em Cinza\nShape: {original_gray_numpy.shape}")
    axes[0].axis('off')

    axes[1].imshow(filtered_numpy, cmap='gray', vmin=0, vmax=255)
    axes[1].set_title(f"Filtrada pela Média\nShape: {filtered_numpy.shape}")
    axes[1].axis('off')

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
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
    
    input_image_filename = "marisa.jpg"  # Exemplo, pode ser alterado
    input_image_path = os.path.join(script_dir, input_image_filename)

    output_dir_name = "resultados_filtro_media"
    output_dir_path = os.path.join(script_dir, output_dir_name)

    try:
        os.makedirs(output_dir_path, exist_ok=True)
        print(f"Diretório de saída '{output_dir_path}' assegurado.")
    except OSError as e:
        print(f"Erro ao criar diretório de saída '{output_dir_path}': {e}")
        # exit(1)

    kernel_filter_size = 3 # Tamanho do kernel para o filtro da média (ex: 3, 5, 7)

    print(f"Carregando imagem: '{input_image_path}'...")
    pil_image_original = load_pil_image(input_image_path)

    if pil_image_original:
        print("Convertendo imagem para array NumPy em escala de cinza...")
        numpy_image_gray = convert_pil_to_grayscale_numpy(pil_image_original)
        
        original_gray_filename = f"{os.path.splitext(input_image_filename)[0]}_gray_numpy.jpg"
        original_gray_output_path = os.path.join(output_dir_path, original_gray_filename)
        save_numpy_as_image(numpy_image_gray, original_gray_output_path)

        print(f"Aplicando filtro da média com kernel {kernel_filter_size}x{kernel_filter_size}...")
        try:
            filtered_image_numpy = mean_filter_manual(numpy_image_gray, kernel_filter_size)
            
            # Salva a imagem filtrada
            filtered_image_filename = f"{os.path.splitext(input_image_filename)[0]}_media_k{kernel_filter_size}.jpg"
            filtered_image_output_path = os.path.join(output_dir_path, filtered_image_filename)
            save_numpy_as_image(filtered_image_numpy, filtered_image_output_path)

            # Plotar e salvar resultados
            plot_filename = f"plot_{os.path.splitext(input_image_filename)[0]}_media_k{kernel_filter_size}.png"
            plot_output_path = os.path.join(output_dir_path, plot_filename)

            plot_mean_filter_results(
                original_gray_numpy=numpy_image_gray,
                filtered_numpy=filtered_image_numpy,
                kernel_size=kernel_filter_size,
                main_title=f"Filtro da Média - {input_image_filename}",
                output_path=plot_output_path
            )

        except ValueError as ve:
            print(f"Erro ao aplicar filtro: {ve}")
        except Exception as e:
            print(f"Um erro inesperado ocorreu durante a filtragem: {e}")
            
        print("Processamento com filtro da média concluído.")
    else:
        print(f"Não foi possível carregar a imagem '{input_image_path}'. O script será interrompido.")
