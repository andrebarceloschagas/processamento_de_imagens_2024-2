from PIL import Image
import numpy as np

def load_image(file_path):
    """
    Função para carregar a imagem a partir do caminho do arquivo.
    """
    img = Image.open(file_path)  # Abre a imagem usando a biblioteca PIL
    return img  # Retorna a imagem carregada

def save_image(image, file_path):
    """
    Função para salvar a imagem em um arquivo externo.
    """
    image.save(file_path)  # Salva a imagem no caminho especificado

def get_pixels(image):
    """
    Função para obter os pixels da imagem.
    """
    pixels = np.array(image)  # Converte a imagem para um array numpy
    return pixels  # Retorna o array de pixels

def set_pixels(pixels):
    """
    Função para definir os pixels em uma imagem.
    """
    # Se a imagem for em escala de cinza, manter o array 2D
    if len(pixels.shape) == 2:
        image = Image.fromarray(pixels.astype('uint8'), 'L')  # 'L' indica imagem em escala de cinza
    else:
        image = Image.fromarray(pixels.astype('uint8'))  # Para imagens RGB
    return image  # Retorna a imagem criada a partir dos pixels

def rgb_to_gray(image):
    """
    Função para transformar a imagem em escala de cinza.
    """
    gray_image = image.convert('L')  # Converte a imagem para escala de cinza
    return gray_image  # Retorna a imagem em escala de cinza

def bilinear_interpolation(pixels, new_size):
    """
    Função para realizar a interpolação bilinear para redução de imagem.
    """
    height, width = pixels.shape[:2]  # Obtém a altura e a largura da imagem original
    if len(pixels.shape) == 2:
        channels = 1  # Para imagens em escala de cinza
    else:
        channels = pixels.shape[2]  # Para imagens coloridas (RGB)
    
    new_height, new_width = new_size  # Define a nova altura e largura da imagem
    # Cria um array vazio para os novos pixels, com float32 para evitar overflow
    new_pixels = np.zeros((new_height, new_width, channels), dtype=np.float32) if channels > 1 else np.zeros((new_height, new_width), dtype=np.float32)

    for i in range(new_height):
        for j in range(new_width):
            # Encontrar as coordenadas dos pixels vizinhos
            h_idx = int(i * height / new_height)
            w_idx = int(j * width / new_width)
            h_idx_2 = min(h_idx + 1, height - 1)
            w_idx_2 = min(w_idx + 1, width - 1)

            # Pegar os quatro pixels vizinhos
            A = pixels[h_idx, w_idx] if channels == 1 else pixels[h_idx, w_idx, :]
            B = pixels[h_idx, w_idx_2] if channels == 1 else pixels[h_idx, w_idx_2, :]
            C = pixels[h_idx_2, w_idx] if channels == 1 else pixels[h_idx_2, w_idx, :]
            D = pixels[h_idx_2, w_idx_2] if channels == 1 else pixels[h_idx_2, w_idx_2, :]

            # Calcular a média dos quatro pixels conforme a fórmula
            new_value = (int(A) + int(B) + int(C) + int(D)) / 4
            new_pixels[i, j] = new_value

    return new_pixels  # Retorna o array de novos pixels interpolados

if __name__ == '__main__':
    # Caminho do arquivo da imagem
    file_path = "/home/andre/desenvolvimento/processamento_de_imagens_2024-2/1/brat.jpeg"

    # Carregando a imagem
    image = load_image(file_path)  # Chama a função para carregar a imagem

    # Convertendo a imagem em escala de cinza
    gray_image = rgb_to_gray(image)  # Converte a imagem para escala de cinza

    # Obtendo os pixels da imagem em escala de cinza
    pixels = get_pixels(gray_image)  # Obtém os pixels da imagem em escala de cinza

    # Redimensionando a imagem utilizando a interpolação bilinear
    new_size = (gray_image.size[0] // 2, gray_image.size[1] // 2)  # Define o novo tamanho da imagem (reduzindo pela metade)
    new_pixels = bilinear_interpolation(pixels, new_size)  # Realiza a interpolação bilinear

    # Definindo os pixels na nova imagem
    new_image = set_pixels(new_pixels)  # Define os novos pixels na imagem

    # Salvando a nova imagem em um arquivo externo
    save_image(new_image, "/home/andre/desenvolvimento/processamento_de_imagens_2024-2/1/brat_reducao_bilinear.jpeg")  # Salva a nova imagem
    