# Importando as bibliotecas necessárias
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
    pixels = np.array(image, dtype=np.float32)  # Converte a imagem para um array numpy de float32 para evitar overflow
    return pixels  # Retorna o array de pixels

def set_pixels(pixels):
    """
    Função para definir os pixels em uma imagem.
    """
    pixels = np.clip(pixels, 0, 255)  # Garante que os valores dos pixels estejam entre 0 e 255
    image = Image.fromarray(pixels.astype('uint8'))  # Converte o array de volta para uint8 e cria uma imagem
    return image  # Retorna a imagem criada a partir dos pixels

def rgb_to_gray(image):
    """
    Função para transformar a imagem em escala de cinza.
    """
    gray_image = image.convert('L')  # Converte a imagem para escala de cinza
    return gray_image  # Retorna a imagem em escala de cinza

def bilinear_interpolation_ampliacao(pixels, new_size):
    """
    Função para realizar a interpolação bilinear para ampliação de imagem.
    """
    height, width = pixels.shape[:2]  # Obtém a altura e a largura da imagem original
    if len(pixels.shape) == 2:
        channels = 1  # Para imagens em escala de cinza
    else:
        channels = pixels.shape[2]  # Para imagens coloridas (RGB)
    
    new_height, new_width = new_size  # Define a nova altura e largura da imagem
    # Cria um array vazio para os novos pixels, com float32 para evitar overflow
    new_pixels = np.zeros((new_height, new_width, channels), dtype=np.float32) if channels > 1 else np.zeros((new_height, new_width), dtype=np.float32)

    for i in range(0, new_height, 2):
        for j in range(0, new_width, 2):
            # Índices dos pixels originais
            h_idx = i // 2
            w_idx = j // 2
            h_idx_2 = min(h_idx + 1, height - 1)
            w_idx_2 = min(w_idx + 1, width - 1)

            # Pegar os quatro pixels vizinhos
            f_ij = pixels[h_idx, w_idx] if channels == 1 else pixels[h_idx, w_idx, :]
            f_ij1 = pixels[h_idx, w_idx_2] if channels == 1 else pixels[h_idx, w_idx_2, :]
            f_i1j = pixels[h_idx_2, w_idx] if channels == 1 else pixels[h_idx_2, w_idx, :]
            f_i1j1 = pixels[h_idx_2, w_idx_2] if channels == 1 else pixels[h_idx_2, w_idx_2, :]

            # Cálculos de interpolação (a, b, c, d, e) com float32 para evitar overflow
            a = (f_ij + f_ij1) / 2
            e = (f_i1j + f_i1j1) / 2
            b = (f_ij + f_i1j) / 2
            d = (f_ij1 + f_i1j1) / 2
            c = (f_ij + f_ij1 + f_i1j + f_i1j1) / 4

            # Atribuindo os valores aos novos pixels
            new_pixels[i, j] = f_ij         # Ponto original
            new_pixels[i, j + 1] = a        # Ponto interpolado 'a'
            new_pixels[i + 1, j] = b        # Ponto interpolado 'b'
            new_pixels[i + 1, j + 1] = c    # Ponto interpolado 'c'

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

    # Definindo o novo tamanho da imagem (ampliando por fator de 2)
    new_size = (gray_image.size[0] * 2, gray_image.size[1] * 2)  # Calcula o novo tamanho da imagem

    # Redimensionando a imagem utilizando a interpolação bilinear para ampliação
    new_pixels = bilinear_interpolation_ampliacao(pixels, new_size)  # Realiza a interpolação bilinear

    # Definindo os pixels na nova imagem
    new_image = set_pixels(new_pixels)  # Define os novos pixels na imagem

    # Salvando a nova imagem em um arquivo externo
    save_image(new_image, "/home/andre/desenvolvimento/processamento_de_imagens_2024-2/1/brat_ampliacao_bilinear.jpeg")  # Salva a nova imagem
    