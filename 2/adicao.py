# Bibliotecas externas:
import numpy as np
from PIL import Image

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

def add(matrix1, matrix2):
    """
    Função para adicionar duas matrizes de pixels.
    Se a soma de dois pixels exceder 255, o valor será truncado para 255.
    """
    # Verifica se as matrizes possuem o mesmo tamanho:
    if matrix1.shape != matrix2.shape:
        raise ValueError("As matrizes devem ter o mesmo tamanho.")

    # Cria uma matriz vazia com o mesmo tamanho das matrizes de entrada:
    result = np.zeros_like(matrix1)

    # Percorre cada elemento das matrizes e realiza a operação de adição:
    for i in range(matrix1.shape[0]):
        for j in range(matrix1.shape[1]):
            soma = matrix1[i, j] + matrix2[i, j]
            if soma > 255:
                soma = 255  # Se a soma exceder 255, ajusta para o máximo permitido
            result[i, j] = soma  # Atribui o valor da soma ao resultado

    # Retorna a matriz resultado:
    return result

if __name__ == '__main__':
    # Caminhos para as imagens de entrada:
    image_path1 = "/home/andre/processamento_de_imagens_2024-2/2/19.png"
    image_path2 = "/home/andre/processamento_de_imagens_2024-2/2/14.png"
    
    # Carrega as imagens:
    image1 = load_image(image_path1)
    image2 = load_image(image_path2)

    # Converte as imagens para escala de cinza (se necessário):
    gray_image1 = rgb_to_gray(image1)
    gray_image2 = rgb_to_gray(image2)

    # Obtém os pixels das imagens:
    pixels1 = get_pixels(gray_image1)
    pixels2 = get_pixels(gray_image2)

    # Chama a função de adição:
    matrix_add = add(pixels1, pixels2)

    # Cria uma nova imagem com o resultado da adição:
    added_image = set_pixels(matrix_add)

    # Caminho para salvar a imagem resultante:
    output_image_path = "/home/andre/processamento_de_imagens_2024-2/2/adição.png"

    # Salva a nova imagem resultado:
    save_image(added_image, output_image_path)
