from PIL import Image
import numpy as np


def segmentacao_limiarizacao_vale(image_path):
    # Carrega a imagem
    image = Image.open(image_path)

    # Converte a imagem para escala de cinza
    image_gray = image.convert('L')

    # Converte a imagem para um array numpy
    image_array = np.array(image_gray)

    # Calcula o histograma da imagem
    histogram = np.histogram(image_array, bins=256, range=(0, 256))

    # Encontra o vale no histograma
    valleys = np.argmin(histogram[0])

    # Define o valor de limiar como o valor do vale
    threshold = valleys

    # Aplica a limiarização
    segmented_image = np.where(image_array < threshold, 0, 255)

    # Cria uma nova imagem binária a partir do array numpy
    binary_image = Image.fromarray(segmented_image.astype(np.uint8))

    return binary_image

if __name__ == '__main__':
    # Exemplo de uso
    image_path = '/mnt/3ACCDBA5CCDB59A9/one/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/7/caneca-interior-vermelho-personalizada-min.png'
    binary_image = segmentacao_limiarizacao_vale(image_path)
    binary_image.save('/mnt/3ACCDBA5CCDB59A9/one/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/7/b.png')
