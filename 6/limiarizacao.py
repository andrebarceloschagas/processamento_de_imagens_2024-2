import os
import numpy as np
from PIL import Image, UnidentifiedImageError
import matplotlib.pyplot as plt
from typing import Optional # Union and Tuple were not strictly needed here


# --- Funções Auxiliares Padronizadas ---

def load_pil_image(file_path: str) -> Optional[Image.Image]:
    """
    Carrega uma imagem a partir do caminho do arquivo usando Pillow.

    Args:
        file_path: Caminho para o arquivo de imagem.

    Returns:
        Um objeto Image da PIL se o carregamento for bem-sucedido, None caso contrário.
    """
    try:
        img = Image.open(file_path)
        return img
    except FileNotFoundError:
        print(f"Erro: Arquivo de imagem não encontrado em '{file_path}'.")
    except UnidentifiedImageError:
        print(f"Erro: Não foi possível identificar o arquivo de imagem. Pode estar corrompido ou não ser um formato suportado: '{file_path}'.")
    except Exception as e:
        print(f"Um erro inesperado ocorreu ao carregar a imagem '{file_path}': {e}")
    return None

def pil_to_numpy_array(image: Image.Image, dtype: type = np.uint8) -> np.ndarray:
    """
    Converte uma imagem PIL para um array NumPy.

    Args:
        image: A imagem PIL.
        dtype: O tipo de dados desejado para o array NumPy (padrão: np.uint8).

    Returns:
        Um array NumPy representando a imagem.
    """
    return np.array(image, dtype=dtype)

def numpy_to_pil_image(array: np.ndarray) -> Image.Image:
    """
    Converte um array NumPy para uma imagem PIL.
    Lida com escala de cinza (2D) e RGB (3D).

    Args:
        array: O array NumPy.

    Returns:
        Um objeto Image da PIL.
    """
    if array.ndim == 2:
        # Garante que o array seja uint8 para o modo 'L'
        if array.dtype != np.uint8:
            # Normaliza se for float, por exemplo, assumindo 0-1 ou 0-255
            if np.max(array) <= 1.0 and np.min(array) >= 0.0 and array.dtype != np.uint8: # Float 0-1
                 array = (array * 255).astype(np.uint8)
            else: # Outros tipos, tenta converter direto, clip para garantir
                 array = np.clip(array, 0, 255).astype(np.uint8)
        return Image.fromarray(array, 'L')
    elif array.ndim == 3 and array.shape[2] == 3:
        return Image.fromarray(array.astype(np.uint8), 'RGB')
    elif array.ndim == 3 and array.shape[2] == 4: # Suporte para RGBA
        return Image.fromarray(array.astype(np.uint8), 'RGBA')
    else:
        raise ValueError(f"Formato de array NumPy não suportado para conversão PIL: {array.shape}, dtype: {array.dtype}")

def save_numpy_as_image(array: np.ndarray, file_path: str) -> None:
    """
    Salva um array NumPy como um arquivo de imagem usando Pillow.

    Args:
        array: O array NumPy representando a imagem.
        file_path: Caminho para salvar o arquivo de imagem.
    """
    try:
        image = numpy_to_pil_image(array)
        image.save(file_path)
        print(f"Imagem salva com sucesso em '{file_path}'.")
    except Exception as e:
        print(f"Erro ao salvar imagem em '{file_path}': {e}")

def convert_pil_to_grayscale_numpy(image: Image.Image) -> np.ndarray:
    """
    Converte uma imagem PIL para um array NumPy em escala de cinza (uint8).

    Args:
        image: A imagem PIL de entrada.

    Returns:
        Um array NumPy representando a imagem em escala de cinza.
    """
    if image.mode == 'L':
        return pil_to_numpy_array(image, dtype=np.uint8)
    return pil_to_numpy_array(image.convert('L'), dtype=np.uint8)


# --- Função Principal de Limiarização ---

def manual_thresholding(image_gray_numpy: np.ndarray, threshold_value: int) -> np.ndarray:
    """
    Aplica limiarização manual a uma imagem em escala de cinza.
    Pixels com valor > threshold_value tornam-se 255 (branco), outros 0 (preto).

    Args:
        image_gray_numpy: Array NumPy 2D da imagem em escala de cinza (esperado ser uint8).
        threshold_value: Valor do limiar (0-255).

    Returns:
        Array NumPy 2D da imagem binarizada (uint8, valores 0 ou 255).
    """
    if not (0 <= threshold_value <= 255):
        raise ValueError("O valor do limiar deve estar entre 0 e 255.")
    if image_gray_numpy.ndim != 2:
        raise ValueError("A imagem de entrada para limiarização deve ser 2D (escala de cinza).")
    
    # Garante que a imagem de entrada seja uint8 para a comparação
    current_dtype = image_gray_numpy.dtype
    if current_dtype != np.uint8:
        print(f"Aviso: A imagem de entrada para limiarização não é uint8 (dtype: {current_dtype}). Será convertida/clipada para uint8.")
        if np.issubdtype(current_dtype, np.floating) and np.max(image_gray_numpy) <= 1.0 and np.min(image_gray_numpy) >=0.0:
            image_gray_numpy = (image_gray_numpy * 255).astype(np.uint8)
        else:
            image_gray_numpy = np.clip(image_gray_numpy, 0, 255).astype(np.uint8)

    # Cria a imagem binária: True onde > threshold_value, False caso contrário
    binary_image = image_gray_numpy > threshold_value
    
    # Converte o array booleano para uint8 (True -> 1, False -> 0) e multiplica por 255
    return binary_image.astype(np.uint8) * 255


# --- Função de Plotagem ---

def plot_thresholding_results(
    original_gray_numpy: np.ndarray,
    thresholded_image_numpy: np.ndarray,
    threshold_value: int,
    main_title: str = "Resultados da Limiarização",
    output_path: Optional[str] = None
) -> None:
    """
    Plota a imagem original em escala de cinza e a imagem limiarizada.

    Args:
        original_gray_numpy: Imagem original em escala de cinza (NumPy array).
        thresholded_image_numpy: Imagem limiarizada (NumPy array).
        threshold_value: Valor do limiar utilizado.
        main_title: Título principal para o plot.
        output_path: Caminho opcional para salvar o plot.
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    fig.suptitle(f"{main_title} (Limiar: {threshold_value})", fontsize=16)

    axes[0].imshow(original_gray_numpy, cmap='gray', vmin=0, vmax=255)
    axes[0].set_title(f"Original em Cinza\nShape: {original_gray_numpy.shape}")
    axes[0].axis('off')

    axes[1].imshow(thresholded_image_numpy, cmap='gray', vmin=0, vmax=255)
    axes[1].set_title(f"Imagem Limiarizada\nShape: {thresholded_image_numpy.shape}")
    axes[1].axis('off')

    plt.tight_layout(rect=[0, 0, 1, 0.95]) # Ajuste para o supertítulo
    
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
    
    # Tenta usar '18.png', se não existir, tenta 'img.png' ou 'image.png'
    input_image_filename_options = ["18.png", "img.png", "image.png"]
    input_image_filename = None
    input_image_full_path = None

    for fname in input_image_filename_options:
        temp_path = os.path.join(script_dir, fname)
        if os.path.exists(temp_path):
            input_image_filename = fname
            input_image_full_path = temp_path
            print(f"Usando imagem de entrada: '{input_image_full_path}'")
            break
    
    if not input_image_full_path:
        print(f"Nenhuma das imagens de entrada padrão ({', '.join(input_image_filename_options)}) foi encontrada em '{script_dir}'.")
        # exit(1) # Considerar sair se nenhuma imagem for encontrada

    output_dir_name = "resultados_limiarizacao"
    output_dir_path = os.path.join(script_dir, output_dir_name)

    default_threshold = 128

    try:
        os.makedirs(output_dir_path, exist_ok=True)
        print(f"Diretório de saída '{output_dir_path}' assegurado.")
    except OSError as e:
        print(f"Erro ao criar diretório de saída '{output_dir_path}': {e}")
        # exit(1) # Considerar sair

    if input_image_full_path and input_image_filename: # Procede apenas se uma imagem foi encontrada
        print(f"Carregando imagem: '{input_image_full_path}'...")
        pil_image_original = load_pil_image(input_image_full_path)

        if pil_image_original:
            print("Convertendo imagem para array NumPy em escala de cinza...")
            numpy_image_gray = convert_pil_to_grayscale_numpy(pil_image_original)
            
            base_filename = os.path.splitext(input_image_filename)[0]
            original_gray_filename = f"{base_filename}_gray_numpy.png"
            original_gray_output_path = os.path.join(output_dir_path, original_gray_filename)
            save_numpy_as_image(numpy_image_gray, original_gray_output_path)

            print(f"Aplicando limiarização manual com limiar = {default_threshold}...")
            numpy_image_thresholded = manual_thresholding(numpy_image_gray, default_threshold)

            thresholded_filename = f"{base_filename}_thresholded_{default_threshold}.png"
            thresholded_output_path = os.path.join(output_dir_path, thresholded_filename)
            save_numpy_as_image(numpy_image_thresholded, thresholded_output_path)

            plot_filename = f"plot_{base_filename}_thresholding_results.png"
            plot_output_path = os.path.join(output_dir_path, plot_filename)

            plot_thresholding_results(
                original_gray_numpy=numpy_image_gray,
                thresholded_image_numpy=numpy_image_thresholded,
                threshold_value=default_threshold,
                main_title=f"Limiarização Manual - {input_image_filename}",
                output_path=plot_output_path
            )
            print(f"Processamento de limiarização para '{input_image_filename}' concluído.")
        else:
            print(f"Não foi possível carregar a imagem '{input_image_full_path}'. O script será interrompido.")
    else:
        print("Nenhuma imagem de entrada válida foi processada.")
