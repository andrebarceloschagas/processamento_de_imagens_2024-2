from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def laplacian_filter(image_array, kernel):
    """
    Função para aplicar o filtro laplaciano em uma imagem.
    """
    height, width = image_array.shape
    kernel_height, kernel_width = kernel.shape
    margin = kernel_width // 2

    # Cria um array vazio para armazenar a imagem filtrada
    filtered_array = np.zeros((height, width), dtype=np.float32)

    # Aplica a convolução com a máscara Laplaciana
    for y in range(margin, height - margin):  # Itera sobre as linhas da imagem (y representa a coordenada vertical)
        for x in range(margin, width - margin):  # Itera sobre as colunas da imagem (x representa a coordenada horizontal)
            total = 0  # Inicializa a soma (o valor convolucionado) para o pixel (x, y)
            
            # Itera sobre a área da vizinhança ao redor do pixel (x, y), considerando a máscara (kernel)
            for j in range(-margin, margin + 1):  # Varia o deslocamento vertical (j) com base na margem do kernel
                for i in range(-margin, margin + 1):  # Varia o deslocamento horizontal (i) com base na margem do kernel
                    # Multiplica o valor do pixel da imagem pelo valor correspondente no kernel
                    total += image_array[y + j, x + i] * kernel[j + margin, i + margin]  # Soma o valor convolucionado

            # Atribui o valor da convolução (soma total) ao pixel (y, x) da imagem filtrada
            filtered_array[y, x] = total  # O pixel (y, x) recebe o valor convolucionado no array de saída (filtered_array)


    # Normaliza a saída entre 0 e 255
    filtered_array = (filtered_array - filtered_array.min()) / (filtered_array.max() - filtered_array.min()) * 255

    return filtered_array.astype(np.uint8)

if __name__ == '__main__':
    # Define as máscaras Laplacianas:
    mascara_1 = np.array([[0, 1, 0], # Laplaciano 1
                          [1, -4, 1], # Esta máscara detecta mudanças de intensidade de forma simples.
                          [0, 1, 0]]) # Destaca as bordas mais grossas e não destaca detalhes da transição.
                                      # ênfase nas transições verticais e horizontais

    mascara_2 = np.array([[1, 1, 1], # Laplaciano 2
                          [1, -8, 1], # Mais agressiva. Detecta bordas mais finas e destaca mais detalhes da transição
                          [1, 1, 1]]) # É mais sensível a ruídos e detalhes da imagem.
                                      # ênfase nas transições diagonais
                                    
    mascara_3 = np.array([[0, -1, 0], # Laplaciano 3
                          [-1, 4, -1], # Máscara que destaca bordas mais grossas e não destaca detalhes da transição.
                          [0, -1, 0]]) # É mais suave que a máscara 1.

    mascara_4 = np.array([[-1, -1, -1], # Laplaciano 4
                          [-1, 8, -1],  # Máscara que destaca bordas mais finas e destaca mais detalhes da transição.
                          [-1, -1, -1]]) # Com mais contraste nas bordas

    # Carrega a imagem original
    image_path = "/home/andre/dev/processamento_de_imagens_2024-2/5/centavos.jpeg"
    original_image = Image.open(image_path)

    # Converte a imagem para escala de cinza
    image_gray = original_image.convert('L')
    image_array = np.array(image_gray)

    # Aplica as máscaras Laplacianas
    filtered_image1 = laplacian_filter(image_array, mascara_1)
    filtered_image2 = laplacian_filter(image_array, mascara_2)
    filtered_image3 = laplacian_filter(image_array, mascara_3)
    filtered_image4 = laplacian_filter(image_array, mascara_4)

    # Salva a imagem em tons de cinza
    Image.fromarray(image_array).save("/home/andre/dev/processamento_de_imagens_2024-2/5/laplaciano_centavos_gray.jpeg")

    # Salva as imagens filtradas
    Image.fromarray(filtered_image1).save("/home/andre/dev/processamento_de_imagens_2024-2/5/laplaciano_1.jpeg")
    Image.fromarray(filtered_image2).save("/home/andre/dev/processamento_de_imagens_2024-2/5/laplaciano_2.jpeg")
    Image.fromarray(filtered_image3).save("/home/andre/dev/processamento_de_imagens_2024-2/5/laplaciano_3.jpeg")
    Image.fromarray(filtered_image4).save("/home/andre/dev/processamento_de_imagens_2024-2/5/laplaciano_4.jpeg")
