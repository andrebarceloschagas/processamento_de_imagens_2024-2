import numpy as np
from PIL import Image

def find_root(label, equivalences):
    # Encontra a raiz de um rótulo (resolve equivalências)
    while equivalences[label] != label:
        label = equivalences[label]
    return label

def label_objects(image_path, threshold=128):
    # Carrega a imagem e converte para escala de cinza
    image = Image.open(image_path).convert('L')
    # Converte a imagem para binária usando um limiar (threshold)
    binary_image = np.array(image.point(lambda x: 0 if x < threshold else 255))

    # Inicializa a matriz de rótulos e o dicionário de equivalências
    labels = np.zeros_like(binary_image, dtype=int)
    equivalences = {}
    label = 1

    # Passo 1: Primeira passagem - rotulação e registro de equivalências
    for i in range(binary_image.shape[0]):
        for j in range(binary_image.shape[1]):
            if binary_image[i, j] == 255:  # Se o pixel faz parte de um objeto (pixel branco)
                # Obtenha os vizinhos r (esquerda) e s (acima)
                r = labels[i, j-1] if j > 0 else 0  # Vizinho à esquerda
                s = labels[i-1, j] if i > 0 else 0  # Vizinho acima

                if r == 0 and s == 0:
                    # Caso 2.1: r e s são 0, atribui um novo rótulo a p
                    labels[i, j] = label
                    equivalences[label] = label  # Cada novo rótulo é seu próprio representante
                    label += 1
                elif r != 0 and s == 0:
                    # Caso 2.2: Apenas r é rotulado
                    labels[i, j] = r
                elif r == 0 and s != 0:
                    # Caso 2.2: Apenas s é rotulado
                    labels[i, j] = s
                elif r != 0 and s != 0:
                    if r == s:
                        # Caso 2.3: r e s têm o mesmo rótulo
                        labels[i, j] = r
                    else:
                        # Caso 2.4: r e s têm rótulos diferentes, marcam-se como equivalentes
                        min_label = min(r, s)
                        max_label = max(r, s)
                        labels[i, j] = min_label
                        equivalences[max_label] = min_label

    # Passo 2: Segunda passagem - Trocar rótulos pelos seus equivalentes
    for i in range(binary_image.shape[0]):
        for j in range(binary_image.shape[1]):
            if labels[i, j] != 0:
                # Substitui cada rótulo pelo seu equivalente final (raiz)
                labels[i, j] = find_root(labels[i, j], equivalences)

    return labels

def save_labeled_image(labeled_image, output_path):
    # Converte a matriz de rótulos para uma imagem e salva
    labeled_image_normalized = (labeled_image / labeled_image.max()) * 255  # Normaliza os valores de rótulos para a faixa [0, 255]
    image = Image.fromarray(labeled_image_normalized.astype(np.uint8))
    image.save(output_path)

if __name__ == '__main__':
    # Caminho da imagem de entrada
    input_image_path = "/home/andre/processamento_de_imagens_2024-2/2/brat.jpeg"
    
    # Rotula os objetos na imagem
    labeled_image = label_objects(input_image_path)

    # Salva a imagem rotulada
    output_image_path = "/home/andre/processamento_de_imagens_2024-2/2/brat_label_image.jpeg"
    save_labeled_image(labeled_image, output_image_path)
