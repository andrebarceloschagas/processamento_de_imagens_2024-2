'''Operações Aritméticas: Subtração'''

# Bibliotecas externas:
import numpy as np
from PIL import Image

def subtract(matrix1, matrix2):
    # Verifica se as matrizes possuem o mesmo tamanho:
    if matrix1.shape != matrix2.shape:
        raise ValueError("As matrizes devem ter o mesmo tamanho.")

    # Cria uma matriz vazia com o mesmo tamanho das matrizes de entrada:
    result = np.zeros_like(matrix1)

    # Percorre cada elemento das matrizes e realiza a operação de subtração:
    for i in range(matrix1.shape[0]):
        for j in range(matrix1.shape[1]):
            subtract = matrix1[i, j] - matrix2[i, j]
            if subtract < 0:
                subtract = 0
            result[i, j] = subtract

    # Retorna a matriz resultado:
    return result


if __name__ == '__main__':
    # Carrega as imagens:
    input_path1 = np.array(Image.open("/run/media/andre/arquivos/oneDrive/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/3/operacao_aritmetica/subtracao/19.png").convert("L"))
    input_path2 = np.array(Image.open("/run/media/andre/arquivos/oneDrive/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/3/operacao_aritmetica/subtracao/14.png").convert("L"))

    # Chama a função de subtração:
    matrix_subtract = np.add(input_path1, input_path2)

    # Cria uma nova imagem com o resultado:
    save_subtract_image = Image.fromarray(matrix_subtract)

    # Salva a nova imagem resultado:
    save_subtract_image.save("/run/media/andre/arquivos/oneDrive/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/3/operacao_aritmetica/subtracao/resultado.png")
