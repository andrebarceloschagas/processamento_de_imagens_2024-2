# Equalização de Histograma Normalizado

from PIL import Image

def equalizacao_histograma(imagem):
    gray_image = imagem.convert('L')  # Converte a imagem para tons de cinza.
    hist = monta_histograma(gray_image)  # Calcula o histograma da imagem em tons de cinza.
    hist_norm = soma_hist_normalizado(hist)  # Normaliza o histograma.
    lut = criacao_lut(hist_norm)  # Chama a função de criação da LUT.
    return gray_image.point(lut)  # Retorno da funçao.

def monta_histograma(imagem):
    hist = [0] * 256  # Cria uma lista de 256 elementos com valor inicial zero para armazenar o histograma.
    largura, altura = imagem.size  # Armazena a largura e a altura da imagem em variáveis.

    # Percorre todos os pixels da imagem e atualiza o valor do histograma na posição correspondente.
    for i in range(largura):
        for j in range(altura):
            pixel = imagem.getpixel((i, j))  # Obtém o valor do pixel na posição (i, j).
            hist[pixel] += 1  # Incrementa o valor do histograma na posição correspondente.
    return hist  # Retorna o histograma da imagem.

def soma_hist_normalizado(hist):
    s = sum(hist)  # Calcula a soma de todos os valores do histograma.
    hist_norm = [float(i)/s for i in hist]  # Normaliza o histograma dividindo cada valor pela soma.
    return hist_norm  # Retorna o histograma normalizado.

def criacao_lut(hist_norm):
    lut = []  # Cria uma lista vazia para a tabela de pesquisa de intensidade.
    for i in range(256):  # Percorre todos os valores de intensidade de pixel.
        j = 0
        # Encontra o menor valor de j tal que a soma dos valores do histograma normalizado até j seja maior ou igual a i/255.
        while j < 256 and sum(hist_norm[:j]) <= i/255.0:
            j += 1
        lut.append(j - 1)  # Adiciona o valor j - 1 à tabela de pesquisa de intensidade.
    return lut  # Retorna a tabela de pesquisa de intensidade.


if __name__ == '__main__':
    # carrega a imagem
    image_path = Image.open('/run/media/andre/arquivos/oneDrive/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/4/equalizacao/gize.jpg')

    # chama a função de equalização de histograma
    image_eq = equalizacao_histograma(image_path)

    # salva a imagem equalizada
    image_eq.save('/run/media/andre/arquivos/oneDrive/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/4/equalizacao/imagem_eq.jpg')
