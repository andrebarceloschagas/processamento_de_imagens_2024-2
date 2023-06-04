# Filtro da Média

from PIL import Image

def filtro_media(image_path, size):
    # Abre a imagem e converte para tons de cinza:
    image = Image.open(image_path).convert('L')
    width, height = image.size

    # Calcula a margem (metade do tamanho do filtro):
    margin = size // 2

    # Cria uma nova imagem com o mesmo tamanho da original:
    filtered_image = Image.new('L', (width, height))

    # Itera sobre todos os pixels da imagem:
    for x in range(margin, width - margin):
        for y in range(margin, height - margin):

            # Inicializa o valor da soma:
            total = 0
            # Itera sobre todos os pixels vizinhos:
            for i in range(-margin, margin+1):
                for j in range(-margin, margin+1):
                    # Soma o valor do pixel vizinho:
                    total += image.getpixel((x+i, y+j))

            # Calcula a média dos valores dos pixels vizinhos:
            average = total // 9
            # Define o valor do pixel filtrado na nova imagem:
            filtered_image.putpixel((x, y), average)

    # Preenche as bordas da imagem com zeros:
    for x in range(width):
        for y in range(margin):
            filtered_image.putpixel((x, y), 0)
            filtered_image.putpixel((x, height-y-1), 0)
    for x in range(margin):
        for y in range(height):
            filtered_image.putpixel((x, y), 0)
            filtered_image.putpixel((width-x-1, y), 0)

    return filtered_image

if __name__ == '__main__':
    # Carrega a imagem:
    image_path = filtro_media('/mnt/3ACCDBA5CCDB59A9/one/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/5/filtro_media/marisa.jpg', 3)

    # Salva a imagem equalizada:
    image_path.save('/mnt/3ACCDBA5CCDB59A9/one/UFT/disciplinas/8_periodo/3_processamento_de_imagens/codigos/5/filtro_media/image_filtered.jpg')
