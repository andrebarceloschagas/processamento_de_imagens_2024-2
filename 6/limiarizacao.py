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
    # Encontra os picos no histograma para limitar a busca do vale entre eles
    peak_indices = [i for i in range(1, len(histogram) - 1) if histogram[i - 1] < histogram[i] > histogram[i + 1]]

    if len(peak_indices) >= 2:
        # Considera apenas o primeiro e o segundo pico principais para buscar o vale entre eles
        left_peak, right_peak = peak_indices[0], peak_indices[1]

        # Busca o vale entre os dois picos principais
        vale = left_peak
        for i in range(left_peak, right_peak):
            if histogram[i] < histogram[vale]:
                vale = i
        return vale
    else:
        # Caso não encontre dois picos, usa um valor padrão
        return 128


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


def plot_images(original, binaria, histogram, vale):
    """
    Função para exibir a imagem original, a imagem binarizada e o histograma com o vale.
    """
    plt.figure(figsize=(15, 5))

    # Imagem original em cores
    plt.subplot(1, 3, 1)
    plt.imshow(original)
    plt.title("Imagem Original (Cores)")
    plt.axis("off")

    # Imagem binarizada
    plt.subplot(1, 3, 2)
    plt.imshow(binaria, cmap='gray')
    plt.title("Imagem Segmentada (Limiarização)")
    plt.axis("off")

    # Histograma com o vale marcado
    plt.subplot(1, 3, 3)
    plt.plot(histogram, color='black')
    plt.axvline(vale, color='red', linestyle='--', label=f'Vale (Limiar) = {vale}')
    plt.title("Histograma com Vale")
    plt.xlabel("Intensidade")
    plt.ylabel("Frequência")
    plt.legend()

    plt.show()


if __name__ == "__main__":
    # Carrega a imagem original em cores
    image_path = "/home/andre/dev/processamento_de_imagens_2024-2/6/18.png"  # Substitua pelo caminho da sua imagem
    original_image = Image.open(image_path)  # Carrega a imagem original em cores

    # Converte a imagem para escala de cinza para cálculo do histograma e limiarização
    gray_image = original_image.convert('L')

    # Calcula o histograma da imagem em escala de cinza
    histogram = monta_histograma(gray_image)

    # Encontra o limiar pelo método do vale
    limiar = encontrar_vale(histogram)
    print(f"Limiar encontrado: {limiar}")

    # Aplica a limiarização
    imagem_binaria = limiarizacao(gray_image, limiar)

    # Exibe a imagem original, a imagem segmentada e o histograma com o vale
    plot_images(original_image, imagem_binaria, histogram, limiar)

    # Salvar a imagem em escala de cinza
    gray_image.save("/home/andre/dev/processamento_de_imagens_2024-2/6/img_cinza.png")

    # Salvar a imagem resultante da limiarização
    imagem_binaria.save("/home/andre/dev/processamento_de_imagens_2024-2/6/img_limiar.png")
