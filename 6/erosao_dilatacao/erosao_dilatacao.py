# Erosão e Dilataçao

from PIL import Image
import numpy as np


def erosao(image, element):
    width, height = image.shape

    # Cria uma imagem de saída com o mesmo tamanho da imagem original:
    eroded = np.zeros_like(image)

    # Percorre todos os pixels da imagem:
    for x in range(width):
        for y in range(height):
            # Obtém o valor mínimo na vizinhança definida pelo elemento:
            min_value = np.min(image[max(0, x - 1):min(width, x + 2), max(0, y - 1):min(height, y + 2)])

            # Define o valor mínimo na imagem de saída:
            eroded[x, y] = min_value

    return eroded


def dilatacao(image, element):
    width, height = image.shape

    # Cria uma imagem de saída com o mesmo tamanho da imagem original:
    dilated = np.zeros_like(image)

    # Percorre todos os pixels da imagem:
    for x in range(width):
        for y in range(height):
            # Obtém o valor máximo na vizinhança definida pelo elemento:
            max_value = np.max(image[max(0, x - 1):min(width, x + 2), max(0, y - 1):min(height, y + 2)])

            # Define o valor máximo na imagem de saída:
            dilated[x, y] = max_value

    return dilated


if __name__ == '__main__':
    # Carrega a imagem original:
    image_path = '/mnt/3ACCDBA5CCDB59A9/one/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/6/erosao_dilatacao/image.png'
    element = np.array([[0, 1, 0],
                        [1, 1, 1],
                        [0, 1, 0]], dtype=np.uint8)  # Defina o elemento desejado.

    # Abre a imagem e converte para escala de cinza:
    image = Image.open(image_path).convert('L')

    # Converte a imagem para um array numpy:
    img_array = np.array(image)

    # Aplica a operação de erosão:
    eroded_image = erosao(img_array, element)
    eroded_image = Image.fromarray(eroded_image.astype(np.uint8))
    eroded_image.save('/mnt/3ACCDBA5CCDB59A9/one/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/6/erosao_dilatacao/image_e.png')

    # Aplica a operação de dilatação:
    dilated_image = dilatacao(img_array, element)
    dilated_image = Image.fromarray(dilated_image.astype(np.uint8))
    dilated_image.save('/mnt/3ACCDBA5CCDB59A9/one/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/6/erosao_dilatacao/image_d.png')
