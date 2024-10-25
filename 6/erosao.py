from PIL import Image
import numpy as np


def erosao(image, element):
    """
    Função para realizar a erosão em uma imagem em tons de cinza usando um elemento estruturante.
    """
    width, height = image.shape # Dimensões da imagem original
    elem_width, elem_height = element.shape  # Dimensão do elemento estruturante aplicado a imagem
    margin_x = elem_width // 2 # Margem para percorrer a imagem na horizontal
    margin_y = elem_height // 2 # Margem para percorrer a imagem na vertical

    eroded = np.zeros_like(image) # Cria uma imagem de saída com o mesmo tamanho da imagem original

    # Percorre todos os pixels da imagem:
    for x in range(margin_x, width - margin_x):
        for y in range(margin_y, height - margin_y):
            # Define uma região da imagem com o tamanho do elemento estruturante
            region = image[x - margin_x:x + margin_x + 1, y - margin_y:y + margin_y + 1] # 

            # Aplica a operação de erosão: pega o valor mínimo onde o elemento estruturante é 1
            min_value = np.min(region[element == 1])

            # Atribui o valor mínimo na imagem de saída
            eroded[x, y] = min_value

    return eroded


if __name__ == '__main__':
    # Carrega a imagem original:
    image_path = '/home/andre/dev/processamento_de_imagens_2024-2/6/teste.png'

    # Defina o elemento estruturante desejado:
    element = np.array([[0, 1, 0],
                        [1, 1, 1],
                        [0, 1, 0]], dtype=np.uint8)

    # Abre a imagem e converte para escala de cinza:
    image = Image.open(image_path).convert('L')

    # Converte a imagem para um array numpy:
    img_array = np.array(image)

    # Aplica a operação de erosão:
    eroded_image = erosao(img_array, element)

    # Converte o array resultante de volta para uma imagem:
    eroded_image = Image.fromarray(eroded_image.astype(np.uint8))

    # Salva a imagem erodida:
    eroded_image.save('/home/andre/dev/processamento_de_imagens_2024-2/6/image_e.png')
