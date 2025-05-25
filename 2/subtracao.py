import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os
from typing import Union, Tuple

def load_image(file_path: str, as_gray: bool = False) -> Union[np.ndarray, None]:
    """
    Carrega uma imagem a partir do caminho do arquivo.

    Args:
        file_path: O caminho para o arquivo de imagem.
        as_gray: Se True, converte a imagem para escala de cinza.

    Returns:
        Um array NumPy representando a imagem se o carregamento for bem-sucedido, None caso contrário.
    """
    try:
        img = Image.open(file_path)
        if as_gray:
            img = img.convert('L')
        return np.array(img)
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em '{file_path}'")
        return None
    except Exception as e:
        print(f"Erro ao carregar a imagem '{file_path}': {e}")
        return None

def save_image(pixels: np.ndarray, file_path: str) -> None:
    """
    Salva a imagem (array de pixels) em um arquivo externo.

    Args:
        pixels: O array NumPy de pixels da imagem.
        file_path: O caminho para salvar a imagem.
    """
    try:
        image = Image.fromarray(pixels.astype('uint8'))
        image.save(file_path)
        print(f"Imagem salva em '{file_path}'")
    except Exception as e:
        print(f"Erro ao salvar a imagem em '{file_path}': {e}")


def plot_images(image1: np.ndarray, image2: np.ndarray, result_image: np.ndarray, output_path: str = None) -> None:
    """
    Plota as imagens originais e a imagem resultante da operação de subtração.

    Args:
        image1: A primeira imagem (array NumPy).
        image2: A segunda imagem (array NumPy).
        result_image: A imagem resultante da subtração (array NumPy).
        output_path: Caminho opcional para salvar o plot.
    """
    plt.figure(figsize=(15, 5))

    # Primeira imagem
    plt.subplot(1, 3, 1)
    plt.imshow(image1, cmap='gray', vmin=0, vmax=255 if image1.ndim == 2 else None)
    plt.title("Imagem 1")
    plt.axis("off")

    # Segunda imagem
    plt.subplot(1, 3, 2)
    plt.imshow(image2, cmap='gray', vmin=0, vmax=255 if image2.ndim == 2 else None)
    plt.title("Imagem 2")
    plt.axis("off")

    # Imagem resultante (subtração)
    plt.subplot(1, 3, 3)
    plt.imshow(result_image, cmap='gray', vmin=0, vmax=255 if result_image.ndim == 2 else None)
    plt.title("Imagem Resultante (Subtração)")
    plt.axis("off")

    plt.tight_layout()
    if output_path:
        try:
            plt.savefig(output_path)
            print(f"Plot salvo em '{output_path}'")
        except Exception as e:
            print(f"Erro ao salvar o plot em '{output_path}': {e}")
    plt.show()

def subtract_images(image1_array: np.ndarray, image2_array: np.ndarray) -> np.ndarray:
    """
    Subtrai duas imagens (arrays NumPy).
    A subtração é feita pixel a pixel. Se o resultado for negativo, é truncado para 0.
    As imagens devem ter o mesmo tamanho e tipo.

    Args:
        image1_array: O array NumPy da primeira imagem.
        image2_array: O array NumPy da segunda imagem.

    Returns:
        Um array NumPy com o resultado da subtração.

    Raises:
        ValueError: Se as imagens não tiverem o mesmo formato (shape).
    """
    if image1_array.shape != image2_array.shape:
        raise ValueError("As imagens devem ter o mesmo tamanho para a subtração.")

    # Converte para int para evitar overflow/underflow durante a subtração
    # e permitir valores negativos temporariamente.
    subtracted_array = image1_array.astype(np.int16) - image2_array.astype(np.int16)
    
    # Trunca valores negativos para 0 e valores > 255 para 255 (embora subtração não gere > 255 se inputs são uint8)
    # np.clip é mais eficiente que um loop manual.
    result_array = np.clip(subtracted_array, 0, 255)
    
    return result_array.astype(np.uint8)

if __name__ == '__main__':
    # Diretório de entrada e saída
    input_dir = "/home/andre/dev/processamento_de_imagens_2024-2/2"
    output_dir = os.path.join(input_dir, "resultados_subtracao")
    
    # Cria o diretório de saída se não existir
    os.makedirs(output_dir, exist_ok=True)

    # Nomes dos arquivos de imagem de entrada
    image_name1 = "8.png"
    image_name2 = "12.png"
    
    image_path1 = os.path.join(input_dir, image_name1)
    image_path2 = os.path.join(input_dir, image_name2)

    print(f"Processando subtração entre: '{image_path1}' e '{image_path2}'")

    # Carrega as imagens em escala de cinza:
    pixels1 = load_image(image_path1, as_gray=True)
    pixels2 = load_image(image_path2, as_gray=True)

    if pixels1 is not None and pixels2 is not None:
        try:
            # Chama a função de subtração:
            subtracted_image_array = subtract_images(pixels1, pixels2)

            # Define os nomes dos arquivos de saída
            base_name1 = os.path.splitext(image_name1)[0]
            base_name2 = os.path.splitext(image_name2)[0]
            output_image_filename = f"subtracao_{base_name1}_menos_{base_name2}.png"
            output_image_path = os.path.join(output_dir, output_image_filename)
            
            plot_output_filename = f"plot_subtracao_{base_name1}_menos_{base_name2}.png"
            plot_output_path = os.path.join(output_dir, plot_output_filename)

            # Salva a nova imagem resultado:
            save_image(subtracted_image_array, output_image_path)

            # Plota as imagens originais e a imagem resultante:
            plot_images(pixels1, pixels2, subtracted_image_array, plot_output_path)
            
            print("Processamento de subtração concluído com sucesso.")

        except ValueError as ve:
            print(f"Erro de valor: {ve}")
        except Exception as e:
            print(f"Ocorreu um erro durante o processamento da subtração: {e}")
    else:
        print("Não foi possível carregar uma ou ambas as imagens. Encerrando o script.")
