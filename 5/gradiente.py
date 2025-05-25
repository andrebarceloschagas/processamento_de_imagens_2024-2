import os
import numpy as np
from PIL import Image, UnidentifiedImageError
import matplotlib.pyplot as plt
from typing import Tuple, Union

# --- Funções Auxiliares Padronizadas ---

def load_pil_image(file_path: str) -> Union[Image.Image, None]:
    """
    Carrega uma imagem a partir do caminho do arquivo usando Pillow.

    Args:
        file_path: Caminho para o arquivo de imagem.

    Returns:
        Um objeto Image da PIL se o carregamento for bem-sucedido, None caso contrário.
    """
    try:
        img = Image.open(file_path)
        return img
    except FileNotFoundError:
        print(f"Erro: Arquivo de imagem não encontrado em '{file_path}'.")
    except UnidentifiedImageError:
        print(f"Erro: Não foi possível identificar o arquivo de imagem. Pode estar corrompido ou não ser um formato suportado: '{file_path}'.")
    except Exception as e:
        print(f"Um erro inesperado ocorreu ao carregar a imagem '{file_path}': {e}")
    return None

def pil_to_numpy_array(image: Image.Image, dtype: type = np.uint8) -> np.ndarray:
    """
    Converte uma imagem PIL para um array NumPy.

    Args:
        image: A imagem PIL.
        dtype: O tipo de dados desejado para o array NumPy (padrão: np.uint8).

    Returns:
        Um array NumPy representando a imagem.
    """
    return np.array(image, dtype=dtype)

def numpy_to_pil_image(array: np.ndarray) -> Image.Image:
    """
    Converte um array NumPy para uma imagem PIL.
    Lida com escala de cinza (2D) e RGB (3D).

    Args:
        array: O array NumPy, esperado ser uint8.

    Returns:
        Um objeto Image da PIL.
    """
    if array.ndim == 2:
        return Image.fromarray(array.astype(np.uint8), 'L')
    elif array.ndim == 3 and array.shape[2] == 3:
        return Image.fromarray(array.astype(np.uint8), 'RGB')
    elif array.ndim == 3 and array.shape[2] == 4: # Suporte para RGBA
        return Image.fromarray(array.astype(np.uint8), 'RGBA')
    else:
        raise ValueError(f"Formato de array NumPy não suportado para conversão PIL: {array.shape}")

def save_numpy_as_image(array: np.ndarray, file_path: str) -> None:
    """
    Salva um array NumPy como um arquivo de imagem usando Pillow.

    Args:
        array: O array NumPy representando a imagem.
        file_path: Caminho para salvar o arquivo de imagem.
    """
    try:
        image = numpy_to_pil_image(array)
        image.save(file_path)
        print(f"Imagem salva com sucesso em '{file_path}'.")
    except Exception as e:
        print(f"Erro ao salvar imagem em '{file_path}': {e}")

def convert_pil_to_grayscale_numpy(image: Image.Image) -> np.ndarray:
    """
    Converte uma imagem PIL para um array NumPy em escala de cinza.

    Args:
        image: A imagem PIL de entrada.

    Returns:
        Um array NumPy representando a imagem em escala de cinza.
    """
    if image.mode == 'L':
        return pil_to_numpy_array(image)
    return pil_to_numpy_array(image.convert('L'))

# --- Funções Principais do Filtro de Sobel ---

def apply_convolution(image_array: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """
    Aplica uma convolução 2D a uma imagem usando um kernel especificado.
    Esta é uma implementação básica. Para desempenho, bibliotecas como SciPy são recomendadas.
    Trata as bordas replicando os pixels da borda (similar a 'border' em algumas libs).

    Args:
        image_array: Array NumPy 2D da imagem em escala de cinza.
        kernel: Array NumPy 2D representando o kernel de convolução.

    Returns:
        Array NumPy 2D da imagem após a convolução.
    """
    kernel_height, kernel_width = kernel.shape
    if kernel_height % 2 == 0 or kernel_width % 2 == 0:
        raise ValueError("O kernel deve ter dimensões ímpares.")

    pad_h = kernel_height // 2
    pad_w = kernel_width // 2

    # Adiciona padding à imagem replicando as bordas
    # Usamos np.pad com mode='edge' que replica os valores da borda
    padded_image = np.pad(image_array, ((pad_h, pad_h), (pad_w, pad_w)), mode='edge')
    
    output_image = np.zeros_like(image_array, dtype=np.float32)
    image_height, image_width = image_array.shape

    for r in range(image_height):
        for c in range(image_width):
            # A região da imagem corresponde ao kernel centrado em (r, c)
            # No array com padding, a submatriz começa em (r, c) e vai até (r+kernel_height, c+kernel_width)
            region = padded_image[r : r + kernel_height, c : c + kernel_width]
            output_image[r, c] = np.sum(region * kernel)
            
    return output_image

def sobel_filter_manual(
    image_gray_numpy: np.ndarray
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Aplica o filtro de Sobel para detectar bordas em uma imagem em escala de cinza.
    Calcula os gradientes Gx, Gy e a magnitude do gradiente.

    Args:
        image_gray_numpy: Array NumPy 2D representando a imagem em escala de cinza.

    Returns:
        Uma tupla contendo (grad_x, grad_y, magnitude_gradiente):
        - grad_x: Gradiente na direção X (bordas verticais).
        - grad_y: Gradiente na direção Y (bordas horizontais).
        - magnitude_gradiente: Magnitude do gradiente.
        Todos os arrays retornados são float32 e podem precisar ser normalizados para visualização.
    """
    kernel_sobel_x = np.array([[-1, 0, 1],
                               [-2, 0, 2],
                               [-1, 0, 1]], dtype=np.float32)
    
    kernel_sobel_y = np.array([[-1, -2, -1],
                               [ 0,  0,  0],
                               [ 1,  2,  1]], dtype=np.float32)

    grad_x = apply_convolution(image_gray_numpy.astype(np.float32), kernel_sobel_x)
    grad_y = apply_convolution(image_gray_numpy.astype(np.float32), kernel_sobel_y)
    
    magnitude_gradiente = np.sqrt(grad_x**2 + grad_y**2)
    
    return grad_x, grad_y, magnitude_gradiente

def normalize_to_uint8(array: np.ndarray) -> np.ndarray:
    """
    Normaliza um array NumPy para o intervalo 0-255 e converte para uint8.
    Lida com arrays que podem ter valores negativos (como gradientes).
    """
    # Desloca para que o mínimo seja 0, depois escala para 0-255
    min_val = np.min(array)
    max_val = np.max(array)
    if max_val == min_val: # Evita divisão por zero se o array for constante
        return np.zeros_like(array, dtype=np.uint8) if min_val == 0 else np.full_like(array, 128 if -1e-6 < min_val < 1e-6 else min_val, dtype=np.uint8)

    normalized = 255 * (array - min_val) / (max_val - min_val)
    return normalized.astype(np.uint8)

# --- Função de Plotagem ---

def plot_sobel_results(
    original_gray_numpy: np.ndarray,
    grad_x_numpy: np.ndarray,
    grad_y_numpy: np.ndarray,
    magnitude_numpy: np.ndarray,
    main_title: str = "Resultados do Filtro de Sobel",
    output_path: Union[str, None] = None
) -> None:
    """
    Plota a imagem original em cinza e os resultados do filtro de Sobel.

    Args:
        original_gray_numpy: Imagem original em escala de cinza (NumPy array).
        grad_x_numpy: Gradiente X (NumPy array).
        grad_y_numpy: Gradiente Y (NumPy array).
        magnitude_numpy: Magnitude do gradiente (NumPy array).
        main_title: Título principal para o plot.
        output_path: Caminho opcional para salvar o plot.
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(main_title, fontsize=16)

    # Normaliza gradientes para visualização (0-255)
    # Para Gx e Gy, é comum visualizar o valor absoluto ou uma normalização que centre o zero.
    # Aqui, normalizamos para mostrar a variação completa.
    vis_grad_x = normalize_to_uint8(grad_x_numpy)
    vis_grad_y = normalize_to_uint8(grad_y_numpy)
    vis_magnitude = normalize_to_uint8(magnitude_numpy)

    axes[0, 0].imshow(original_gray_numpy, cmap='gray', vmin=0, vmax=255)
    axes[0, 0].set_title(f"Original em Cinza\nShape: {original_gray_numpy.shape}")
    axes[0, 0].axis('off')

    axes[0, 1].imshow(vis_grad_x, cmap='gray', vmin=0, vmax=255)
    axes[0, 1].set_title(f"Gradiente X (Sobel)\nShape: {vis_grad_x.shape}")
    axes[0, 1].axis('off')

    axes[1, 0].imshow(vis_grad_y, cmap='gray', vmin=0, vmax=255)
    axes[1, 0].set_title(f"Gradiente Y (Sobel)\nShape: {vis_grad_y.shape}")
    axes[1, 0].axis('off')

    axes[1, 1].imshow(vis_magnitude, cmap='gray', vmin=0, vmax=255)
    axes[1, 1].set_title(f"Magnitude do Gradiente (Sobel)\nShape: {vis_magnitude.shape}")
    axes[1, 1].axis('off')

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
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
    
    input_image_filename = "centavos.jpeg"  # Exemplo, pode ser alterado
    input_image_path = os.path.join(script_dir, input_image_filename)

    output_dir_name = "resultados_gradiente_sobel"
    output_dir_path = os.path.join(script_dir, output_dir_name)

    try:
        os.makedirs(output_dir_path, exist_ok=True)
        print(f"Diretório de saída '{output_dir_path}' assegurado.")
    except OSError as e:
        print(f"Erro ao criar diretório de saída '{output_dir_path}': {e}")
        # exit(1)

    print(f"Carregando imagem: '{input_image_path}'...")
    pil_image_original = load_pil_image(input_image_path)

    if pil_image_original:
        print("Convertendo imagem para array NumPy em escala de cinza...")
        numpy_image_gray = convert_pil_to_grayscale_numpy(pil_image_original)
        
        # Salva a imagem original em cinza (NumPy)
        original_gray_filename = f"{os.path.splitext(input_image_filename)[0]}_gray_numpy.jpeg"
        original_gray_output_path = os.path.join(output_dir_path, original_gray_filename)
        save_numpy_as_image(numpy_image_gray, original_gray_output_path)

        print("Aplicando filtro de Sobel...")
        grad_x, grad_y, magnitude = sobel_filter_manual(numpy_image_gray)

        # Salva os componentes do gradiente e a magnitude
        # É importante notar que os gradientes podem ter valores negativos.
        # A função save_numpy_as_image espera uint8, então normalizamos antes de salvar.
        save_numpy_as_image(normalize_to_uint8(grad_x), os.path.join(output_dir_path, f"{os.path.splitext(input_image_filename)[0]}_sobel_gx.jpeg"))
        save_numpy_as_image(normalize_to_uint8(grad_y), os.path.join(output_dir_path, f"{os.path.splitext(input_image_filename)[0]}_sobel_gy.jpeg"))
        save_numpy_as_image(normalize_to_uint8(magnitude), os.path.join(output_dir_path, f"{os.path.splitext(input_image_filename)[0]}_sobel_magnitude.jpeg"))

        # Plotar e salvar resultados
        plot_filename = f"plot_{os.path.splitext(input_image_filename)[0]}_sobel_results.png"
        plot_output_path = os.path.join(output_dir_path, plot_filename)

        plot_sobel_results(
            original_gray_numpy=numpy_image_gray,
            grad_x_numpy=grad_x,
            grad_y_numpy=grad_y,
            magnitude_numpy=magnitude,
            main_title=f"Filtro de Sobel - {input_image_filename}",
            output_path=plot_output_path
        )
        print("Processamento com filtro de Sobel concluído.")
    else:
        print(f"Não foi possível carregar a imagem '{input_image_path}'. O script será interrompido.")
