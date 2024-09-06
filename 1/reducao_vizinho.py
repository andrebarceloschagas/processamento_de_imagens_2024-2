# Importando as bibliotecas necessárias
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

def reduce_by_nearest_neighbor(pixels):
    """
    Função para reduzir a imagem pela metade usando o método de vizinho mais próximo.
    Remove as linhas e colunas alternadas.
    """
    # Mantém apenas os pixels em índices pares
    reduced_pixels = pixels[::2, ::2]  # Seleciona apenas os pixels em índices pares
    return reduced_pixels  # Retorna o array de pixels reduzidos

if __name__ == '__main__':
    # Caminho do arquivo da imagem
    file_path = "/home/andre/desenvolvimento/processamento_de_imagens_2024-2/1/brat.jpeg"

    # Carregando a imagem
    image = load_image(file_path)  # Chama a função para carregar a imagem

    # Convertendo a imagem em escala de cinza
    gray_image = rgb_to_gray(image)  # Converte a imagem para escala de cinza

    # Obtendo os pixels da imagem em escala de cinza
    pixels = get_pixels(gray_image)  # Obtém os pixels da imagem em escala de cinza

    # Reduzindo a imagem utilizando vizinho mais próximo (removendo linhas e colunas)
    reduced_pixels = reduce_by_nearest_neighbor(pixels)  # Realiza a redução por vizinho mais próximo

    # Definindo os pixels na nova imagem
    new_image = set_pixels(reduced_pixels)  # Define os novos pixels na imagem

    # Salvando a nova imagem em um arquivo externo
    save_image(new_image, "/home/andre/desenvolvimento/processamento_de_imagens_2024-2/1/brate_reducao_vizinho.jpeg")  # Salva a nova imagem
    