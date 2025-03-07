import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


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


def plot_images(image1, image2, result_image):
    """
    Função para plotar as imagens originais e a imagem resultante da operação de adição.
    """
    plt.figure(figsize=(15, 5))

    # Primeira imagem
    plt.subplot(1, 3, 1)
    plt.imshow(image1, cmap='gray')
    plt.title("Imagem 1")
    plt.axis("off")

    # Segunda imagem
    plt.subplot(1, 3, 2)
    plt.imshow(image2, cmap='gray')
    plt.title("Imagem 2")
    plt.axis("off")

    # Imagem resultante (adicionada)
    plt.subplot(1, 3, 3)
    plt.imshow(result_image, cmap='gray')
    plt.title("Imagem Resultante (Adição)")
    plt.axis("off")

    plt.show()


def add(matrix1, matrix2):
    """
    Função para adicionar duas matrizes de pixels.
    Se a soma de dois pixels exceder 255, o valor será truncado para 255.
    """
    # Verifica se as matrizes possuem o mesmo tamanho:
    if matrix1.shape != matrix2.shape:
        raise ValueError("As matrizes devem ter o mesmo tamanho.")

    # Cria uma matriz vazia com o mesmo tamanho das matrizes de entrada:
    result = np.zeros_like(matrix1, dtype=int)  # Usa 'int' temporariamente para evitar overflow

    # Percorre cada elemento das matrizes e realiza a operação de adição:
    for i in range(matrix1.shape[0]):
        for j in range(matrix1.shape[1]):
            # Calcula a soma como inteiro para evitar overflow
            soma = int(matrix1[i, j]) + int(matrix2[i, j])
            # Limita a soma ao máximo permitido (255)
            if soma > 255:
                soma = 255
            result[i, j] = soma  # Atribui o valor da soma ao resultado

    # Converte o resultado de volta para uint8 antes de retornar
    return result.astype(np.uint8)


if __name__ == '__main__':
    # Caminhos para as imagens de entrada:
    image_path1 = "/home/andre/dev/processamento_de_imagens_2024-2/2/14.png"
    image_path2 = "/home/andre/dev/processamento_de_imagens_2024-2/2/19.png"

    # Carrega as imagens em escala de cinza:
    pixels1 = load_image(image_path1, as_gray=True)
    pixels2 = load_image(image_path2, as_gray=True)

    # Chama a função de adição:
    matrix_add = add(pixels1, pixels2)

    # Caminho para salvar a imagem resultante:
    output_image_path = "/home/andre/dev/processamento_de_imagens_2024-2/2/adicao.png"

    # Salva a nova imagem resultado:
    save_image(matrix_add, output_image_path)

    # Exibe as imagens originais e a imagem resultante:
    plot_images(pixels1, pixels2, matrix_add)
