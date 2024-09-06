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

def nearest_neighbor_amplification(pixels, scale_factor):
    """
    Função para realizar a ampliação da imagem por vizinho mais próximo, replicando os pixels.
    """
    height, width = pixels.shape[:2]  # Obtém a altura e a largura da imagem original
    
    # Dimensões da nova imagem ampliada
    new_height = height * scale_factor  # Calcula a nova altura
    new_width = width * scale_factor  # Calcula a nova largura
    
    # Criar um novo array para os pixels ampliados
    new_pixels = np.zeros((new_height, new_width), dtype=np.uint8)  # Cria um array vazio para os novos pixels
    
    # Preenchendo a nova imagem duplicando os pixels
    for i in range(new_height):
        for j in range(new_width):
            new_pixels[i, j] = pixels[i // scale_factor, j // scale_factor]  # Copia o valor do pixel mais próximo
    
    return new_pixels  # Retorna o array de novos pixels ampliados

if __name__ == '__main__':
    # Caminho do arquivo da imagem
    file_path = "/home/andre/desenvolvimento/processamento_de_imagens_2024-2/1/brat.jpeg"

    # Carregando a imagem
    image = load_image(file_path)  # Chama a função para carregar a imagem

    # Convertendo a imagem em escala de cinza
    gray_image = rgb_to_gray(image)  # Converte a imagem para escala de cinza

    # Obtendo os pixels da imagem em escala de cinza
    pixels = get_pixels(gray_image)  # Obtém os pixels da imagem em escala de cinza

    # Ampliando a imagem utilizando a interpolação por vizinho mais próximo
    scale_factor = 2  # Fator de escala (duplicar a imagem)
    new_pixels = nearest_neighbor_amplification(pixels, scale_factor)  # Realiza a ampliação por vizinho mais próximo

    # Definindo os pixels na nova imagem
    new_image = set_pixels(new_pixels)  # Define os novos pixels na imagem

    # Salvando a nova imagem em um arquivo externo
    save_image(new_image, "/home/andre/desenvolvimento/processamento_de_imagens_2024-2/1/brat_ampliacao_vizinho.jpeg")  # Salva a nova imagem
    