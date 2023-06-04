# Transformação de intensidade negativa

from PIL import Image

def negative_intensity(image_path):
    image = Image.open(image_path).convert('L')  # Abre a imagem em tons de cinza.
    neg_image = Image.new('L', image.size)  # Cria uma nova imagem com o mesmo tamanho da original.

    # Itera sobre todos os pixels da imagem e aplica a transformação de intensidade negativa.
    for x in range(image.width):  # duas estruturas de loop são usadas para iterar sobre todos os pixels da imagem.
        for y in range(image.height):
            pixel = 255 - image.getpixel((x, y))
            neg_image.putpixel((x, y), pixel)

    return neg_image

if __name__ == '__main__':
    image_path = negative_intensity('/run/media/andre/arquivos/oneDrive/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/4/intensidade/gize.jpg')
    image_path.save('/run/media/andre/arquivos/oneDrive/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/4/intensidade/negativa.jpg')
