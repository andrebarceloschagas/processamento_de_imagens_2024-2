# Abertura e Fechamento

from PIL import Image
import numpy as np

def abertura(image, element):
    # Aplica a operação de erosão seguida de dilatação
    eroded = erosao(image, element)
    opened = dilatacao(eroded, element)

    return opened


def fechamento(image, element):
    # Aplica a operação de dilatação seguida de erosão
    dilated = dilatacao(image, element)
    closed = erosao(dilated, element)

    return closed


def erosao(image, element):
    width, height = image.shape

    # Cria uma imagem de saída com o mesmo tamanho da imagem original
    output = np.zeros_like(image)

    # Inverte o elemento estruturante para realizar a operação de erosão
    inverted_element = np.logical_not(element)

    # Percorre todos os pixels da imagem
    for x in range(1, width-1):
        for y in range(1, height-1):
            # Verifica se o pixel é maior que 0 (branco)
            if image[x, y] > 0:
                # Verifica se todos os pixels do elemento estruturante são maiores que 0 na vizinhança
                if np.all(image[x - 1:x + 2, y - 1:y + 2] * inverted_element == 0):
                    output[x, y] = 0  # Define o pixel como 0 na imagem de saída

    return output


def dilatacao(image, element):
    width, height = image.shape

    # Cria uma imagem de saída com o mesmo tamanho da imagem original
    output = np.zeros_like(image)

    # Percorre todos os pixels da imagem
    for x in range(1, width-1):
        for y in range(1, height-1):
            # Verifica se o pixel é maior que 0 (branco)
            if image[x, y] > 0:
                # Sobrepõe o elemento estruturante na vizinhança do pixel
                output[x - 1:x + 2, y - 1:y + 2] = np.logical_or(output[x - 1:x + 2, y - 1:y + 2], element)

    return output


if __name__ == '__main__':
    # Exemplo de uso
    image_path = '/mnt/3ACCDBA5CCDB59A9/one/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/6/abertura_fechamento/image.jpg'
    element = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=np.uint8)  # Defina o elemento estruturante desejado

    # Abre a imagem e converte para escala de cinza
    image = Image.open(image_path).convert('L')

    # Converte a imagem para um array numpy
    img_array = np.array(image)

    # Converte a imagem para uma imagem binária
    img_binary = np.where(img_array < 128, 1, 0)

    # Aplica a abertura na imagem binária
    opened_image = abertura(img_binary, element)
    opened_image = Image.fromarray((opened_image * 255).astype(np.uint8))
    opened_image.save('/mnt/3ACCDBA5CCDB59A9/one/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/6/abertura_fechamento/image_abertura.jpg')

    # Aplica o fechamento na imagem binária
    closed_image = fechamento(img_binary, element)
    closed_image = Image.fromarray((closed_image * 255).astype(np.uint8))
    closed_image.save('/mnt/3ACCDBA5CCDB59A9/one/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/6/abertura_fechamento/image_fechamento.jpg')
















'''
from PIL import Image
import numpy as np


def abertura(image, element):
    # Aplica a operação de erosão seguida de dilatação
    eroded = erosao(image, element)
    opened = dilatacao(eroded, element)

    return opened


def fechamento(image, element):
    # Aplica a operação de dilatação seguida de erosão
    dilated = dilatacao(image, element)
    closed = erosao(dilated, element)

    return closed


def erosao(image, element):
    width, height = image.shape

    # Cria uma imagem de saída com o mesmo tamanho da imagem original
    output = np.zeros_like(image)

    # Inverte o elemto estruturante para realizar a operação de erosão
    inverted_element = np.logical_not(element)

    # Percorre todos os pixels da imagem
    for x in range(width):
        for y in range(height):
            # Verifica se o pixel é 1
            if image[x, y] == 1:
                # Verifica se todos os pixels do kernel são 1 na vizinhança
                if np.all(image[x - 1:x + 2, y - 1:y + 2] * inverted_element == 0):
                    output[x, y] = 0  # Define o pixel como 0 na imagem de saída
            else:
                output[x, y] = 0  # Define o pixel como 0 na imagem de saída

    return output


def dilatacao(image, element):
    width, height = image.shape

    # Cria uma imagem de saída com o mesmo tamanho da imagem original
    output = np.zeros_like(image)

    # Percorre todos os pixels da imagem
    for x in range(width):
        for y in range(height):
            # Verifica se o pixel é 1
            if image[x, y] == 1:
                # Sobrepoem o kernel na vizinhança do pixel
                output[x - 1:x + 2, y - 1:y + 2] = np.logical_or(output[x - 1:x + 2, y - 1:y + 2], element)

    return output


if __name__ == '__main__':
    # Exemplo de uso
    image_path = '/mnt/3ACCDBA5CCDB59A9/one/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/6/abertura_fechamento/erosao.jpg'
    element = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=np.uint8)  # Defina o kernel desejado

    # Abre a imagem e converte para escala de cinza
    image = Image.open(image_path).convert('L')

    # Converte a imagem para um array numpy
    img_array = np.array(image)

    # Converte a imagem para uma imagem binária
    img_binary = np.where(img_array < 128, 0, 1)

    # Aplica a abertura na imagem binária
    opened_image = abertura(img_binary, element)
    opened_image = Image.fromarray((opened_image * 255).astype(np.uint8))
    opened_image.save('/mnt/3ACCDBA5CCDB59A9/one/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/6/abertura_fechamento/imagem_abertura.jpg')

    # Aplica o fechamento na imagem binária
    closed_image = fechamento(img_binary, element)
    closed_image = Image.fromarray((closed_image * 255).astype(np.uint8))
    closed_image.save('/mnt/3ACCDBA5CCDB59A9/one/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/6/abertura_fechamento/imagem_fechamento.jpg')
'''