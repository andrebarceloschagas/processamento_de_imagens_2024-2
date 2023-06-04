from PIL import Image
import numpy as np


def closing(image, kernel):
    # Converte a imagem para um array NumPy
    image_array = np.array(image)

    # Realiza a operação de dilatação
    dilated_image = dilation(image_array, kernel)

    # Realiza a operação de erosão na imagem dilatada
    closed_image = erosao(dilated_image, kernel)

    # Converte o array resultante novamente em uma imagem
    closed_image = Image.fromarray(closed_image)

    return closed_image


def erosao(image, kernel):
    width, height = image.shape

    # Cria uma imagem de saída com o mesmo tamanho da imagem original
    output = np.zeros_like(image)

    # Percorre todos os pixels da imagem
    for x in range(width):
        for y in range(height):
            # Obtém o valor mínimo na vizinhança definida pelo kernel
            min_value = np.min(image[max(0, x - 1):min(width, x + 2), max(0, y - 1):min(height, y + 2)])

            # Define o valor mínimo na imagem de saída
            output[x, y] = min_value

    return output


def dilatacao(image, element):
    width, height = image.shape

    # Cria uma imagem de saída com o mesmo tamanho da imagem original
    output = np.zeros_like(image)

    # Percorre todos os pixels da imagem
    for x in range(width):
        for y in range(height):
            # Obtém o valor máximo na vizinhança definida pelo kernel
            max_value = np.max(image[max(0, x - 1):min(width, x + 2), max(0, y - 1):min(height, y + 2)])

            # Define o valor máximo na imagem de saída
            output[x, y] = max_value

    return output

if __name__ == '__main__':
# Carrega a imagem binária
    image = Image.open("/mnt/3ACCDBA5CCDB59A9/one/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/6/abertura_fechamento/marisa.jpg").convert("L")  # Converte para escala de cinza

    # Define o kernel (elemento estruturante)
    element = np.array([[1, 0, 0],
                       [0, 1, 0],
                       [0, 0, 1]], dtype=np.uint8)

    # Aplica a operação de abertura na imagem
    closed_image = closing(image, element)

    # Exibe as imagens resultantes
    closed_image.save("/mnt/3ACCDBA5CCDB59A9/one/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/6/abertura_fechamento/marisa_f.jpg")
