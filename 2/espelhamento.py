from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
from typing import Union, Tuple


def load_image_pil(file_path: str) -> Union[Image.Image, None]:
    """
    Carrega uma imagem a partir do caminho do arquivo usando Pillow.

    Args:
        file_path: O caminho para o arquivo de imagem.

    Returns:
        Um objeto Image da PIL se o carregamento for bem-sucedido, None caso contrário.
    """
    try:
        image = Image.open(file_path)
        return image
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em '{file_path}'")
        return None
    except Exception as e:
        print(f"Erro ao carregar a imagem '{file_path}' com Pillow: {e}")
        return None


def load_numpy_array_from_image(file_path: str, as_gray: bool = False) -> Union[np.ndarray, None]:
    """
    Carrega uma imagem e a converte para um array NumPy.

    Args:
        file_path: O caminho para o arquivo de imagem.
        as_gray: Se True, converte a imagem para escala de cinza antes de criar o array.

    Returns:
        Um array NumPy representando a imagem se o carregamento for bem-sucedido, None caso contrário.
    """
    pil_image = load_image_pil(file_path)
    if pil_image is None:
        return None
    try:
        if as_gray:
            if pil_image.mode != 'L':
                pil_image = pil_image.convert('L')
        return np.array(pil_image)
    except Exception as e:
        print(f"Erro ao converter imagem para array NumPy: {e}")
        return None


def save_numpy_array_as_image(image_array: np.ndarray, file_path: str) -> None:
    """
    Salva um array NumPy como um arquivo de imagem.

    Args:
        image_array: O array NumPy a ser salvo (espera-se dtype=uint8).
        file_path: O caminho do arquivo para salvar a imagem.
    """
    try:
        image = Image.fromarray(image_array.astype(np.uint8))
        image.save(file_path)
        print(f"Imagem salva em '{file_path}'")
    except Exception as e:
        print(f"Erro ao salvar a imagem em '{file_path}': {e}")


def plot_mirroring_results(
    original_pil_image: Image.Image,
    gray_numpy_array: np.ndarray,
    mirrored_numpy_array: np.ndarray,
    output_path: str = None
) -> None:
    """
    Plota a imagem original (colorida), em escala de cinza e a imagem espelhada.

    Args:
        original_pil_image: A imagem original (objeto Pillow Image).
        gray_numpy_array: A imagem em escala de cinza (array NumPy).
        mirrored_numpy_array: A imagem espelhada (array NumPy).
        output_path: Caminho opcional para salvar o plot.
    """
    plt.figure(figsize=(18, 6))

    plt.subplot(1, 3, 1)
    plt.imshow(original_pil_image)
    plt.title("Imagem Original")
    plt.axis("off")

    plt.subplot(1, 3, 2)
    plt.imshow(gray_numpy_array, cmap='gray', vmin=0, vmax=255)
    plt.title("Imagem em Escala de Cinza")
    plt.axis("off")

    plt.subplot(1, 3, 3)
    plt.imshow(mirrored_numpy_array, cmap='gray', vmin=0, vmax=255)
    plt.title("Imagem Espelhada Horizontalmente")
    plt.axis("off")

    plt.tight_layout()
    if output_path:
        try:
            plt.savefig(output_path)
            print(f"Plot salvo em '{output_path}'")
        except Exception as e:
            print(f"Erro ao salvar o plot em '{output_path}': {e}")
    plt.show()


def mirror_horizontal_numpy(image_array: np.ndarray) -> np.ndarray:
    """
    Realiza o espelhamento horizontal de uma imagem representada por um array NumPy.

    Args:
        image_array: O array NumPy da imagem (pode ser 2D para escala de cinza ou 3D para colorida).

    Returns:
        Um novo array NumPy com a imagem espelhada horizontalmente.
    """
    # np.fliplr(image_array) ou image_array[:, ::-1] para 2D
    # Para imagens coloridas (3D: altura, largura, canais), o espelhamento é nas colunas (segunda dimensão)
    if image_array.ndim == 3:
        return image_array[:, ::-1, :]
    elif image_array.ndim == 2:
        return image_array[:, ::-1]
    else:
        raise ValueError("O array da imagem deve ser 2D (escala de cinza) ou 3D (colorida).")


if __name__ == '__main__':
    # Diretório de entrada e nome da imagem
    input_dir = "/home/andre/dev/processamento_de_imagens_2024-2/2"
    input_image_name = "olho.jpg"
    input_image_path = os.path.join(input_dir, input_image_name)

    # Diretório de saída
    output_dir = os.path.join(input_dir, "resultados_espelhamento")
    os.makedirs(output_dir, exist_ok=True)

    print(f"Processando imagem: {input_image_path}")

    # Carrega a imagem original com Pillow para plotagem (mantém cores se houver)
    original_pil = load_image_pil(input_image_path)

    # Carrega a imagem como array NumPy em escala de cinza para processamento
    gray_numpy = load_numpy_array_from_image(input_image_path, as_gray=True)

    if original_pil and gray_numpy is not None:
        try:
            print("Aplicando espelhamento horizontal...")
            mirrored_image_numpy = mirror_horizontal_numpy(gray_numpy)

            # Define os nomes dos arquivos de saída
            base_name = os.path.splitext(input_image_name)[0]
            mirrored_output_filename = f"{base_name}_mirrored.jpg"
            mirrored_output_path = os.path.join(output_dir, mirrored_output_filename)
            
            plot_output_filename = f"{base_name}_mirroring_comparison_plot.png"
            plot_output_path = os.path.join(output_dir, plot_output_filename)

            # Salva a imagem espelhada
            save_numpy_array_as_image(mirrored_image_numpy, mirrored_output_path)

            # Plota os resultados
            plot_mirroring_results(original_pil, gray_numpy, mirrored_image_numpy, plot_output_path)
            
            print("Processamento de espelhamento concluído com sucesso.")

        except ValueError as ve:
            print(f"Erro de valor durante o espelhamento: {ve}")
        except Exception as e:
            print(f"Ocorreu um erro durante o processamento da imagem '{input_image_name}': {e}")
    else:
        print(f"Não foi possível carregar a imagem '{input_image_name}' corretamente. Encerrando o script.")
