from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def load_image(image_path):
    """
    Função para carregar a imagem e já convertê-la para escala de cinza.
    """
    img = Image.open(image_path).convert('L')  # Converte a imagem para tons de cinza
    return np.array(img)  # Retorna a imagem como array

def filtro_media(image_array, size):
    """
    Função para aplicar o filtro da média em uma imagem dada (como array).
    """
    height, width = image_array.shape # Obtém as dimensões da imagem
    margin = size // 2 # Calcula a margem para a janela de tamanho 'size'

    # Cria uma nova imagem filtrada com o mesmo tamanho da original
    filtered_image = np.zeros_like(image_array)

    # Aplica o filtro da média (com a janela 3x3) para cada pixel da imagem (exceto bordas)
    for x in range(margin, width - margin): 
        for y in range(margin, height - margin):
            total = 0
            count = 0
            # Itera sobre todos os vizinhos dentro da janela de tamanho 'size'
            for i in range(-margin, margin + 1):
                for j in range(-margin, margin + 1):
                    if 0 <= x + i < width and 0 <= y + j < height:
                        total += int(image_array[y + j, x + i])  # Soma os pixels vizinhos
                        count += 1  # Conta o número de pixels na vizinhança
            # Atribui a média à posição atual do pixel
            filtered_image[y, x] = total // count

    # Tratamento das bordas (Replicação dos valores adjacentes)
    # Trata as bordas superiores e inferiores
    for x in range(width):
        filtered_image[0, x] = image_array[0, x]  # Replicando o valor da primeira linha
        filtered_image[height - 1, x] = image_array[height - 1, x]  # Replicando o valor da última linha

    # Trata as bordas laterais
    for y in range(height):
        filtered_image[y, 0] = image_array[y, 0]  # Replicando o valor da primeira coluna
        filtered_image[y, width - 1] = image_array[y, width - 1]  # Replicando o valor da última coluna

    return filtered_image

if __name__ == '__main__':
    # Caminho para a imagem carregada:
    image_path = "/home/andre/dev/processamento_de_imagens_2024-2/5/marisa.jpg"

    # Carrega a imagem em escala de cinza
    image_array = load_image(image_path)

    # Aplica o filtro da média (tamanho da máscara 3x3)
    filtered_image = filtro_media(image_array, size=3)

    # Salva a imagem em tons de cinza
    Image.fromarray(image_array).save("/home/andre/dev/processamento_de_imagens_2024-2/5/media_marisa_gray.jpg")

    # Converte o array filtrado de volta para imagem e salva
    Image.fromarray(filtered_image.astype(np.uint8)).save("/home/andre/dev/processamento_de_imagens_2024-2/5/media_marisa_filtered.jpg")
