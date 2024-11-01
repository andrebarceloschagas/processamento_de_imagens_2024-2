from PIL import Image
import numpy as np
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


def plot_images(original_image, gray_image, mirrored_image):
    """
    Função para plotar a imagem original colorida, em escala de cinza e a imagem espelhada.
    """
    plt.figure(figsize=(15, 5))

    # Imagem original colorida
    plt.subplot(1, 3, 1)
    plt.imshow(original_image)
    plt.title("Imagem Original Colorida")
    plt.axis("off")

    # Imagem em escala de cinza
    plt.subplot(1, 3, 2)
    plt.imshow(gray_image, cmap='gray')
    plt.title("Imagem em Escala de Cinza")
    plt.axis("off")

    # Imagem espelhada
    plt.subplot(1, 3, 3)
    plt.imshow(mirrored_image, cmap='gray')
    plt.title("Imagem Espelhada")
    plt.axis("off")

    plt.show()


def espelhamento_horizontal(image):
    """
    Função para realizar o espelhamento horizontal de uma imagem.
    """
    # Obtém as dimensões da imagem:
    altura, largura = image.shape

    # Cria uma imagem vazia com as mesmas dimensões da imagem original:
    result = np.zeros((altura, largura), dtype=np.uint8)

    # Percorre a imagem e copia os valores na imagem espelhada:
    for i in range(altura):  # Itera sobre cada linha da imagem
        for j in range(largura):  # Itera sobre cada coluna da imagem
            result[i, j] = image[i, largura - j - 1]  # Copia o valor do pixel da posição espelhada horizontalmente

    # Retorna a imagem espelhada:
    return result


if __name__ == '__main__':
    # Caminho para a imagem de entrada:
    input_image_path = "/home/andre/dev/processamento_de_imagens_2024-2/2/olho.jpg"

    # Carrega a imagem original colorida
    original_image = Image.open(input_image_path)

    # Carrega a imagem em escala de cinza:
    pixels = load_image(input_image_path, as_gray=True)

    # Chama a função de espelhamento:
    imagem_espelhada = espelhamento_horizontal(pixels)

    # Caminho para salvar a imagem espelhada:
    output_image_path = "/home/andre/dev/processamento_de_imagens_2024-2/2/resultado_olho.jpg"

    # Salva a imagem espelhada:
    save_image(imagem_espelhada, output_image_path)

    # Plota as imagens originais e a imagem resultante:
    plot_images(original_image, pixels, imagem_espelhada)
