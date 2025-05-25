import os
import numpy as np
from PIL import Image, UnidentifiedImageError
import matplotlib.pyplot as plt
from typing import Tuple, Union, Literal

# --- Funções Auxiliares Padronizadas (Reutilizadas de abertura_fechamento.py) ---

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

# --- Funções Morfológicas Fundamentais (Adaptadas para Escala de Cinza) ---

def apply_grayscale_morphological_operation(
    grayscale_image_numpy: np.ndarray,
    structuring_element_numpy: np.ndarray, # Geralmente binário (0s e 1s)
    operation: Literal['erosion', 'dilation']
) -> np.ndarray:
    """
    Aplica uma operação morfológica (erosão ou dilatação) a uma imagem em escala de cinza.
    Trata as bordas replicando os pixels da borda.

    Args:
        grayscale_image_numpy: Array NumPy 2D da imagem em escala de cinza.
        structuring_element_numpy: Array NumPy 2D do elemento estruturante (geralmente binário, 0 ou 1).
                                   Os 1s definem a vizinhança.
        operation: 'erosion' (mínimo local) ou 'dilation' (máximo local).

    Returns:
        Array NumPy 2D da imagem resultante (mesmo dtype da entrada).
    """
    if grayscale_image_numpy.ndim != 2 or structuring_element_numpy.ndim != 2:
        raise ValueError("Imagem e elemento estruturante devem ser 2D.")
    if not np.all(np.isin(structuring_element_numpy, [0, 1])):
        print("Alerta: Elemento estruturante para morfologia em escala de cinza geralmente é binário (0s e 1s) para definir a vizinhança.")

    se_height, se_width = structuring_element_numpy.shape
    pad_h, pad_w = se_height // 2, se_width // 2

    # Padding com replicação de borda é comum para morfologia em escala de cinza
    padded_image = np.pad(grayscale_image_numpy, ((pad_h, pad_h), (pad_w, pad_w)), mode='edge')
    
    output_image = np.zeros_like(grayscale_image_numpy)
    img_height, img_width = grayscale_image_numpy.shape

    # Pontos do elemento estruturante onde o valor é 1 (define a vizinhança)
    se_mask = structuring_element_numpy == 1

    for r in range(img_height):
        for c in range(img_width):
            region = padded_image[r : r + se_height, c : c + se_width]
            # Considera apenas os pixels da região sob os 1s do elemento estruturante
            neighborhood_pixels = region[se_mask]
            
            if not neighborhood_pixels.size: # Caso o SE seja todo de zeros (improvável mas defensivo)
                output_image[r,c] = grayscale_image_numpy[r,c]
                continue

            if operation == 'erosion':
                output_image[r, c] = np.min(neighborhood_pixels)
            elif operation == 'dilation':
                output_image[r, c] = np.max(neighborhood_pixels)
            else:
                raise ValueError(f"Operação morfológica desconhecida: {operation}")
                
    return output_image.astype(grayscale_image_numpy.dtype)

def erosion_grayscale_manual(grayscale_image_numpy: np.ndarray, structuring_element_numpy: np.ndarray) -> np.ndarray:
    return apply_grayscale_morphological_operation(grayscale_image_numpy, structuring_element_numpy, 'erosion')

def dilation_grayscale_manual(grayscale_image_numpy: np.ndarray, structuring_element_numpy: np.ndarray) -> np.ndarray:
    return apply_grayscale_morphological_operation(grayscale_image_numpy, structuring_element_numpy, 'dilation')

# --- Função de Plotagem ---

def plot_grayscale_morph_results(
    original_gray_numpy: np.ndarray,
    eroded_gray_numpy: np.ndarray,
    dilated_gray_numpy: np.ndarray,
    structuring_element_shape: Tuple[int, int],
    main_title: str = "Erosão e Dilatação em Escala de Cinza",
    output_path: Union[str, None] = None
) -> None:
    """
    Plota os resultados da erosão e dilatação em escala de cinza.
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle(f"{main_title} (Elem. Estrut.: {structuring_element_shape[0]}x{structuring_element_shape[1]})", fontsize=14)

    titles = ['Original em Cinza', 'Erosão em Cinza', 'Dilatação em Cinza']
    images = [original_gray_numpy, eroded_gray_numpy, dilated_gray_numpy]

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
    
    input_image_filename = "trabalho_pratico.png"  # Exemplo, pode ser alterado
    input_image_path = os.path.join(script_dir, input_image_filename)

    output_dir_name = "resultados_morfologia_cinza"
    output_dir_path = os.path.join(script_dir, output_dir_name)

    try:
        os.makedirs(output_dir_path, exist_ok=True)
        print(f"Diretório de saída '{output_dir_path}' assegurado.")
    except OSError as e:
        print(f"Erro ao criar diretório de saída '{output_dir_path}': {e}")
        # exit(1)

    # Elemento estruturante: quadrado 3x3 de 1s. Define a vizinhança.
    struct_elem_numpy = np.ones((3, 3), dtype=np.uint8)

    print(f"Carregando imagem: '{input_image_path}'...")
    pil_image_original = load_pil_image(input_image_path)

    if pil_image_original:
        print("Convertendo imagem para array NumPy em escala de cinza...")
        numpy_image_gray = convert_pil_to_grayscale_numpy(pil_image_original)
        save_numpy_as_image(numpy_image_gray, os.path.join(output_dir_path, f"{os.path.splitext(input_image_filename)[0]}_gray.png"))

        print(f"Aplicando operações morfológicas em escala de cinza com elemento estruturante {struct_elem_numpy.shape}...")
        try:
            eroded_gray_img = erosion_grayscale_manual(numpy_image_gray, struct_elem_numpy)
            dilated_gray_img = dilation_grayscale_manual(numpy_image_gray, struct_elem_numpy)

            # Salvar imagens resultantes
            save_numpy_as_image(eroded_gray_img, os.path.join(output_dir_path, f"{os.path.splitext(input_image_filename)[0]}_erosao_cinza.png"))
            save_numpy_as_image(dilated_gray_img, os.path.join(output_dir_path, f"{os.path.splitext(input_image_filename)[0]}_dilatacao_cinza.png"))

            # Plotar e salvar resultados
            plot_filename = f"plot_{os.path.splitext(input_image_filename)[0]}_morfologia_cinza_se{struct_elem_numpy.shape[0]}x{struct_elem_numpy.shape[1]}.png"
            plot_output_path = os.path.join(output_dir_path, plot_filename)

            plot_grayscale_morph_results(
                original_gray_numpy=numpy_image_gray,
                eroded_gray_numpy=eroded_gray_img,
                dilated_gray_numpy=dilated_gray_img,
                structuring_element_shape=struct_elem_numpy.shape,
                main_title=f"Morfologia em Cinza - {input_image_filename}",
                output_path=plot_output_path
            )

        except ValueError as ve:
            print(f"Erro durante operações morfológicas: {ve}")
        except Exception as e:
            print(f"Um erro inesperado ocorreu: {e}")
            
        print("Processamento morfológico em escala de cinza concluído.")
    else:
        print(f"Não foi possível carregar a imagem '{input_image_path}'. O script será interrompido.")
