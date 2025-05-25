import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
from typing import Tuple, Union

def load_image(file_path: str) -> Union[Image.Image, None]:
    """
    Carrega uma imagem a partir do caminho do arquivo.

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
        print(f"Erro ao carregar a imagem '{file_path}': {e}")
        return None

def rgb_to_gray(image: Image.Image) -> Image.Image:
    """
    Converte uma imagem PIL para escala de cinza.

    Args:
        image: A imagem PIL a ser convertida.

    Returns:
        A imagem convertida para escala de cinza.
    """
    return image.convert('L')

def plot_images(original: Image.Image, gray: Image.Image, negative: Image.Image, output_path: str = None) -> None:
    """
    Plota a imagem original, em escala de cinza e a negativa.

    Args:
        original: A imagem original (pode ser colorida ou cinza).
        gray: A imagem em escala de cinza.
        negative: A imagem negativa (em escala de cinza).
        output_path: Caminho opcional para salvar o plot.
    """
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.imshow(original)
    plt.title('Imagem Original')
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.imshow(gray, cmap='gray', vmin=0, vmax=255)
    plt.title('Imagem em Escala de Cinza')
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.imshow(negative, cmap='gray', vmin=0, vmax=255)
    plt.title('Imagem Negativa')
    plt.axis('off')

    plt.tight_layout()
    if output_path:
        try:
            plt.savefig(output_path)
            print(f"Plot salvo em '{output_path}'")
        except Exception as e:
            print(f"Erro ao salvar o plot em '{output_path}': {e}")
    plt.show()

def negative_transform(image: Image.Image) -> Image.Image:
    """
    Aplica a transformação negativa a uma imagem em escala de cinza.

    Args:
        image: A imagem PIL em escala de cinza.

    Returns:
        A imagem negativa.
    """
    if image.mode != 'L':
        print("Atenção: A imagem de entrada para a transformação negativa não está em escala de cinza. Convertendo...")
        image = image.convert('L')
    
    image_array = np.array(image, dtype=np.uint8)
    negative_array = 255 - image_array
    return Image.fromarray(negative_array)

if __name__ == '__main__':
    # Diretório de entrada e saída
    input_dir = "/home/andre/dev/processamento_de_imagens_2024-2/3"
    output_dir = os.path.join(input_dir, "resultados_negativa")
    
    # Cria o diretório de saída se não existir
    os.makedirs(output_dir, exist_ok=True)

    # Nome do arquivo de imagem de entrada
    input_image_name = "alvorada.jpg" # Ou "canoas.jpg", "museu.jpg", "ponte_jk.jpg"
    input_image_path = os.path.join(input_dir, input_image_name)

    print(f"Processando a imagem: {input_image_path}")

    original_image = load_image(input_image_path)

    if original_image:
        try:
            # Converte para escala de cinza
            gray_image = rgb_to_gray(original_image.copy()) # Usar .copy() se original_image for usada depois sem alterações

            # Aplica a transformação negativa
            negative_image = negative_transform(gray_image)

            # Define os nomes dos arquivos de saída
            base_name = os.path.splitext(input_image_name)[0]
            gray_output_path = os.path.join(output_dir, f"{base_name}_gray.jpg")
            negative_output_path = os.path.join(output_dir, f"{base_name}_negative.jpg")
            plot_output_path = os.path.join(output_dir, f"{base_name}_comparison_plot.png")

            # Salva as imagens processadas
            gray_image.save(gray_output_path)
            print(f"Imagem em escala de cinza salva em '{gray_output_path}'")
            
            negative_image.save(negative_output_path)
            print(f"Imagem negativa salva em '{negative_output_path}'")

            # Plota e salva as três imagens
            plot_images(original_image, gray_image, negative_image, plot_output_path)
            
            print("Processamento concluído com sucesso.")

        except Exception as e:
            print(f"Ocorreu um erro durante o processamento da imagem '{input_image_name}': {e}")
    else:
        print(f"Não foi possível carregar a imagem '{input_image_name}'. Encerrando o script.")
