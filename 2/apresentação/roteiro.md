## Roteiro 

1
Olá professora glenda.
Sou o Antonio André e eu sou a Helorrayne Cristine.
Vamos apresentar um código, da segunda implementação de PI, em Python onde é implementada uma técnica de processamento de imagem conhecida como rotulação de objetos.
2
A rotulagem de objetos é uma técnica que consiste em atribuir um rótulo a cada pixel em uma imagem binária de forma que pixels pertencentes ao mesmo objeto tenham o mesmo rótulo.
3
O código utiliza duas bibliotecas externas.
A biblioteca numpy é utilizada para trabalhar com arrays multidimensionais e a biblioteca pillow é utilizada para carregar e salvar imagens.
O código começa com uma função chamada to_binary_image, que converte uma imagem colorida em uma imagem binária usando um limiar.
O limiar é um valor que determina se um pixel deve ser considerado branco ou preto na imagem binária resultante.
O valor padrão para o limiar é 128. A função carrega a imagem e converte para escala de cinza pela função .convert("L") da biblioteca pillow.
Em seguida, usa a biblioteca numpy para criar uma matriz binária a partir da imagem, onde pixels com valores abaixo do limiar são pretos (0) e pixels com valores acima do limiar são brancos (255).
A função retorna a matriz binária resultante.
3
A próxima função é save_binary_matrix, que salva uma matriz binária como um arquivo de texto.
A função recebe uma matriz binária e um caminho de arquivo de saída e usa a biblioteca numpy para inverter os valores da matriz binária (que pode ser colocado qualquer string para representar o branco e o preto) e salvar a matriz em um arquivo de texto com valores separados por espaço.
O arquivo resultante pode ser usado para representar uma imagem binária como uma matriz binária de zeros e uns (ou qualquer outro caracter) em um formato legível e visualmente didático.
4
A próxima função é save_binary_image, que salva uma matriz binária como uma imagem.
A função recebe uma matriz binária e um caminho de arquivo de saída e usa a biblioteca pillow para criar uma imagem a partir da matriz.
A imagem é então salva no arquivo especificado.
5
A última função (e a principal) é label_objects, que rotula objetos em uma imagem binária.
A função começa criando uma matriz de rótulos com o mesmo tamanho da matriz de entrada e preenchendo-a com zeros.
Dentro dos loops que percorrem os pixels da imagem binária, o código checa se o pixel atual pertence a um objeto (isto é, se é branco). Caso seja, o código busca todos os pixels adjacentes ao pixel atual que já foram rotulados e adiciona seus rótulos a uma lista de rótulos adjacentes.
Se nenhum pixel adjacente foi rotulado, o código atribui um novo rótulo ao pixel atual e atualiza o contador de rótulos. Caso contrário, o código atribui o menor rótulo adjacente ao pixel atual e adiciona as equivalências de rótulo, se houver mais de um rótulo adjacente.
Ao final da rotulação, a função retorna uma matriz de rótulos, em que cada pixel pertence a um objeto e é representado pelo seu rótulo.
A função recebe uma matriz binária como entrada e retorna uma matriz rotulada.
6
No final do código temos a main, que:
Carrega a imagem de entrada.
Depois, converte-a em uma imagem binária usando a função to_binary_image.
Mais adiante, chama a função label_objects para rotular a imagem binaria.
por fim, temos:
A a chamada da função save_binary_image para salvar a imagem já rotulada e a chamada da função save_binary_matrix para salvar em formato de texto a matriz rotulada.
7
E agora vamos rodar o código: