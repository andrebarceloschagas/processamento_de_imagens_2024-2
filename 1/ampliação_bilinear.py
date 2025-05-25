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

def pil_to_numpy_float32(image: Image.Image) -> np.ndarray:
    """
    Converte uma imagem PIL para um array NumPy com dtype float32.
    Float32 é usado para manter precisão em cálculos intermediários.

    Args:
        image: A imagem PIL.

    Returns:
        Um array NumPy representando a imagem.
    """
    return np.array(image, dtype=np.float32)

def numpy_to_pil_image(pixels_array: np.ndarray) -> Image.Image:
    """
    Converte um array NumPy de pixels de volta para uma imagem PIL.
    Os valores são truncados para [0, 255] e convertidos para uint8.

    Args:
        pixels_array: O array NumPy de pixels.

    Returns:
        A imagem PIL correspondente.
    """
    # Garante que os valores dos pixels estejam entre 0 e 255
    clipped_pixels = np.clip(pixels_array, 0, 255)
    # Converte o array de volta para uint8 e cria uma imagem
    image = Image.fromarray(clipped_pixels.astype(np.uint8))
    return image

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

def upsample_2x_custom_bilinear(source_pixels: np.ndarray) -> np.ndarray:
    """
    Realiza uma ampliação de 2x em uma imagem usando um método de interpolação bilinear customizado.
    Para cada pixel da imagem original, um bloco 2x2 é gerado na imagem de destino.
    - O pixel do canto superior esquerdo (0,0) do bloco é o pixel original.
    - O pixel (0,1) é a média dos vizinhos horizontais originais.
    - O pixel (1,0) é a média dos vizinhos verticais originais.
    - O pixel (1,1) é a média dos quatro vizinhos originais.

    Args:
        source_pixels: Array NumPy (H, W) ou (H, W, C) da imagem original (dtype float32).

    Returns:
        Array NumPy (2*H, 2*W) ou (2*H, 2*W, C) com a imagem ampliada (dtype float32).
    """
    source_height, source_width = source_pixels.shape[:2]
    
    target_height = source_height * 2
    target_width = source_width * 2

    if source_pixels.ndim == 3: # Imagem colorida
        channels = source_pixels.shape[2]
        target_pixels = np.zeros((target_height, target_width, channels), dtype=np.float32)
    else: # Imagem em escala de cinza
        channels = 1
        target_pixels = np.zeros((target_height, target_width), dtype=np.float32)

    for i_target in range(0, target_height, 2):
        for j_target in range(0, target_width, 2):
            # Índices correspondentes na imagem original
            i_source = i_target // 2
            j_source = j_target // 2

            # Índices dos vizinhos na imagem original, com tratamento de bordas
            i_source_plus_1 = min(i_source + 1, source_height - 1)
            j_source_plus_1 = min(j_source + 1, source_width - 1)

            # Pegar os quatro pixels vizinhos da imagem original
            p_ij = source_pixels[i_source, j_source]
            p_i1j = source_pixels[i_source_plus_1, j_source]
            p_ij1 = source_pixels[i_source, j_source_plus_1]
            p_i1j1 = source_pixels[i_source_plus_1, j_source_plus_1]
            
            # Atribuindo os valores aos novos pixels no bloco 2x2 de destino
            target_pixels[i_target, j_target] = p_ij  # Ponto original (top-left)
            
            # Ponto interpolado 'a' (top-right)
            val_a = (p_ij + p_ij1) / 2.0
            target_pixels[i_target, j_target + 1] = val_a
            
            # Ponto interpolado 'b' (bottom-left)
            val_b = (p_ij + p_i1j) / 2.0
            target_pixels[i_target + 1, j_target] = val_b
            
            # Ponto interpolado 'c' (bottom-right)
            val_c = (p_ij + p_ij1 + p_i1j + p_i1j1) / 4.0
            target_pixels[i_target + 1, j_target + 1] = val_c
            
    return target_pixels

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
    axes[2].set_title(f"Ampliada 2x Cinza ({amplified_gray.width}x{amplified_gray.height})")
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
    # Nota: O caminho original era "/home/andre/desenvolvimento/...", 
    # ajustado para ser relativo ao workspace "/home/andre/dev/..."
    base_dir = "1" 
    input_image_name = "brat.jpeg"
    input_file_path = os.path.join(base_dir, input_image_name)

    # Diretório de saída para os resultados
    output_dir = os.path.join(base_dir, "resultados_ampliacao_bilinear")
    os.makedirs(output_dir, exist_ok=True)

    print(f"Carregando imagem: {input_file_path}")
    original_pil = load_pil_image(input_file_path)

    if original_pil:
        try:
            # 1. Converter para escala de cinza (PIL Image)
            print("Convertendo para escala de cinza...")
            gray_pil = pil_to_grayscale_pil(original_pil)
            
            # Salvar a imagem em escala de cinza original (opcional)
            # gray_output_path = os.path.join(output_dir, f"{os.path.splitext(input_image_name)[0]}_gray.jpeg")
            # save_pil_image(gray_pil, gray_output_path)

            # 2. Converter imagem cinza para array NumPy float32 para processamento
            print("Convertendo imagem cinza para array NumPy...")
            gray_numpy_float32 = pil_to_numpy_float32(gray_pil)

            # 3. Aplicar ampliação 2x customizada
            # Para uma interpolação bilinear mais geral e otimizada, considere:
            # amplified_pil = gray_pil.resize((gray_pil.width * 2, gray_pil.height * 2), Image.Resampling.BILINEAR)
            print("Aplicando ampliação 2x customizada...")
            amplified_numpy_float32 = upsample_2x_custom_bilinear(gray_numpy_float32)

            # 4. Converter array NumPy ampliado de volta para imagem PIL
            print("Convertendo array ampliado para imagem PIL...")
            amplified_pil = numpy_to_pil_image(amplified_numpy_float32)

            # 5. Salvar a imagem ampliada
            amplified_image_filename = f"{os.path.splitext(input_image_name)[0]}_ampliado_2x_custom.jpeg"
            amplified_output_path = os.path.join(output_dir, amplified_image_filename)
            save_pil_image(amplified_pil, amplified_output_path)

            # 6. Plotar e salvar a comparação
            plot_filename = f"{os.path.splitext(input_image_name)[0]}_comparacao_ampliacao.png"
            plot_output_path = os.path.join(output_dir, plot_filename)
            plot_comparison_images(original_pil, gray_pil, amplified_pil, plot_output_path)
            
            print("Processamento de ampliação concluído com sucesso.")

        except Exception as e:
            print(f"Ocorreu um erro geral durante o processamento: {e}")
    else:
        print(f"Não foi possível carregar a imagem '{input_file_path}'. Encerrando script.")
