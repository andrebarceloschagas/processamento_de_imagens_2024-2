from PIL import Image
import numpy as np

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


if __name__ == '__main__':
    # Exemplo de uso
    image_path = '/mnt/3ACCDBA5CCDB59A9/one/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/6/erosao_dilatacao/erosao.jpg'
    kernel = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=np.uint8)  # Defina o kernel desejado

    # Abre a imagem e converte para escala de cinza
    image = Image.open(image_path).convert('L')

    # Converte a imagem para um array numpy
    img_array = np.array(image)

    # Aplica a operação de erosão
    eroded_image = erosao(img_array, kernel)
    eroded_image = Image.fromarray(eroded_image.astype(np.uint8))
    eroded_image.save('/mnt/3ACCDBA5CCDB59A9/one/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/6/erosao_dilatacao/imagem_erosao.jpg')

