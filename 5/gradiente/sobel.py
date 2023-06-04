
from PIL import Image
import numpy as np

def filtro_gradiente(image_path):
    # Abre a imagem e converte para tons de cinza:
    image = Image.open(image_path).convert('L')
    width, height = image.size

    # Define as máscaras de Sobel para o gradiente em x e y:
    mask_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    mask_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

    # Cria uma nova imagem com o mesmo tamanho da original
    filtered_image = Image.new('L', (width, height))

    # Itera sobre todos os pixels da imagem:
    for x in range(1, width-1):
        for y in range(1, height-1):
            # Calcula o gradiente em x e y usando as máscaras de Sobel:
            gx = np.sum(mask_x * np.array([[image.getpixel((i, j)) for i in range(x-1, x+2)] for j in range(y-1, y+2)]))
            gy = np.sum(mask_y * np.array([[image.getpixel((i, j)) for i in range(x-1, x+2)] for j in range(y-1, y+2)]))

            # Calcula a magnitude do gradiente:
            magnitude = int(np.sqrt(gx**2 + gy**2))

            # Define o valor do pixel filtrado na nova imagem:
            filtered_image.putpixel((x, y), max(0, magnitude))

    return filtered_image

if __name__ == '__main__':
    # Exemplo de uso
    image_path = '/run/media/andre/arquivos/oneDrive/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/5/gradiente/marisa.jpg'
    filtered_image = filtro_gradiente(image_path)
    filtered_image.save('/run/media/andre/arquivos/oneDrive/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/5/gradiente/marisa_sobel.jpg')