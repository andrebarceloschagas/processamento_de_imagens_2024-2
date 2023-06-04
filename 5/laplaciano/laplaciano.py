from PIL import Image
import numpy as np

def laplacian_filter(image_path, kernel):
    # Carrega a imagem e converte para tons de cinza
    image = Image.open(image_path).convert('L')
    width, height = image.size

    # Converte a imagem para um array numpy
    img_array = np.array(image)

    # Aplica a convolução com a máscara Laplaciana
    filtered_array = np.zeros((height, width), dtype=np.float32)
    kernel_height, kernel_width = kernel.shape
    margin = kernel_width // 2

    for y in range(margin, height-margin):
        for x in range(margin, width-margin):
            total = 0
            for j in range(-margin, margin+1):
                for i in range(-margin, margin+1):
                    total += img_array[y+j, x+i] * kernel[j+margin, i+margin]
            filtered_array[y, x] = total

    # Normaliza a saída entre 0 e 255:
    filtered_array = filtered_array - filtered_array.min()
    filtered_array = (filtered_array / filtered_array.max()) * 255

    # Converte o array de volta para imagem
    filtered_image = Image.fromarray(filtered_array.astype(np.uint8))

    return filtered_image

if __name__ == '__main__':
    # Define as máscaras Laplacianas:
    mascara_1 = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
    mascara_2 = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])
    mascara_3 = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])
    mascara_4 = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])


    # Aplica as máscaras em uma imagem de exemplo
    image_path = '/run/media/andre/arquivos/oneDrive/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/5/laplaciano/marisa.jpg'

    # Chama a função
    filtered_image1 = laplacian_filter(image_path, mascara_1)
    filtered_image2 = laplacian_filter(image_path, mascara_2)
    filtered_image3 = laplacian_filter(image_path, mascara_3)
    filtered_image4 = laplacian_filter(image_path, mascara_4)

    # Salva as imagens resultantes
    filtered_image1.save('/run/media/andre/arquivos/oneDrive/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/5/laplaciano/filtered_image1.jpg')
    filtered_image2.save('/run/media/andre/arquivos/oneDrive/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/5/laplaciano/filtered_image2.jpg')
    filtered_image3.save('/run/media/andre/arquivos/oneDrive/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/5/laplaciano/filtered_image3.jpg')
    filtered_image4.save('/run/media/andre/arquivos/oneDrive/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/5/laplaciano/filtered_image4.jpg')
