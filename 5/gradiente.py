
from PIL import Image
import numpy as np

def sobel_filter(image_array, mask_x, mask_y):
    """
    Função para aplicar o filtro de Sobel em uma imagem.
    """
    height, width = image_array.shape
    margin = 1  # As máscaras Sobel são 3x3, portanto a margem é 1

    # Cria um array vazio para armazenar a imagem filtrada
    filtered_array = np.zeros((height, width), dtype=np.float32)

    # Aplica a convolução com as máscaras Sobel (x e y)
    for y in range(margin, height - margin):
        for x in range(margin, width - margin):
            # Convolução com máscara X
            gx = 0
            for j in range(-margin, margin + 1):
                for i in range(-margin, margin + 1):
                    gx += image_array[y + j, x + i] * mask_x[j + margin, i + margin]

            # Convolução com máscara Y
            gy = 0
            for j in range(-margin, margin + 1):
                for i in range(-margin, margin + 1):
                    gy += image_array[y + j, x + i] * mask_y[j + margin, i + margin]

            # Calcula a magnitude do gradiente
            magnitude = np.sqrt(gx ** 2 + gy ** 2)
            filtered_array[y, x] = magnitude

    # Normaliza a saída entre 0 e 255
    filtered_array = (filtered_array - filtered_array.min()) / (filtered_array.max() - filtered_array.min()) * 255 # Normaliza a saída entre 0 e 255


    return filtered_array.astype(np.uint8)

if __name__ == '__main__':
    # Define as máscaras de Sobel para o eixo X e Y
    mask_x = np.array([[-1, 0, 1],
                       [-2, 0, 2],
                       [-1, 0, 1]])

    mask_y = np.array([[-1, -2, -1],
                       [0, 0, 0],
                       [1, 2, 1]])

    # Carrega a imagem original
    image_path = "/home/andre/dev/processamento_de_imagens_2024-2/5/centavos.jpeg"
    original_image = Image.open(image_path)

    # Converte a imagem para escala de cinza
    image_gray = original_image.convert('L')
    image_array = np.array(image_gray)

    # Aplica o filtro de Sobel
    filtered_image_sobel = sobel_filter(image_array, mask_x, mask_y)

    # Salva a imagem em tons de cinza
    Image.fromarray(image_array).save("/home/andre/dev/processamento_de_imagens_2024-2/5/gradiente_centavos_gray.jpeg")

    # Salva a imagem filtrada com Sobel
    Image.fromarray(filtered_image_sobel).save("/home/andre/dev/processamento_de_imagens_2024-2/5/gradiente_sobel_filtered.jpeg")
