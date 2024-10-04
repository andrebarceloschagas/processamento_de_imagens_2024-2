import matplotlib.pyplot as plt
from PIL import Image

def load_image(file_path):
    """
    Função para carregar a imagem a partir do caminho do arquivo.
    """
    return Image.open(file_path)  # Abre e retorna a imagem

def plot_images(original, gray, equalized):
    """
    Função para plotar a imagem original, em escala de cinza e equalizada.
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

    # Imagem equalizada
    plt.subplot(1, 3, 3)
    plt.imshow(equalized, cmap='gray')
    plt.title('Imagem Equalizada')
    plt.axis('off')

    # Mostra as imagens
    plt.show()

def monta_histograma(image):
    """
    Monta o histograma da imagem em escala de cinza.
    """
    hist = [0] * 256  # Inicializa o histograma com 256 níveis.
    largura, altura = image.size  # Obtém a largura e altura da imagem.

    # Itera sobre os pixels da imagem e atualiza o histograma.
    for i in range(largura):
        for j in range(altura):
            pixel = image.getpixel((i, j))  # Obtém o valor do pixel.
            hist[pixel] += 1  # Incrementa o valor correspondente no histograma.

    return hist  # Retorna o histograma.

def soma_hist_normalizado(hist):
    """
    Calcula a soma acumulada normalizada do histograma (CDF).
    """
    s = sum(hist)  # Soma total de todos os valores do histograma.
    hist_norm = [0] * 256  # Inicializa o histograma normalizado.
    acumulado = 0  # Variável para armazenar a soma acumulada.

    # Calcula a soma acumulada normalizada.
    for i in range(256):
        acumulado += hist[i]
        hist_norm[i] = acumulado / s  # Normaliza pela soma total.

    return hist_norm  # Retorna a soma normalizada (CDF).

def criacao_lut(hist_norm):
    """
    Cria a LUT (Look-Up Table) com base no histograma normalizado (CDF).
    """
    lut = [0] * 256  # Inicializa a LUT.
    for i in range(256):
        lut[i] = int(hist_norm[i] * 255)  # Mapeia os valores da CDF para o intervalo [0, 255].

    return lut  # Retorna a LUT.

def equalizacao_histograma(image):
    """
    Aplica a equalização de histograma na imagem.
    """
    hist = monta_histograma(image)  # Calcula o histograma da imagem em tons de cinza.
    hist_norm = soma_hist_normalizado(hist)  # Normaliza o histograma.
    lut = criacao_lut(hist_norm)  # Chama a função de criação da LUT.
    return image.point(lut)  # Aplica a LUT à imagem e retorna a imagem equalizada.

if __name__ == '__main__':
    # Caminho para a imagem de entrada
    input_image_path = "/home/andre/desenvolvimento/processamento_de_imagens_2024-2/4/ponte_jk.jpg"

    # Carrega a imagem original
    original_image = load_image(input_image_path)

    # Converte para escala de cinza
    gray_image = original_image.convert('L')

    # Aplica a equalização de histograma
    equalized_image = equalizacao_histograma(gray_image)

    # Plota as três imagens
    plot_images(original_image, gray_image, equalized_image)

    # Salva a imagem em escala de cinza

    gray_image.save("/home/andre/desenvolvimento/processamento_de_imagens_2024-2/4/imagem_cinza.jpg")

    # Salva a imagem equalizada
    equalized_image.save("/home/andre/desenvolvimento/processamento_de_imagens_2024-2/4/imagem_eq.jpg")