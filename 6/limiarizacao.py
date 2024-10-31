from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def calcular_histograma(image_array):
    """
    Função para calcular o histograma de uma imagem em escala de cinza.
    """
    histogram, _ = np.histogram(image_array, bins=256, range=(0, 256))
    return histogram

def encontrar_vale(histogram):
    """
    Função para encontrar o vale no histograma, que será usado como limiar.
    """
    # Derivada do histograma para identificar picos e vales
    derivada = np.diff(histogram)
    
    # Encontra os índices onde há uma mudança de concavidade (vales)
    valleys = np.where((derivada[:-1] > 0) & (derivada[1:] < 0))[0] + 1
    
    # Escolhe o vale mais profundo
    if len(valleys) > 0:
        vale = valleys[np.argmin(histogram[valleys])]
    else:
        vale = 128  # Padrão se não houver vale claro
    
    return vale

def limiarizacao(image_array, limiar):
    """
    Função para aplicar a limiarização na imagem com base em um limiar dado.
    """
    binarized_image = np.where(image_array < limiar, 0, 255)
    return binarized_image.astype(np.uint8)

def plot_image(original, binaria):
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
    image_path = '/mnt/data/image.png'  # Substitua pelo caminho da sua imagem
    image = Image.open(image_path).convert('L')
    image_array = np.array(image)

    # Calcula o histograma da imagem
    histogram = calcular_histograma(image_array)

    # Encontra o limiar pelo método do vale
    limiar = encontrar_vale(histogram)
    print(f"Limiar encontrado: {limiar}")

    # Aplica a limiarização
    imagem_binaria = limiarizacao(image_array, limiar)

    # Exibe a imagem original e a imagem segmentada
    plot_image(image_array, imagem_binaria)
