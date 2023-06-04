1
Agora vou falar sobre tecnicas de Filtragen.

2
O filtro da média é um dos filtros mais simples usados em processamento de imagens.
Ele é usado para suavizar imagens, removendo detalhes finos e ruídos.
O filtro funciona através da substituição de cada pixel na imagem pela média dos valores dos pixels na sua vizinhança imediata.
O tamanho da vizinhança é determinado pelo tamanho da janela usada para aplicar o filtro, e quanto maior a janela, maior é o efeito de suavização sobre a imagem.
Embora o filtro da média seja útil para remover ruídos, ele também pode causar uma perda de detalhes importantes, o que pode tornar a imagem final menos nítida.

3
O filtro Laplaciano é um tipo de filtro de realce de imagem que é usado para destacar as bordas e detalhes finos de uma imagem.
Ele funciona detectando mudanças abruptas na intensidade dos pixels de uma imagem, aumentando essas mudanças e reduzindo as áreas de intensidade constante.
O filtro é implementado por convolução de uma máscara Laplaciana com a imagem original.

4
O filtro de gradiente usando máscaras de Sobel é uma técnica de processamento de imagem que calcula a magnitude do gradiente da imagem em cada pixel, realçando as bordas e detalhes.
Isso é feito aplicando duas máscaras de convolução, uma para calcular as diferenças horizontais e outra para as diferenças verticais na intensidade dos pixels.
As duas convoluções são combinadas para obter a magnitude do gradiente em cada pixel.
Esse filtro é amplamente utilizado em tarefas de detecção de bordas, segmentação de imagem e processamento de imagens médicas.
