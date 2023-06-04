'''Operações Geométricas: Espelhamento'''


# Bibliotecas externas:
from PIL import Image
import numpy as np

def espelhamento_horizontal(image):
    # Obtém as dimensões da imagem:
    altura, largura = image.shape
    
    # Cria uma imagem vazia com as mesmas dimensões da imagem original:
    result = np.zeros((altura, largura), dtype=np.uint8)
    
    # Percorre a imagem e copia os valores na imagem espelhada:
    for i in range(altura):
        for j in range(largura):
            result[i, j] = image[i, largura - j - 1]
    
    # Retorna a imagem espelhada:
    return result

if __name__ == '__main__':
    # Carrega as imagens:
    input_path = np.array(Image.open("/run/media/andre/arquivos/oneDrive/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/3/operacao_geometrica/olho.jpg").convert("L"))

    # Chama a função de espelhamento:
    imagem_espelhada = espelhamento_horizontal(input_path)

    # Cria uma nova imagem com o resultado:
    imagem_resultado = Image.fromarray(imagem_espelhada)

    # Salva a nova imagem:
    imagem_resultado.save("/run/media/andre/arquivos/oneDrive/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/3/operacao_geometrica/resultado_olho.jpg")
