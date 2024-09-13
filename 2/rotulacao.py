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
    # Rotula objetos em uma imagem binária
    labels = np.zeros_like(binary_image)
    label = 1

    # Para cada pixel na imagem binária:
    for i in range(binary_image.shape[0]):
        for j in range(binary_image.shape[1]):
            # Se o pixel é parte de um objeto:
            if binary_image[i, j] == 255:
                # Encontra todos os pixels adjacentes ao pixel atual que já foram rotulados:
                adjacent_labels = []
                if i > 0 and labels[i-1, j] > 0:
                    adjacent_labels.append(labels[i-1, j])
                if j > 0 and labels[i, j-1] > 0:
                    adjacent_labels.append(labels[i, j-1])

                # Se nenhum pixel adjacente foi rotulado, crie um novo rótulo:
                if not adjacent_labels:
                    labels[i, j] = label
                    label += 1
                # Caso contrário, atribua o menor rótulo adjacente ao pixel atual:
                else:
                    adjacent_labels.sort()
                    labels[i, j] = adjacent_labels[0]

                    # Se houver mais de um rótulo adjacente, adiciona as equivalências de rótulo:
                    if len(adjacent_labels) > 1:
                        for k in range(1, len(adjacent_labels)):
                            equivalence = min(adjacent_labels[0], adjacent_labels[k])
                            labels = np.where(labels == adjacent_labels[k], equivalence, labels)

    return labels

if __name__ == '__main__':
    # Carrega a imagem.
    input_path = '/home/andre/processamento_de_imagens_2024-2/2/18_redux.png'

    # Converte a imagem colorida em uma imagem binária.
    binary_image = to_binary_image(input_path)

    # Rotula os objetos na imagem binária.
    labeled_image = label_objects(binary_image)

    # Salva a imagem binária como um arquivo de imagem.
    output_image_path = '/home/andre/processamento_de_imagens_2024-2/2/label_image.png'
    save_binary_image(binary_image, output_image_path)

    # Salva a matriz binária em um arquivo de texto.
    output_matrix_path = '/home/andre/processamento_de_imagens_2024-2/2/binary_matrix.txt'
    save_binary_matrix(binary_image, output_matrix_path)
