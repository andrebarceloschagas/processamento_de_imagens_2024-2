from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def plot_images(original, eroded, dilated, opened, closed):
    """
    Função para plotar a imagem original, a imagem erodida, a imagem dilatada,
    a imagem após abertura e a imagem após fechamento.
    """
    plt.figure(figsize=(15, 5))

    # Imagem original em escala de cinza
    plt.subplot(1, 5, 1)
    plt.imshow(original, cmap='gray')
    plt.title('Imagem Original')
    plt.axis('off')

    # Imagem erodida
    plt.subplot(1, 5, 2)
    plt.imshow(eroded, cmap='gray')
    plt.title('Imagem Erodida')
    plt.axis('off')

    # Imagem dilatada
    plt.subplot(1, 5, 3)
    plt.imshow(dilated, cmap='gray')
    plt.title('Imagem Dilatada')
    plt.axis('off')

    # Imagem abertura
    plt.subplot(1, 5, 4)
    plt.imshow(opened, cmap='gray')
    plt.title('Abertura')
    plt.axis('off')

    # Imagem fechamento
    plt.subplot(1, 5, 5)
    plt.imshow(closed, cmap='gray')
    plt.title('Fechamento')
    plt.axis('off')

    # Mostra as imagens
    plt.show()

def binarize_image(image_array, threshold=128):
    """
    Converte uma imagem em escala de cinza para binária (0 ou 1) com base em um valor de limiar.
    """
    return np.where(image_array >= threshold, 1, 0)

def morphological_operation(image, element, operation):
    """
    Função genérica para realizar operações morfológicas (erosão ou dilatação) em uma imagem binária.
    A operação pode ser 'min' (erosão) ou 'max' (dilatação).
    """
    width, height = image.shape
    elem_width, elem_height = element.shape
    margin_x = elem_width // 2
    margin_y = elem_height // 2

    result = np.zeros_like(image)

    for x in range(margin_x, width - margin_x):
        for y in range(margin_y, height - margin_y):
            region = image[x - margin_x:x + margin_x + 1, y - margin_y:y + margin_y + 1]
            
            if operation == 'min':
                result[x, y] = np.min(region[element == 1]) 
            elif operation == 'max':
                result[x, y] = np.max(region[element == 1])

    return result

def erosao(image, element):
    return morphological_operation(image, element, 'min')

def dilatacao(image, element):
    return morphological_operation(image, element, 'max')

def abertura(image, element):
    """
    Função para realizar a abertura em uma imagem.
    Abertura é a erosão seguida de dilatação.
    """
    eroded = erosao(image, element) 
    opened = dilatacao(eroded, element)
    return opened # Remove pequenos objetos e ruídos, útil para limpar a imagem

def fechamento(image, element):
    """
    Função para realizar o fechamento em uma imagem.
    Fechamento é a dilatação seguida de erosão.
    """
    dilated = dilatacao(image, element)
    closed = erosao(dilated, element)
    return closed # Preenche buracos e lacunas, útil para conectar componentes disjuntos

def save_image(image_array, file_path):
    """
    Função para salvar uma imagem binária como arquivo PNG.
    """
    Image.fromarray(image_array.astype(np.uint8) * 255).save(file_path) # Multiplica por 255 para converter de 0-1 para 0-255

if __name__ == '__main__':
    # Carrega a imagem original:
    image_path = '/home/andre/dev/processamento_de_imagens_2024-2/6/image.png'

    # Definir o elemento estruturante desejado:
    element = np.array([[1, 1, 1],
                        [1, 1, 1],
                        [1, 1, 1]], dtype=np.uint8)

    # Abre a imagem e converte para escala de cinza:
    image = Image.open(image_path).convert('L')

    # Converte a imagem para um array numpy:
    img_array = np.array(image)

    # Binariza a imagem
    binary_image = binarize_image(img_array)

    # Aplica a operação de erosão:
    eroded_image = erosao(binary_image, element)

    # Aplica a dilatação na imagem:
    dilated_image = dilatacao(binary_image, element)

    # Aplica a operação de abertura:
    opened_image = abertura(binary_image, element)

    # Aplica a operação de fechamento:
    closed_image = fechamento(binary_image, element)

    # Salva as imagens resultantes:
    save_image(eroded_image, '/home/andre/dev/processamento_de_imagens_2024-2/6/image_e.png')
    save_image(dilated_image, '/home/andre/dev/processamento_de_imagens_2024-2/6/image_d.png')
    save_image(opened_image, '/home/andre/dev/processamento_de_imagens_2024-2/6/image_opened.png')
    save_image(closed_image, '/home/andre/dev/processamento_de_imagens_2024-2/6/image_closed.png')

    # Plota as imagens original, erodida, dilatada, abertura e fechamento
    plot_images(binary_image, eroded_image, dilated_image, opened_image, closed_image)
