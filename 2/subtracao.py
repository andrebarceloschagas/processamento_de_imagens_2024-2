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

def subtract(matrix1, matrix2):
    """
    Função para subtrair duas matrizes de pixels.
    Se a subtração de dois pixels resultar em um valor menor que 0, será truncado para 0.
    """
    # Verifica se as matrizes possuem o mesmo tamanho:
    if matrix1.shape != matrix2.shape:
        raise ValueError("As matrizes devem ter o mesmo tamanho.")

    # Cria uma matriz vazia com o mesmo tamanho das matrizes de entrada:
    result = np.zeros_like(matrix1)

    # Percorre cada elemento das matrizes e realiza a operação de subtração:
    for i in range(matrix1.shape[0]):
        for j in range(matrix1.shape[1]):
            subtracao = matrix1[i, j] - matrix2[i, j]
            if subtracao < 0:
                subtracao = 0  # Se a subtração for negativa, ajusta para o mínimo permitido (0)
            result[i, j] = subtracao  # Atribui o valor da subtração ao resultado

    # Retorna a matriz resultado:
    return result

if __name__ == '__main__':
    # Caminhos para as imagens de entrada:
    image_path1 = "/home/andre/processamento_de_imagens_2024-2/2/8.png"
    image_path2 = "/home/andre/processamento_de_imagens_2024-2/2/12.png"
    
    # Carrega as imagens em escala de cinza:
    pixels1 = load_image(image_path1, as_gray=True)
    pixels2 = load_image(image_path2, as_gray=True)

    # Chama a função de subtração:
    matrix_subtract = subtract(pixels1, pixels2)

    # Caminho para salvar a imagem resultante:
    output_image_path = "/home/andre/processamento_de_imagens_2024-2/2/subtracao.png"

    # Salva a nova imagem resultado:
    save_image(matrix_subtract, output_image_path)
