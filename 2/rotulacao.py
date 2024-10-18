import numpy as np
from PIL import Image

def to_binary_image(image_path, threshold=128):
    # Converte uma imagem colorida em uma imagem binária usando um limiar.
    image = Image.open(image_path).convert('L')
    binary_image = np.array(image.point(lambda x: 0 if x < threshold else 255))
    return binary_image

def save_binary_image(binary_image, output_path):
    # Salva uma imagem binária como um arquivo de imagem.
    image = Image.fromarray(binary_image.astype(np.uint8))
    image.save(output_path)

def save_binary_matrix(binary_image, output_path):
    # Salva uma imagem binária como uma matriz binária em um arquivo de texto
    binary_image = np.where(binary_image == 0, '0', '1')
    np.savetxt(output_path, binary_image, fmt='%s')

def label_objects(binary_image):
    # Cria uma matriz para armazenar os rótulos, com o mesmo tamanho da imagem binária e tipo int
    labels = np.zeros_like(binary_image, dtype=int)
    label = 1  # Inicializa o primeiro rótulo como 1 (zero é considerado fundo)
    equivalences = {}  # Dicionário para rastrear equivalências de rótulos

    # Primeira passagem para rotular e armazenar equivalências
    for i in range(binary_image.shape[0]):
        for j in range(binary_image.shape[1]):
            # Verifica se o pixel faz parte de um objeto (valor 255 indica objeto)
            if binary_image[i, j] == 255:
                adjacent_labels = []  # Lista para armazenar rótulos dos vizinhos

                # Verifica o vizinho acima
                if i > 0 and labels[i-1, j] > 0:
                    adjacent_labels.append(labels[i-1, j])

                # Verifica o vizinho à esquerda
                if j > 0 and labels[i, j-1] > 0:
                    adjacent_labels.append(labels[i, j-1])

                # Se não houver vizinhos rotulados, cria um novo rótulo
                if not adjacent_labels:
                    labels[i, j] = label  # Atribui um novo rótulo ao pixel atual
                    label += 1  # Incrementa o rótulo para o próximo objeto

                # Caso contrário, usa o menor rótulo adjacente e armazena equivalências
                else:
                    min_label = min(adjacent_labels)  # Encontra o menor rótulo adjacente
                    labels[i, j] = min_label  # Atribui o menor rótulo ao pixel atual

                    # Armazena equivalências entre o menor rótulo e outros rótulos adjacentes
                    for adj_label in adjacent_labels:
                        if adj_label != min_label:  # Apenas para rótulos diferentes do mínimo
                            if adj_label in equivalences:
                                equivalences[adj_label].add(min_label)
                            else:
                                equivalences[adj_label] = {min_label}

    # Segunda passagem para resolver equivalências de rótulos
    for i in range(binary_image.shape[0]):
        for j in range(binary_image.shape[1]):
            # Se o rótulo atual tem equivalências, substitui pelo menor rótulo equivalente
            if labels[i, j] in equivalences:
                min_equiv = min(equivalences[labels[i, j]])  # Menor rótulo equivalente
                labels[i, j] = min_equiv  # Atualiza o rótulo para consolidar as equivalências

    return labels  # Retorna a matriz de rótulos

if __name__ == '__main__':
    # Carrega a imagem.
    input_path = '/home/andre/dev/processamento_de_imagens_2024-2/2/olho.jpg'

    # Converte a imagem colorida em uma imagem binária.
    binary_image = to_binary_image(input_path)

    # Rotula os objetos na imagem binária.
    labeled_image = label_objects(binary_image)

    # Salva a imagem binária como um arquivo de imagem.
    output_image_path = '/home/andre/dev/processamento_de_imagens_2024-2/2/rotulacao.jpg'
    save_binary_image(binary_image, output_image_path)

    # Salva a matriz binária em um arquivo de texto.
    output_matrix_path = '/home/andre/dev/processamento_de_imagens_2024-2/2/rotulacao_matrix.txt'
    save_binary_matrix(binary_image, output_matrix_path)
