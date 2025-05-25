# Importando as bibliotecas necessárias
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
from typing import Tuple, Union

def load_pil_image(file_path: str) -> Union[Image.Image, None]:
    """
    Carrega uma imagem a partir do caminho do arquivo usando Pillow.

    Args:
        file_path: O caminho para o arquivo de imagem.

    Returns:
        Um objeto Image da PIL se o carregamento for bem-sucedido, None caso contrário.
    """
    try:
        img = Image.open(file_path)
        return img
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em '{file_path}'")
        return None
    except Exception as e:
        print(f"Erro ao carregar a imagem '{file_path}': {e}")
        return None

def save_pil_image(image: Image.Image, file_path: str) -> None:
    """
    Salva uma imagem PIL em um arquivo externo.

    Args:
        image: A imagem PIL a ser salva.
        file_path: O caminho para salvar a imagem.
    """
    try:
        image.save(file_path)
        print(f"Imagem salva em '{file_path}'")
    except Exception as e:
        print(f"Erro ao salvar a imagem em '{file_path}': {e}")

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

def numpy_array_to_pil_image(pixels_array: np.ndarray) -> Image.Image:
    """
    Converte um array NumPy de pixels de volta para uma imagem PIL.
    Assume que o array de entrada já está no tipo de dados correto (ex: uint8 para salvar).

    Args:
        pixels_array: O array NumPy de pixels (espera-se uint8 para conversão direta).

    Returns:
        A imagem PIL correspondente.
    """
    # Se o array for float, clip e converta para uint8
    if pixels_array.dtype != np.uint8:
        pixels_array = np.clip(pixels_array, 0, 255).astype(np.uint8)
    return Image.fromarray(pixels_array)

def pil_to_grayscale_pil(image: Image.Image) -> Image.Image:
    """
    Converte uma imagem PIL para escala de cinza.

    Args:
        image: A imagem PIL (pode ser colorida ou já em escala de cinza).

    Returns:
        A imagem PIL em escala de cinza.
    """
    if image.mode == 'L':
        return image
    return image.convert('L')

def upsample_nearest_neighbor(source_pixels: np.ndarray, scale_factor: int) -> np.ndarray:
    """
    Realiza a ampliação da imagem por vizinho mais próximo usando NumPy.repeat.

    Args:
        source_pixels: Array NumPy da imagem original (H, W) ou (H, W, C), dtype=np.uint8.
        scale_factor: Fator de escala inteiro para a ampliação.

    Returns:
        Array NumPy com a imagem ampliada, dtype=np.uint8.
    """
    if not isinstance(scale_factor, int) or scale_factor < 1:
        raise ValueError("O fator de escala deve ser um inteiro positivo.")
    if source_pixels.ndim not in [2, 3]:
        raise ValueError("A imagem de entrada deve ser 2D (escala de cinza) ou 3D (colorida).")

    # Repete os pixels ao longo do eixo das linhas (0) e depois das colunas (1)
    amplified_pixels = source_pixels.repeat(scale_factor, axis=0).repeat(scale_factor, axis=1)
    return amplified_pixels

def plot_comparison_images(original_color: Image.Image, 
                           original_gray: Image.Image, 
                           amplified_gray: Image.Image, 
                           output_path: str = None) -> None:
    """
    Plota a imagem original colorida, a original em escala de cinza e a ampliada em escala de cinza.

    Args:
        original_color: Imagem PIL original colorida.
        original_gray: Imagem PIL original em escala de cinza.
        amplified_gray: Imagem PIL ampliada em escala de cinza.
        output_path: Caminho opcional para salvar o plot.
    """
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    axes[0].imshow(original_color)
    axes[0].set_title(f"Original Colorida ({original_color.width}x{original_color.height})")
    axes[0].axis('off')

    axes[1].imshow(original_gray, cmap='gray', vmin=0, vmax=255)
    axes[1].set_title(f"Original Cinza ({original_gray.width}x{original_gray.height})")
    axes[1].axis('off')

    axes[2].imshow(amplified_gray, cmap='gray', vmin=0, vmax=255)
    axes[2].set_title(f"Ampliada Vizinho {amplified_gray.width//original_gray.width}x ({amplified_gray.width}x{amplified_gray.height})")
    axes[2].axis('off')

    plt.tight_layout()
    if output_path:
        try:
            plt.savefig(output_path)
            print(f"Plot de comparação salvo em '{output_path}'")
        except Exception as e:
            print(f"Erro ao salvar o plot em '{output_path}': {e}")
    plt.show()

if __name__ == '__main__':
    # Diretório base e nome do arquivo
    base_dir = "1" # Assume que o script está em uma pasta que é irmã da pasta '1'
                   # ou que o CWD permite este caminho relativo.
    input_image_name = "brat.jpeg"
    # Ajuste o path se o script não estiver no diretório pai de '1/'
    # Por exemplo, se o script está em '1/', então input_file_path = input_image_name
    input_file_path = os.path.join(base_dir, input_image_name) 

    # Diretório de saída para os resultados
    output_dir = os.path.join(base_dir, "resultados_ampliacao_vizinho")
    os.makedirs(output_dir, exist_ok=True)

    scale_factor = 2  # Fator de escala (ex: 2 para duplicar a imagem)
    print(f"Fator de ampliação: {scale_factor}x")

    print(f"Carregando imagem: {input_file_path}")
    original_pil = load_pil_image(input_file_path)

    if original_pil:
        try:
            # 1. Converter para escala de cinza (PIL Image)
            print("Convertendo para escala de cinza...")
            gray_pil = pil_to_grayscale_pil(original_pil)

            # 2. Converter imagem cinza para array NumPy uint8 para processamento
            print("Convertendo imagem cinza para array NumPy...")
            gray_numpy_uint8 = pil_to_numpy_array(gray_pil, dtype=np.uint8)

            # 3. Aplicar ampliação por vizinho mais próximo
            # Para uma interpolação por vizinho mais próximo otimizada, considere:
            # amplified_pil_direct = gray_pil.resize(
            #    (gray_pil.width * scale_factor, gray_pil.height * scale_factor), 
            #    Image.Resampling.NEAREST
            # )
            print(f"Aplicando ampliação {scale_factor}x por vizinho mais próximo...")
            amplified_numpy_uint8 = upsample_nearest_neighbor(gray_numpy_uint8, scale_factor)

            # 4. Converter array NumPy ampliado de volta para imagem PIL
            print("Convertendo array ampliado para imagem PIL...")
            amplified_pil = numpy_array_to_pil_image(amplified_numpy_uint8)

            # 5. Salvar a imagem ampliada
            amplified_image_filename = f"{os.path.splitext(input_image_name)[0]}_ampliado_vizinho_{scale_factor}x.jpeg"
            amplified_output_path = os.path.join(output_dir, amplified_image_filename)
            save_pil_image(amplified_pil, amplified_output_path)

            # 6. Plotar e salvar a comparação
            plot_filename = f"{os.path.splitext(input_image_name)[0]}_comparacao_ampliacao_vizinho.png"
            plot_output_path = os.path.join(output_dir, plot_filename)
            plot_comparison_images(original_pil, gray_pil, amplified_pil, plot_output_path)
            
            print("Processamento de ampliação por vizinho mais próximo concluído com sucesso.")

        except ValueError as ve:
            print(f"Erro de valor: {ve}")
        except Exception as e:
            print(f"Ocorreu um erro geral durante o processamento: {e}")
    else:
        print(f"Não foi possível carregar a imagem '{input_file_path}'. Encerrando script.")
