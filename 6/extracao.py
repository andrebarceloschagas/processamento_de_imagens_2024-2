import cv2
import numpy as np


def abertura(image_path, kernel_size):
    # Carrega a imagem em escala de cinza
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Binariza a imagem
    _, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)

    # Cria o kernel para a operação de abertura
    kernel = np.ones((kernel_size, kernel_size), np.uint8)

    # Aplica a operação de abertura na imagem binária
    opened_image = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel)

    return opened_image


def fechamento(image_path, kernel_size):
    # Carrega a imagem em escala de cinza
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Binariza a imagem
    _, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)

    # Cria o kernel para a operação de fechamento
    kernel = np.ones((kernel_size, kernel_size), np.uint8)

    # Aplica a operação de fechamento na imagem binária
    closed_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)

    return closed_image


if __name__ == '__main__':
    # Exemplo de uso
    image_path = '/mnt/3ACCDBA5CCDB59A9/one/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/6/dilation.png'
    kernel_size = 3  # Tamanho do kernel (deve ser ímpar)

    # Aplica a abertura na imagem binária
    opened_image = abertura(image_path, kernel_size)
    cv2.imwrite('/mnt/3ACCDBA5CCDB59A9/one/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/6/imagem_abertura.png', opened_image)

    # Aplica o fechamento na imagem binária
    closed_image = fechamento(image_path, kernel_size)
    cv2.imwrite('/mnt/3ACCDBA5CCDB59A9/one/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/6/imagem_fechamento.png', closed_image)
