'''Operações Aritméticas: Adição'''

# Bibliotecas externas:
import numpy as np
from PIL import Image

def add(matrix1, matrix2):
    # Verifica se as matrizes possuem o mesmo tamanho:
    if matrix1.shape != matrix2.shape:
        raise ValueError("As matrizes devem ter o mesmo tamanho.")

    # Cria uma matriz vazia com o mesmo tamanho das matrizes de entrada:
    result = np.zeros_like(matrix1)

    # Percorre cada elemento das matrizes e realiza a operação de adição:
    for i in range(matrix1.shape[0]):
        for j in range(matrix1.shape[1]):
            soma = matrix1[i, j] + matrix2[i, j]
            if soma > 255:
                soma = 255
            result[i, j] = soma

    # Retorna a matriz resultado:
    return result


if __name__ == '__main__':
    # Carrega as imagens:
    input_path1 = np.array(Image.open("/run/media/andre/arquivos/oneDrive/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/3/operacao_aritmetica/adicao/12.png").convert("L"))
    input_path2 = np.array(Image.open("/run/media/andre/arquivos/oneDrive/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/3/operacao_aritmetica/adicao/8.png").convert("L"))

    # Chama a função a de adição:
    matrix_add = np.add(input_path1, input_path2)

    # Cria uma nova imagem com o resultado:
    save_add_image = Image.fromarray(matrix_add)

    # Salva a nova imagem resultado:
    save_add_image.save("/run/media/andre/arquivos/oneDrive/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/3/operacao_aritmetica/adicao/resultado.png")
