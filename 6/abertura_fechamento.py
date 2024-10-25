# Abertura e Fechamento

from PIL import Image
import numpy as np


def abertura(image, element):
    # Converte a imagem para um array:
    image_array = np.array(image)

    # Realiza a operação de erosão:
    eroded_image = erosao(image_array, element)

    # Realiza a operação de dilatação na imagem erodida:
    opened_image = dilatacao(eroded_image, element)

    # Converte o array resultante novamente em uma imagem
    opened_image = Image.fromarray(opened_image)

    return opened_image


def fechamento(image, element):
    # Converte a imagem para um array:
    image_array = np.array(image)

    # Realiza a operação de dilatação:
    dilated_image = dilatacao(image_array, element)

    # Realiza a operação de erosão na imagem dilatada:
    closed_image = erosao(dilated_image, element)

    # Converte o array resultante novamente em uma imagem:
    closed_image = Image.fromarray(closed_image)

    return closed_image


def erosao(image, kernel):
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
    # Carrega a imagem:
    image = Image.open("/mnt/3ACCDBA5CCDB59A9/one/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/6/abertura_fechamento/image.png").convert("L")  # Converte para escala de cinza

    # Define o elemento estruturante:
    element = np.array([[0, 1, 0],
                        [1, 1, 1],
                        [0, 1, 0]], dtype=np.uint8)

    # Aplica a operação de abertura na imagem:
    opened_image = abertura(image, element)

    # Salva a imagem aberta:
    opened_image.save("/mnt/3ACCDBA5CCDB59A9/one/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/6/abertura_fechamento/image_a.png")

    # Aplica a operação de fechamento na imagem:
    closed_image = fechamento(image, element)

    # Salva a imagem fechada:
    closed_image.save("/mnt/3ACCDBA5CCDB59A9/one/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/6/abertura_fechamento/image_f.png")

