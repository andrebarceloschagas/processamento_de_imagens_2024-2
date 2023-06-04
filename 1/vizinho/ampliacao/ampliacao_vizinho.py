# Importando as bibliotecas necessárias
from PIL import Image
import numpy as np

def load_image(file_path):
    """
    Função para carregar a imagem a partir do caminho do arquivo.
    """
    img = Image.open(file_path)
    return img

def save_image(image, file_path):
    """
    Função para salvar a imagem em um arquivo externo.
    """
    image.save(file_path)

def get_pixels(image):
    """
    Função para obter os pixels da imagem.
    """
    pixels = np.array(image)
    return pixels

def set_pixels(pixels):
    """
    Função para definir os pixels em uma imagem.
    """
    image = Image.fromarray(pixels.astype('uint8'))
    return image

def rgb_to_gray(image):
    """
    Função para transformar a imagem em escala de cinza.
    """
    gray_image = image.convert('L')
    return gray_image

def nearest_neighbor_interpolation(pixels, new_size):
    """
    Função para realizar a interpolação por vizinho mais próximo.
    """
    height, width, channels = pixels.shape
    new_height, new_width = new_size
    h_ratio = new_height / height
    w_ratio = new_width / width
    new_pixels = np.zeros((new_height, new_width, channels), dtype=np.uint8)
    
    for i in range(new_height):
        for j in range(new_width):
            h_idx = int(i // h_ratio)
            w_idx = int(j // w_ratio)
            new_pixels[i,j,:] = pixels[h_idx,w_idx,:]
    return new_pixels

if __name__ == '__main__':
    # Caminho do arquivo da imagem
    file_path = "/run/media/andre/arquivos/oneDrive/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/1/ampliacao_vizinho/4.jpg"

    # Carregando a imagem
    image = load_image(file_path)

    # Convertendo a imagem em escala de cinza
    gray_image = rgb_to_gray(image)

    # Obtendo os pixels da imagem em escala de cinza
    pixels = get_pixels(gray_image)

    # Ampliando a imagem utilizando a interpolação por vizinho mais próximo
    new_size = (gray_image.size[0] * 2, gray_image.size[1] * 2)
    new_pixels = nearest_neighbor_interpolation(pixels, new_size)

    # Definindo os pixels na nova imagem
    new_image = set_pixels(new_pixels)

    # Salvando a nova imagem em um arquivo externo
    save_image(new_image, "/run/media/andre/arquivos/oneDrive/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/1/ampliacao_vizinho/new_image.jpg")
