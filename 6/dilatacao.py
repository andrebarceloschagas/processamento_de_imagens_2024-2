from PIL import Image
import numpy as np


def dilatacao(image, element):
    """
    Função para realizar a dilatação em uma imagem em tons de cinza usando um elemento estruturante.
    """
    width, height = image.shape  # Dimensões da imagem original
    elem_width, elem_height = element.shape  # Dimensão do elemento estruturante aplicado à imagem
    margin_x = elem_width // 2  # Margem para percorrer a imagem na horizontal
    margin_y = elem_height // 2  # Margem para percorrer a imagem na vertical

    dilated = np.zeros_like(image)  # Cria uma imagem de saída com o mesmo tamanho da imagem original

    # Percorre todos os pixels da imagem:
    for x in range(margin_x, width - margin_x):
        for y in range(margin_y, height - margin_y):
            # Define uma região da imagem com o tamanho do elemento estruturante
            region = image[x - margin_x:x + margin_x + 1, y - margin_y:y + margin_y + 1]

            # Aplica a operação de dilatação: pega o valor máximo onde o elemento estruturante é 1
            max_value = np.max(region[element == 1])

            # Atribui o valor máximo na imagem de saída
            dilated[x, y] = max_value

    return dilated


if __name__ == '__main__':
    # Carrega a imagem original:
    image_path = '/home/andre/dev/processamento_de_imagens_2024-2/6/teste.png'

    # Defina o elemento estruturante desejado:
    element = np.array([[1, 1, 1],
                        [1, 1, 1],
                        [1, 1, 1]], dtype=np.uint8)

    # Abre a imagem e converte para escala de cinza:
    image = Image.open(image_path).convert('L')

    # Converte a imagem para um array numpy:
    img_array = np.array(image)

    # Aplica a operação de dilatação:
    dilated_image = dilatacao(img_array, element)

    # Converte o array resultante de volta para uma imagem:
    dilated_image = Image.fromarray(dilated_image.astype(np.uint8))

    # Salva a imagem dilatada:
    dilated_image.save('/home/andre/dev/processamento_de_imagens_2024-2/6/image_d.png')
