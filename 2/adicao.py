# Bibliotecas externas:
import numpy as np
from PIL import Image

def load_image(file_path, as_gray=False):
    """
    Função para carregar a imagem a partir do caminho do arquivo.
    Se as_gray for True, converte a imagem para escala de cinza.
    """
    img = Image.open(file_path)  # Abre a imagem
    if as_gray:
        img = img.convert('L')  # Converte para escala de cinza, se necessário
    return np.array(img)  # Retorna os pixels da imagem como array numpy

def save_image(pixels, file_path):
    """
    Função para salvar a imagem (array de pixels) em um arquivo externo.
    """
    image = Image.fromarray(pixels.astype('uint8'))  # Converte o array para imagem
    image.save(file_path)  # Salva a imagem no caminho especificado

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
    image_path1 = "/home/andre/processamento_de_imagens_2024-2/2/8.png"
    image_path2 = "/home/andre/processamento_de_imagens_2024-2/2/12.png"
    
    # Carrega as imagens em escala de cinza:
    pixels1 = load_image(image_path1, as_gray=True)
    pixels2 = load_image(image_path2, as_gray=True)

    # Chama a função de adição:
    matrix_add = add(pixels1, pixels2)

    # Caminho para salvar a imagem resultante:
    output_image_path = "/home/andre/processamento_de_imagens_2024-2/2/adicao.png"

    # Salva a nova imagem resultado:
    save_image(matrix_add, output_image_path)
