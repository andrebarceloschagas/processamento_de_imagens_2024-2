import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def load_image(file_path):
    """
    Função para carregar a imagem a partir do caminho do arquivo.
    """
    return Image.open(file_path)  # Abre e retorna a imagem

def rgb_to_gray(image):
    """
    Função para transformar a imagem em escala de cinza.
    """
    return image.convert('L')  # Converte a imagem para escala de cinza

def plot_images(original, gray, negative):
    """
    Função para plotar a imagem original, em escala de cinza e a negativa.
    """
    plt.figure(figsize=(12, 4))

    # Imagem original colorida
    plt.subplot(1, 3, 1)
    plt.imshow(original)
    plt.title('Imagem Original')
    plt.axis('off')

    # Imagem em escala de cinza
    plt.subplot(1, 3, 2)
    plt.imshow(gray, cmap='gray')
    plt.title('Imagem em Escala de Cinza')
    plt.axis('off')

    # Imagem negativa
    plt.subplot(1, 3, 3)
    plt.imshow(negative, cmap='gray')
    plt.title('Imagem Negativa')
    plt.axis('off')

    # Mostra as imagens
    plt.show()

def negative_transform(image):
    """
    Aplica a transformação negativa na imagem:
    A transformação negativa inverte os valores de pixel da imagem, 
    criando um efeito de negativo fotográfico. Para uma imagem em 
    tons de cinza, cada valor de pixel é subtraído do valor máximo 
    de cinza (255), resultando em uma nova imagem onde as áreas 
    claras se tornam escuras e vice-versa.
    """
    image_array = np.array(image)  # Converte a imagem para array
    max_gray_value = 255
    return Image.fromarray(max_gray_value - image_array)  # Aplica o negativo

if __name__ == '__main__':
    # Caminho para a imagem de entrada
    input_image_path = "/home/andre/desenvolvimento/processamento_de_imagens_2024-2/3/canoas.jpg"

    # Carrega a imagem original
    original_image = load_image(input_image_path)

    # Converte para escala de cinza
    gray_image = rgb_to_gray(original_image)

    # Aplica a transformação negativa
    negative_image = negative_transform(gray_image)

    # Salva as imagens em escala de cinza e negativa
    gray_image.save('/home/andre/desenvolvimento/processamento_de_imagens_2024-2/3/gray_image.jpg')
    negative_image.save('/home/andre/desenvolvimento/processamento_de_imagens_2024-2/3/negative_image.jpg')

    # Plota as três imagens
    plot_images(original_image, gray_image, negative_image)
