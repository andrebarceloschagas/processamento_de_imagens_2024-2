import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os
from typing import Tuple, Union, Dict, List, Any


def load_image_pil(file_path: str) -> Union[Image.Image, None]:
    """
    Carrega uma imagem a partir do caminho do arquivo usando Pillow.

    Args:
        file_path: O caminho para o arquivo de imagem.

    Returns:
        Um objeto Image da PIL se o carregamento for bem-sucedido, None caso contrário.
    """
    try:
        image = Image.open(file_path)
        return image
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em '{file_path}'")
        return None
    except Exception as e:
        print(f"Erro ao carregar a imagem '{file_path}': {e}")
        return None


def binarize_pil_image(image: Image.Image, threshold: int = 128) -> np.ndarray:
    """
    Converte uma imagem PIL (primeiro para escala de cinza) em um array NumPy binário.

    Args:
        image: A imagem PIL a ser convertida.
        threshold: O limiar para binarização (0-255). Pixels < threshold tornam-se 0, senão 255.

    Returns:
        Um array NumPy (uint8) com a imagem binarizada (valores 0 ou 255).
    """
    if image.mode != 'L':
        image_gray = image.convert('L')
    else:
        image_gray = image
    binary_array = np.array(image_gray.point(lambda x: 0 if x < threshold else 255), dtype=np.uint8)
    return binary_array


def save_numpy_as_image(image_array: np.ndarray, output_path: str) -> None:
    """
    Salva um array NumPy como um arquivo de imagem.

    Args:
        image_array: O array NumPy a ser salvo (espera-se dtype=uint8).
        output_path: O caminho do arquivo para salvar a imagem.
    """
    try:
        image = Image.fromarray(image_array.astype(np.uint8))
        image.save(output_path)
        print(f"Imagem salva em '{output_path}'")
    except Exception as e:
        print(f"Erro ao salvar a imagem em '{output_path}': {e}")


def save_array_as_text_matrix(binary_array: np.ndarray, output_path: str) -> None:
    """
    Salva um array NumPy binário (0s e 255s) como uma matriz de '0's e '1's em um arquivo de texto.

    Args:
        binary_array: O array NumPy binário (valores 0 ou 255).
        output_path: O caminho do arquivo de texto para salvar a matriz.
    """
    try:
        # Converte 0 para '0' e 255 para '1'
        text_matrix = np.where(binary_array == 0, '0', '1')
        np.savetxt(output_path, text_matrix, fmt='%s')
        print(f"Matriz binária salva em '{output_path}'")
    except Exception as e:
        print(f"Erro ao salvar a matriz de texto em '{output_path}': {e}")


def plot_segmentation_results(original_pil: Image.Image, 
                              binary_array: np.ndarray, 
                              labeled_array: np.ndarray, 
                              num_objects: int,
                              output_path: str = None) -> None:
    """
    Plota a imagem original, a imagem binária e a imagem rotulada.

    Args:
        original_pil: A imagem original (Pillow Image).
        binary_array: A imagem binarizada (NumPy array).
        labeled_array: A imagem com componentes rotulados (NumPy array).
        num_objects: O número de objetos detectados.
        output_path: Caminho opcional para salvar o plot.
    """
    plt.figure(figsize=(18, 6))

    plt.subplot(1, 3, 1)
    plt.imshow(original_pil)
    plt.title("Imagem Original")
    plt.axis("off")

    plt.subplot(1, 3, 2)
    plt.imshow(binary_array, cmap='gray')
    plt.title("Imagem Binária")
    plt.axis("off")

    plt.subplot(1, 3, 3)
    # Usar um colormap que distinga bem os rótulos. 'nipy_spectral' ou 'tab20b' são boas opções.
    # Normalizar para que o fundo (0) seja uma cor e os objetos outras.
    cmap = plt.cm.get_cmap('nipy_spectral', num_objects + 1) if num_objects > 0 else plt.cm.get_cmap('gray')
    plt.imshow(labeled_array, cmap=cmap, vmin=0, vmax=num_objects if num_objects > 0 else 1)
    plt.title(f"Imagem Rotulada ({num_objects} objetos)")
    plt.axis("off")

    plt.tight_layout()
    if output_path:
        try:
            plt.savefig(output_path)
            print(f"Plot salvo em '{output_path}'")
        except Exception as e:
            print(f"Erro ao salvar o plot em '{output_path}': {e}")
    plt.show()


def label_connected_components_dsu(binary_array: np.ndarray) -> Tuple[np.ndarray, int]:
    """
    Rotula componentes conectados em uma imagem binária usando um algoritmo de duas passagens
    com Disjoint Set Union (DSU) para resolução de equivalências.

    Args:
        binary_array: Um array NumPy 2D representando a imagem binária,
                      onde pixels de objeto são 255 e fundo é 0.

    Returns:
        Tuple[np.ndarray, int]:
            - Um array NumPy 2D com os componentes rotulados (rótulos são inteiros > 0).
            - O número de objetos (componentes conectados) encontrados.
            
    Nota:
        Para aplicações mais robustas e otimizadas, considere usar bibliotecas como
        `scipy.ndimage.label`.
    """
    rows, cols = binary_array.shape
    labeled_array = np.zeros_like(binary_array, dtype=np.int32)
    current_label_id = 0
    # parents[i] armazena o pai do rótulo i. Rótulo 0 é fundo e não é usado aqui.
    # Inicialmente, cada novo rótulo é seu próprio pai.
    parents: List[int] = [0] # parents[0] é um placeholder

    def find_set(label_id: int) -> int:
        # Encontra o representante (raiz) do conjunto ao qual label_id pertence (com compressão de caminho).
        if parents[label_id] == label_id:
            return label_id
        parents[label_id] = find_set(parents[label_id])
        return parents[label_id]

    def union_sets(label_id1: int, label_id2: int) -> None:
        # Une os conjuntos que contêm label_id1 e label_id2.
        root1 = find_set(label_id1)
        root2 = find_set(label_id2)
        if root1 != root2:
            # Faz a raiz menor ser a pai da raiz maior para manter consistência (opcional, mas bom)
            if root1 < root2:
                parents[root2] = root1
            else:
                parents[root1] = root2
    
    # Primeira passagem: Atribuição inicial de rótulos e registro de equivalências
    for r in range(rows):
        for c in range(cols):
            if binary_array[r, c] == 255:  # Pixel de objeto
                # Vizinhos relevantes (Norte e Oeste para conectividade-4)
                neighbor_labels: List[int] = []
                if r > 0 and labeled_array[r - 1, c] > 0: # Vizinho de cima
                    neighbor_labels.append(labeled_array[r - 1, c])
                if c > 0 and labeled_array[r, c - 1] > 0: # Vizinho da esquerda
                    neighbor_labels.append(labeled_array[r, c - 1])
                
                if not neighbor_labels:
                    # Novo componente
                    current_label_id += 1
                    labeled_array[r, c] = current_label_id
                    parents.append(current_label_id) # Adiciona novo rótulo como seu próprio pai
                else:
                    # Pixel conectado a componentes existentes
                    min_neighbor_label = min(neighbor_labels)
                    labeled_array[r, c] = min_neighbor_label
                    # Unir todos os rótulos vizinhos ao menor rótulo vizinho
                    for lbl in neighbor_labels:
                        if lbl != min_neighbor_label:
                            union_sets(min_neighbor_label, lbl)
    
    # Segunda passagem: Resolver equivalências e re-rotular para rótulos sequenciais (1, 2, ...)
    # Mapeia raízes de DSU para novos rótulos compactos (1, 2, ..., num_objects)
    root_to_new_label: Dict[int, int] = {}
    num_objects = 0
    for r in range(rows):
        for c in range(cols):
            if labeled_array[r, c] > 0: # Se for um pixel de objeto rotulado
                root = find_set(labeled_array[r, c])
                if root not in root_to_new_label:
                    num_objects += 1
                    root_to_new_label[root] = num_objects
                labeled_array[r, c] = root_to_new_label[root]
                
    return labeled_array, num_objects


if __name__ == '__main__':
    # Diretório de entrada e nome da imagem
    input_dir = "/home/andre/dev/processamento_de_imagens_2024-2/2"
    input_image_name = "18.png" # Ou outra imagem para teste
    input_path = os.path.join(input_dir, input_image_name)

    # Diretório de saída
    output_dir = os.path.join(input_dir, "resultados_rotulacao")
    os.makedirs(output_dir, exist_ok=True)

    print(f"Processando imagem: {input_path}")
    original_pil_image = load_image_pil(input_path)

    if original_pil_image:
        try:
            # 1. Binarizar a imagem
            print("Binarizando imagem...")
            binary_image_array = binarize_pil_image(original_pil_image, threshold=128)
            
            base_name = os.path.splitext(input_image_name)[0]
            binary_image_output_path = os.path.join(output_dir, f"{base_name}_binary.png")
            save_numpy_as_image(binary_image_array, binary_image_output_path)

            binary_matrix_output_path = os.path.join(output_dir, f"{base_name}_binary_matrix.txt")
            save_array_as_text_matrix(binary_image_array, binary_matrix_output_path)

            # 2. Rotular componentes conectados
            print("Rotulando componentes conectados...")
            labeled_image_array, num_found_objects = label_connected_components_dsu(binary_image_array)
            print(f"Número de objetos encontrados: {num_found_objects}")

            # (Opcional) Salvar a imagem rotulada (array numérico) se necessário para análise,
            # mas o plot já a visualiza com colormap.
            # labeled_image_output_path = os.path.join(output_dir, f"{base_name}_labeled_array.png")
            # save_numpy_as_image(labeled_image_array, labeled_image_output_path) # Precisaria de normalização/colormap para visualização direta

            # 3. Plotar resultados
            print("Plotando resultados...")
            plot_output_path = os.path.join(output_dir, f"{base_name}_segmentation_plot.png")
            plot_segmentation_results(original_pil_image.copy(),  # Passar cópia se original_pil_image for usada depois
                                      binary_image_array, 
                                      labeled_image_array, 
                                      num_found_objects,
                                      plot_output_path)
            
            print("Processamento de rotulação concluído com sucesso.")

        except Exception as e:
            print(f"Ocorreu um erro durante o processamento da imagem '{input_image_name}': {e}")
    else:
        print(f"Não foi possível carregar a imagem '{input_image_name}'. Encerrando o script.")
