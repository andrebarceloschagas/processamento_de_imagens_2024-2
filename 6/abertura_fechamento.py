import os
import numpy as np
from PIL import Image, UnidentifiedImageError
import matplotlib.pyplot as plt
from typing import Tuple, Union, Literal

# --- Funções Auxiliares Padronizadas ---

def load_pil_image(file_path: str) -> Union[Image.Image, None]:
    """
    Carrega uma imagem usando Pillow.
    """
    try:
        img = Image.open(file_path)
        return img
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em '{file_path}'.")
    except UnidentifiedImageError:
        print(f"Erro: Não foi possível identificar o arquivo de imagem: '{file_path}'.")
    except Exception as e:
        print(f"Erro ao carregar imagem '{file_path}': {e}")
    return None

def pil_to_numpy_array(image: Image.Image, dtype: type = np.uint8) -> np.ndarray:
    """
    Converte imagem PIL para array NumPy.
    """
    return np.array(image, dtype=dtype)

def numpy_to_pil_image(array: np.ndarray) -> Image.Image:
    """
    Converte array NumPy para imagem PIL.
    """
    mode = None
    if array.ndim == 2:
        mode = 'L' # Grayscale
    elif array.ndim == 3:
        if array.shape[2] == 3:
            mode = 'RGB'
        elif array.shape[2] == 4:
            mode = 'RGBA'
    if mode is None:
        raise ValueError(f"Formato de array NumPy não suportado para conversão PIL: {array.shape}")
    return Image.fromarray(array.astype(np.uint8), mode)

def save_numpy_as_image(array: np.ndarray, file_path: str) -> None:
    """
    Salva array NumPy como imagem.
    """
    try:
        image = numpy_to_pil_image(array)
        image.save(file_path)
        print(f"Imagem salva com sucesso em '{file_path}'.")
    except Exception as e:
        print(f"Erro ao salvar imagem em '{file_path}': {e}")

def convert_pil_to_grayscale_numpy(image: Image.Image) -> np.ndarray:
    """
    Converte imagem PIL para array NumPy em escala de cinza.
    """
    if image.mode == 'L':
        return pil_to_numpy_array(image)
    return pil_to_numpy_array(image.convert('L'))

def binarize_numpy_array(image_array: np.ndarray, threshold: int = 128) -> np.ndarray:
    """
    Binariza um array NumPy (0 ou 255).
    Espera-se que a entrada seja um array em escala de cinza.
    """
    if image_array.ndim != 2:
        print("Alerta: Binarização geralmente é aplicada em imagens 2D (escala de cinza).")
    # Garante que o resultado seja 0 ou 255 e do tipo uint8
    return np.where(image_array < threshold, 0, 255).astype(np.uint8)

# --- Funções Morfológicas Fundamentais ---

def apply_morphological_operation(
    binary_image_numpy: np.ndarray,
    structuring_element_numpy: np.ndarray,
    operation: Literal['erosion', 'dilation']
) -> np.ndarray:
    """
    Aplica uma operação morfológica (erosão ou dilatação) a uma imagem binária.
    Trata as bordas preenchendo com o valor oposto ao da operação para evitar efeitos indesejados.
    (0 para dilatação, 255 para erosão no padding).

    Args:
        binary_image_numpy: Array NumPy 2D da imagem binária (0 ou 255).
        structuring_element_numpy: Array NumPy 2D do elemento estruturante (binário).
        operation: 'erosion' ou 'dilation'.

    Returns:
        Array NumPy 2D da imagem resultante.
    """
    if binary_image_numpy.ndim != 2 or structuring_element_numpy.ndim != 2:
        raise ValueError("Imagem e elemento estruturante devem ser 2D.")
    if not np.all(np.isin(binary_image_numpy, [0, 255])):
        raise ValueError("A imagem de entrada deve ser binária (0 ou 255).")
    if not np.all(np.isin(structuring_element_numpy, [0, 1])):
         # Elemento estruturante geralmente é 0 e 1 (ou booleano)
        print("Alerta: Elemento estruturante geralmente contém 0s e 1s.")

    se_height, se_width = structuring_element_numpy.shape
    pad_h, pad_w = se_height // 2, se_width // 2

    # Padding: 0 para dilatação (para que o máximo não seja afetado por bordas altas)
    # 255 para erosão (para que o mínimo não seja afetado por bordas baixas)
    pad_value = 0 if operation == 'dilation' else 255
    padded_image = np.pad(binary_image_numpy, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=pad_value)
    
    output_image = np.zeros_like(binary_image_numpy)
    img_height, img_width = binary_image_numpy.shape

    # Pontos do elemento estruturante onde o valor é 1 (relevante para a operação)
    se_points = structuring_element_numpy == 1

    for r in range(img_height):
        for c in range(img_width):
            region = padded_image[r : r + se_height, c : c + se_width]
            
            if operation == 'erosion':
                # Para erosão, todos os pixels do elemento estruturante (onde SE=1)
                # devem caber na região da imagem (onde IMG=255).
                # Se a região coberta pelo SE (onde SE=1) for toda 255, o pixel central é 255.
                if np.all(region[se_points] == 255):
                    output_image[r, c] = 255
                else:
                    output_image[r, c] = 0 # Default para erosão
            elif operation == 'dilation':
                # Para dilatação, se qualquer pixel do elemento estruturante (onde SE=1)
                # sobrepuser um pixel 255 na imagem, o pixel central é 255.
                if np.any(region[se_points] == 255):
                    output_image[r, c] = 255
                else:
                    output_image[r, c] = 0 # Default para dilatação
            else:
                raise ValueError(f"Operação morfológica desconhecida: {operation}")
                
    return output_image.astype(np.uint8)

def erosion_manual(binary_image_numpy: np.ndarray, structuring_element_numpy: np.ndarray) -> np.ndarray:
    return apply_morphological_operation(binary_image_numpy, structuring_element_numpy, 'erosion')

def dilation_manual(binary_image_numpy: np.ndarray, structuring_element_numpy: np.ndarray) -> np.ndarray:
    return apply_morphological_operation(binary_image_numpy, structuring_element_numpy, 'dilation')

def opening_manual(binary_image_numpy: np.ndarray, structuring_element_numpy: np.ndarray) -> np.ndarray:
    """Abertura = Erosão seguida de Dilatação."""
    eroded = erosion_manual(binary_image_numpy, structuring_element_numpy)
    opened = dilation_manual(eroded, structuring_element_numpy)
    return opened

def closing_manual(binary_image_numpy: np.ndarray, structuring_element_numpy: np.ndarray) -> np.ndarray:
    """Fechamento = Dilatação seguida de Erosão."""
    dilated = dilation_manual(binary_image_numpy, structuring_element_numpy)
    closed = erosion_manual(dilated, structuring_element_numpy)
    return closed

# --- Função de Plotagem ---

def plot_morphological_results(
    original_binary_numpy: np.ndarray,
    eroded_numpy: np.ndarray,
    dilated_numpy: np.ndarray,
    opened_numpy: np.ndarray,
    closed_numpy: np.ndarray,
    structuring_element_shape: Tuple[int, int],
    main_title: str = "Operações Morfológicas",
    output_path: Union[str, None] = None
) -> None:
    """
    Plota os resultados das operações morfológicas.
    """
    fig, axes = plt.subplots(1, 5, figsize=(20, 4))
    fig.suptitle(f"{main_title} (Elemento Estruturante: {structuring_element_shape[0]}x{structuring_element_shape[1]})", fontsize=14)

    titles = ['Original Binarizada', 'Erosão', 'Dilatação', 'Abertura', 'Fechamento']
    images = [original_binary_numpy, eroded_numpy, dilated_numpy, opened_numpy, closed_numpy]

    for i, (title, img) in enumerate(zip(titles, images)):
        axes[i].imshow(img, cmap='gray', vmin=0, vmax=255)
        axes[i].set_title(f"{title}\nShape: {img.shape}")
        axes[i].axis('off')

    plt.tight_layout(rect=[0, 0, 1, 0.93])
    
    if output_path:
        try:
            plt.savefig(output_path)
            print(f"Plot salvo com sucesso em '{output_path}'.")
        except Exception as e:
            print(f"Erro ao salvar o plot em '{output_path}': {e}")
    plt.show()

# --- Bloco de Execução Principal ---

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    input_image_filename = "18.png"  # Exemplo, pode ser alterado
    input_image_path = os.path.join(script_dir, input_image_filename)

    output_dir_name = "resultados_morfologicos"
    output_dir_path = os.path.join(script_dir, output_dir_name)

    try:
        os.makedirs(output_dir_path, exist_ok=True)
        print(f"Diretório de saída '{output_dir_path}' assegurado.")
    except OSError as e:
        print(f"Erro ao criar diretório de saída '{output_dir_path}': {e}")
        # exit(1)

    # Parâmetros
    binarization_threshold = 128
    # Elemento estruturante: quadrado 3x3 de 1s. Pode ser alterado.
    # Para operações morfológicas, o elemento estruturante é geralmente binário (0 ou 1).
    struct_elem_numpy = np.ones((3, 3), dtype=np.uint8) 

    print(f"Carregando imagem: '{input_image_path}'...")
    pil_image_original = load_pil_image(input_image_path)

    if pil_image_original:
        print("Convertendo imagem para array NumPy em escala de cinza...")
        numpy_image_gray = convert_pil_to_grayscale_numpy(pil_image_original)
        
        print(f"Binarizando imagem com limiar {binarization_threshold}...")
        numpy_image_binary = binarize_numpy_array(numpy_image_gray, threshold=binarization_threshold)
        save_numpy_as_image(numpy_image_binary, os.path.join(output_dir_path, f"{os.path.splitext(input_image_filename)[0]}_binarizada.png"))

        print(f"Aplicando operações morfológicas com elemento estruturante {struct_elem_numpy.shape}...")
        try:
            eroded_img = erosion_manual(numpy_image_binary, struct_elem_numpy)
            dilated_img = dilation_manual(numpy_image_binary, struct_elem_numpy)
            opened_img = opening_manual(numpy_image_binary, struct_elem_numpy)
            closed_img = closing_manual(numpy_image_binary, struct_elem_numpy)

            # Salvar imagens resultantes
            save_numpy_as_image(eroded_img, os.path.join(output_dir_path, f"{os.path.splitext(input_image_filename)[0]}_erosao.png"))
            save_numpy_as_image(dilated_img, os.path.join(output_dir_path, f"{os.path.splitext(input_image_filename)[0]}_dilatacao.png"))
            save_numpy_as_image(opened_img, os.path.join(output_dir_path, f"{os.path.splitext(input_image_filename)[0]}_abertura.png"))
            save_numpy_as_image(closed_img, os.path.join(output_dir_path, f"{os.path.splitext(input_image_filename)[0]}_fechamento.png"))

            # Plotar e salvar resultados
            plot_filename = f"plot_{os.path.splitext(input_image_filename)[0]}_morfologia_se{struct_elem_numpy.shape[0]}x{struct_elem_numpy.shape[1]}.png"
            plot_output_path = os.path.join(output_dir_path, plot_filename)

            plot_morphological_results(
                original_binary_numpy=numpy_image_binary,
                eroded_numpy=eroded_img,
                dilated_numpy=dilated_img,
                opened_numpy=opened_img,
                closed_numpy=closed_img,
                structuring_element_shape=struct_elem_numpy.shape,
                main_title=f"Operações Morfológicas - {input_image_filename}",
                output_path=plot_output_path
            )

        except ValueError as ve:
            print(f"Erro durante operações morfológicas: {ve}")
        except Exception as e:
            print(f"Um erro inesperado ocorreu: {e}")
            
        print("Processamento morfológico concluído.")
    else:
        print(f"Não foi possível carregar a imagem '{input_image_path}'. O script será interrompido.")
