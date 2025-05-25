import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os
from typing import Union, Tuple


def load_image_as_numpy(file_path: str, as_gray: bool = False) -> Union[np.ndarray, None]:
    """
    Carrega uma imagem a partir do caminho do arquivo e a converte para um array NumPy.

    Args:
        file_path: O caminho para o arquivo de imagem.
        as_gray: Se True, converte a imagem para escala de cinza antes de criar o array.

    Returns:
        Um array NumPy representando a imagem se o carregamento for bem-sucedido, None caso contrário.
    """
    try:
        img = Image.open(file_path)
        if as_gray:
            if img.mode != 'L':
                img = img.convert('L')
        return np.array(img)
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em '{file_path}'")
        return None
    except Exception as e:
        print(f"Erro ao carregar a imagem '{file_path}': {e}")
        return None


def save_numpy_as_image(image_array: np.ndarray, file_path: str) -> None:
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


def plot_addition_results(
    image1_array: np.ndarray,
    image2_array: np.ndarray,
    result_array: np.ndarray,
    output_path: str = None
) -> None:
    """
    Plota as duas imagens originais e a imagem resultante da operação de adição.

    Args:
        image1_array: A primeira imagem (array NumPy).
        image2_array: A segunda imagem (array NumPy).
        result_array: A imagem resultante da adição (array NumPy).
        output_path: Caminho opcional para salvar o plot.
    """
    plt.figure(figsize=(18, 6))

    plt.subplot(1, 3, 1)
    plt.imshow(image1_array, cmap='gray', vmin=0, vmax=255 if image1_array.ndim == 2 else None)
    plt.title("Imagem 1")
    plt.axis("off")

    plt.subplot(1, 3, 2)
    plt.imshow(image2_array, cmap='gray', vmin=0, vmax=255 if image2_array.ndim == 2 else None)
    plt.title("Imagem 2")
    plt.axis("off")

    plt.subplot(1, 3, 3)
    plt.imshow(result_array, cmap='gray', vmin=0, vmax=255 if result_array.ndim == 2 else None)
    plt.title("Imagem Resultante (Adição)")
    plt.axis("off")

    plt.tight_layout()
    if output_path:
        try:
            plt.savefig(output_path)
            print(f"Plot salvo em '{output_path}'")
        except Exception as e:
            print(f"Erro ao salvar o plot em '{output_path}': {e}")
    plt.show()


def add_images_numpy(image1_array: np.ndarray, image2_array: np.ndarray) -> np.ndarray:
    """
    Adiciona duas imagens (arrays NumPy) pixel a pixel.
    A soma é truncada para o intervalo [0, 255].
    As imagens devem ter o mesmo tamanho.

    Args:
        image1_array: O array NumPy da primeira imagem (uint8).
        image2_array: O array NumPy da segunda imagem (uint8).

    Returns:
        Um array NumPy (uint8) com o resultado da adição.

    Raises:
        ValueError: Se as imagens não tiverem o mesmo formato (shape).
    """
    if image1_array.shape != image2_array.shape:
        raise ValueError("As imagens devem ter o mesmo tamanho para a adição.")

    # Converter para um tipo maior para evitar overflow durante a soma intermediária
    sum_array = image1_array.astype(np.int16) + image2_array.astype(np.int16)

    # Truncar o resultado para o intervalo [0, 255]
    result_array = np.clip(sum_array, 0, 255)

    return result_array.astype(np.uint8)


if __name__ == '__main__':
    # Diretório de entrada e nomes das imagens
    input_dir = "/home/andre/dev/processamento_de_imagens_2024-2/2"
    image_name1 = "14.png"
    image_name2 = "19.png"

    image_path1 = os.path.join(input_dir, image_name1)
    image_path2 = os.path.join(input_dir, image_name2)

    # Diretório de saída
    output_dir = os.path.join(input_dir, "resultados_adicao")
    os.makedirs(output_dir, exist_ok=True)

    print(f"Processando adição entre: '{image_path1}' e '{image_path2}'")

    # Carrega as imagens em escala de cinza como arrays NumPy:
    pixels1_np = load_image_as_numpy(image_path1, as_gray=True)
    pixels2_np = load_image_as_numpy(image_path2, as_gray=True)

    if pixels1_np is not None and pixels2_np is not None:
        try:
            # Chama a função de adição otimizada:
            added_image_np = add_images_numpy(pixels1_np, pixels2_np)

            # Define os nomes dos arquivos de saída
            base_name1 = os.path.splitext(image_name1)[0]
            base_name2 = os.path.splitext(image_name2)[0]
            output_image_filename = f"adicao_{base_name1}_mais_{base_name2}.png"
            output_image_path = os.path.join(output_dir, output_image_filename)

            plot_output_filename = f"plot_adicao_{base_name1}_mais_{base_name2}.png"
            plot_output_path = os.path.join(output_dir, plot_output_filename)

            # Salva a nova imagem resultado:
            save_numpy_as_image(added_image_np, output_image_path)

            # Plota as imagens originais e a imagem resultante:
            plot_addition_results(pixels1_np, pixels2_np, added_image_np, plot_output_path)

            print("Processamento de adição concluído com sucesso.")

        except ValueError as ve:
            print(f"Erro de valor: {ve}")
        except Exception as e:
            print(f"Ocorreu um erro durante o processamento da adição: {e}")
    else:
        print("Não foi possível carregar uma ou ambas as imagens. Encerrando o script.")
