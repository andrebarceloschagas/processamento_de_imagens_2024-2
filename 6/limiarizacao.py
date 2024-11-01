from PIL import Image
import matplotlib.pyplot as plt

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

def encontrar_vale(histogram):
    """
    Encontra o vale no histograma, para ser utilizado como limiar.
    """
    # Derivada simples para identificar os vales
    derivada = [histogram[i + 1] - histogram[i] for i in range(len(histogram) - 1)]
    
    # Encontra os vales no histograma (mudanças de concavidade)
    valleys = []
    for i in range(1, len(derivada) - 1):
        if derivada[i - 1] > 0 and derivada[i] < 0:  # Mudança de sinal de positivo para negativo
            valleys.append(i)

    # Encontra o menor valor no histograma nos pontos de vale encontrados
    if valleys:
        vale = valleys[0]
        for v in valleys:
            if histogram[v] < histogram[vale]:
                vale = v
        return vale
    else:
        return 128  # Caso nenhum vale seja encontrado, usa o valor 128 como padrão.

def limiarizacao(image, limiar):
    """
    Aplica a limiarização na imagem com base em um limiar dado.
    """
    largura, altura = image.size
    binarizada = Image.new('L', (largura, altura))  # Cria uma nova imagem para armazenar a versão binária

    # Itera sobre os pixels da imagem para aplicar o limiar
    for i in range(largura):
        for j in range(altura):
            pixel = image.getpixel((i, j))
            if pixel < limiar:
                binarizada.putpixel((i, j), 0)  # Atribui 0 para os pixels abaixo do limiar
            else:
                binarizada.putpixel((i, j), 255)  # Atribui 255 para os pixels acima do limiar

    return binarizada

def plot_images(original, binaria):
    """
    Função para exibir a imagem original e a imagem binarizada.
    """
    plt.figure(figsize=(10, 5))

    # Imagem original
    plt.subplot(1, 2, 1)
    plt.imshow(original, cmap='gray')
    plt.title("Imagem Original")
    plt.axis("off")

    # Imagem binarizada
    plt.subplot(1, 2, 2)
    plt.imshow(binaria, cmap='gray')
    plt.title("Imagem Segmentada (Limiarização)")
    plt.axis("off")

    plt.show()

if __name__ == "__main__":
    # Carrega a imagem e converte para escala de cinza
    image_path = "/home/andre/dev/processamento_de_imagens_2024-2/6/museu.jpg"  # Substitua pelo caminho da sua imagem
    image = Image.open(image_path).convert('L')

    # Calcula o histograma da imagem
    histogram = monta_histograma(image)

    # Encontra o limiar pelo método do vale
    limiar = encontrar_vale(histogram)
    print(f"Limiar encontrado: {limiar}")

    # Aplica a limiarização
    imagem_binaria = limiarizacao(image, limiar)

    # Exibe a imagem original e a imagem segmentada
    plot_images(image, imagem_binaria)

    # Salvar a imagem em tons de cinza
    image.save("/home/andre/dev/processamento_de_imagens_2024-2/6/museu_cinza.jpg")  # Salvar a imagem em tons de cinza

    # Salvar a imagem binarizada

