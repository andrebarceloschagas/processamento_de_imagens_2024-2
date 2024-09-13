# Bibliotecas externas:
from PIL import Image
import numpy as np

def load_image(file_path):
    """
    Função para carregar a imagem a partir do caminho do arquivo.
    """
    img = Image.open(file_path)  # Abre a imagem usando a biblioteca PIL
    return img  # Retorna a imagem carregada

def save_image(image, file_path):
    """
    Função para salvar a imagem em um arquivo externo.
    """
    image.save(file_path)  # Salva a imagem no caminho especificado

def get_pixels(image):
    """
    Função para obter os pixels da imagem.
    """
    pixels = np.array(image)  # Converte a imagem para um array numpy
    return pixels  # Retorna o array de pixels

def set_pixels(pixels):
    """
    Função para definir os pixels em uma imagem.
    """
    image = Image.fromarray(pixels.astype('uint8'))  # Converte o array de volta para uint8 e cria uma imagem
    return image  # Retorna a imagem criada a partir dos pixels

def rgb_to_gray(image):
    """
    Função para transformar a imagem em escala de cinza.
    """
    gray_image = image.convert('L')  # Converte a imagem para escala de cinza
    return gray_image  # Retorna a imagem em escala de cinza

def espelhamento_horizontal(image):
    """
    Função para realizar o espelhamento horizontal de uma imagem.
    """
    # Obtém as dimensões da imagem:
    altura, largura = image.shape
    
    # Cria uma imagem vazia com as mesmas dimensões da imagem original:
    result = np.zeros((altura, largura), dtype=np.uint8)
    
    # Percorre a imagem e copia os valores na imagem espelhada:
    for i in range(altura):  # Itera sobre cada linha da imagem
        for j in range(largura):  # Itera sobre cada coluna da imagem
            result[i, j] = image[i, largura - j - 1]  # Copia o valor do pixel da posição espelhada horizontalmente
    
    # Retorna a imagem espelhada:
    return result

if __name__ == '__main__':
    # Caminho para a imagem de entrada:
    input_image_path = "/home/andre/processamento_de_imagens_2024-2/2/olho.jpg"
    
    # Carrega a imagem:
    image = load_image(input_image_path)

    # Converte a imagem para escala de cinza (se necessário):
    gray_image = rgb_to_gray(image)

    # Obtém os pixels da imagem:
    pixels = get_pixels(gray_image)

    # Chama a função de espelhamento:
    imagem_espelhada = espelhamento_horizontal(pixels)

    # Converte o resultado para uma imagem:
    imagem_resultado = set_pixels(imagem_espelhada)

    # Caminho para salvar a imagem espelhada:
    output_image_path = "/home/andre/processamento_de_imagens_2024-2/2/resultado_olho.jpg"

    # Salva a imagem espelhada:
    save_image(imagem_resultado, output_image_path)
