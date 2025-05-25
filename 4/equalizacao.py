import os
import numpy as np
from PIL import Image, ImageOps, UnidentifiedImageError
import matplotlib.pyplot as plt
from typing import List, Tuple, Union

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

def save_pil_image(image: Image.Image, file_path: str) -> None:
    """
    Salva uma imagem PIL em um arquivo externo.

    Args:
        image: A imagem PIL a ser salva.
        file_path: O caminho para salvar a imagem.
    """
    try:
        image.save(file_path)
        print(f"Imagem salva com sucesso em '{file_path}'.")
    except Exception as e:
        print(f"Erro ao salvar a imagem em '{file_path}': {e}")

def convert_pil_to_grayscale(image: Image.Image) -> Image.Image:
    """
    Converte uma imagem PIL para escala de cinza.

    Args:
        image: A imagem PIL de entrada.

    Returns:
        Uma nova imagem PIL em escala de cinza ('L' mode).
    """
    if image.mode == 'L':
        return image
    return image.convert('L')

# --- Funções Principais de Equalização de Histograma ---

def calculate_histogram_pil(image_gray: Image.Image) -> List[int]:
    """
    Calcula o histograma de uma imagem PIL em escala de cinza.

    Args:
        image_gray: Imagem PIL em escala de cinza.

    Returns:
        Lista representando o histograma (256 níveis).
    """
    if image_gray.mode != 'L':
        raise ValueError("A imagem de entrada para calcular o histograma deve estar em escala de cinza ('L' mode).")
    return image_gray.histogram()

def calculate_cdf_normalized(histogram: List[int]) -> List[float]:
    """
    Calcula a Função de Distribuição Cumulativa (CDF) normalizada do histograma.

    Args:
        histogram: Lista representando o histograma.

    Returns:
        Lista representando a CDF normalizada.
    """
    cdf = [0.0] * 256
    cdf[0] = histogram[0]
    for i in range(1, 256):
        cdf[i] = cdf[i-1] + histogram[i]

    # Normaliza a CDF pelo número total de pixels (soma do histograma)
    total_pixels = cdf[-1]
    if total_pixels == 0: # Evita divisão por zero para imagens vazias/constantes
        return [0.0] * 256
        
    cdf_normalized = [val / total_pixels for val in cdf]
    return cdf_normalized

def create_equalization_lut(cdf_normalized: List[float]) -> List[int]:
    """
    Cria a Look-Up Table (LUT) para a equalização do histograma.

    Args:
        cdf_normalized: Lista representando a CDF normalizada.

    Returns:
        Lista (LUT) mapeando níveis de cinza originais para novos níveis.
    """
    lut = [0] * 256
    for i in range(256):
        lut[i] = int(round(cdf_normalized[i] * 255))
    return lut

def equalize_histogram_pil(image_gray: Image.Image) -> Image.Image:
    """
    Aplica a equalização de histograma a uma imagem PIL em escala de cinza.
    Este método usa a funcionalidade nativa do Pillow que é mais otimizada.

    Args:
        image_gray: Imagem PIL em escala de cinza.

    Returns:
        Imagem PIL equalizada.
    """
    if image_gray.mode != 'L':
        raise ValueError("A imagem de entrada para equalização deve estar em escala de cinza ('L' mode).")
    return ImageOps.equalize(image_gray)

def equalize_histogram_manual(image_gray: Image.Image) -> Image.Image:
    """
    Aplica a equalização de histograma a uma imagem PIL em escala de cinza
    usando o cálculo manual de histograma, CDF e LUT.

    Args:
        image_gray: Imagem PIL em escala de cinza.

    Returns:
        Imagem PIL equalizada.
    """
    if image_gray.mode != 'L':
        raise ValueError("A imagem de entrada para equalização manual deve estar em escala de cinza ('L' mode).")
    
    hist = calculate_histogram_pil(image_gray)
    cdf_norm = calculate_cdf_normalized(hist)
    lut = create_equalization_lut(cdf_norm)
    
    # Aplica a LUT usando o método point()
    return image_gray.point(lut)

# --- Função de Plotagem ---

def plot_images_and_histograms(
    original_pil_gray: Image.Image,
    equalized_pil: Image.Image,
    hist_gray: List[int],
    hist_equalized: List[int],
    main_title: str = "Equalização de Histograma",
    output_path: Union[str, None] = None
) -> None:
    """
    Plota as imagens (original em cinza, equalizada) e seus respectivos histogramas.

    Args:
        original_pil_gray: Imagem PIL original em escala de cinza.
        equalized_pil: Imagem PIL equalizada.
        hist_gray: Histograma da imagem original em cinza.
        hist_equalized: Histograma da imagem equalizada.
        main_title: Título principal para o plot.
        output_path: Caminho opcional para salvar o plot.
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(main_title, fontsize=16)

    # Imagem Original em Cinza
    axes[0, 0].imshow(original_pil_gray, cmap='gray', vmin=0, vmax=255)
    axes[0, 0].set_title(f"Imagem Original em Cinza\nShape: {original_pil_gray.size}")
    axes[0, 0].axis('off')

    # Histograma Original em Cinza
    axes[1, 0].bar(range(256), hist_gray, width=1.0, color='gray')
    axes[1, 0].set_title("Histograma Original")
    axes[1, 0].set_xlabel("Nível de Cinza")
    axes[1, 0].set_ylabel("Frequência")
    axes[1, 0].set_xlim([0, 255])

    # Imagem Equalizada
    axes[0, 1].imshow(equalized_pil, cmap='gray', vmin=0, vmax=255)
    axes[0, 1].set_title(f"Imagem Equalizada\nShape: {equalized_pil.size}")
    axes[0, 1].axis('off')

    # Histograma Equalizado
    axes[1, 1].bar(range(256), hist_equalized, width=1.0, color='blue')
    axes[1, 1].set_title("Histograma Equalizado")
    axes[1, 1].set_xlabel("Nível de Cinza")
    axes[1, 1].set_ylabel("Frequência")
    axes[1, 1].set_xlim([0, 255])

    plt.tight_layout(rect=[0, 0, 1, 0.96]) # Ajusta para o suptitle
    
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
    
    input_image_filename = "museu.jpg" # Exemplo, pode ser alterado
    input_image_path = os.path.join(script_dir, "..", "3", input_image_filename) # Ajuste o caminho se necessário
    
    # Tenta carregar de um caminho alternativo se não encontrar no primeiro
    if not os.path.exists(input_image_path):
        input_image_path_alt = os.path.join(script_dir, input_image_filename)
        if os.path.exists(input_image_path_alt):
            input_image_path = input_image_path_alt
        else:
            # Tenta carregar do diretório 5 se ainda não encontrou
            input_image_path_alt2 = os.path.join(script_dir, "..", "5", input_image_filename)
            if os.path.exists(input_image_path_alt2):
                 input_image_path = input_image_path_alt2
            else:
                print(f"Alerta: Arquivo de imagem '{input_image_filename}' não encontrado nos caminhos esperados.")


    output_dir_name = "resultados_equalizacao"
    output_dir_path = os.path.join(script_dir, output_dir_name)

    try:
        os.makedirs(output_dir_path, exist_ok=True)
        print(f"Diretório de saída '{output_dir_path}' assegurado.")
    except OSError as e:
        print(f"Erro ao criar diretório de saída '{output_dir_path}': {e}")
        # Considerar sair se o diretório for crítico: exit(1)

    print(f"Carregando imagem: '{input_image_path}'...")
    pil_image_original = load_pil_image(input_image_path)

    if pil_image_original:
        print("Convertendo imagem original para escala de cinza...")
        pil_image_gray = convert_pil_to_grayscale(pil_image_original)
        
        # Salva a imagem original em escala de cinza
        original_gray_filename = f"{os.path.splitext(input_image_filename)[0]}_gray.jpg"
        original_gray_output_path = os.path.join(output_dir_path, original_gray_filename)
        save_pil_image(pil_image_gray, original_gray_output_path)

        print("Calculando histograma da imagem em cinza...")
        hist_gray_original = calculate_histogram_pil(pil_image_gray)

        print("Aplicando equalização de histograma (método Pillow)...")
        # Usando o método otimizado do Pillow por padrão
        pil_image_equalized = equalize_histogram_pil(pil_image_gray) 
        # Alternativamente, para usar o método manual:
        # pil_image_equalized = equalize_histogram_manual(pil_image_gray)

        print("Calculando histograma da imagem equalizada...")
        hist_equalized_new = calculate_histogram_pil(pil_image_equalized)

        # Salva a imagem equalizada
        equalized_filename = f"{os.path.splitext(input_image_filename)[0]}_equalizada.jpg"
        equalized_output_path = os.path.join(output_dir_path, equalized_filename)
        save_pil_image(pil_image_equalized, equalized_output_path)

        # Plotar e salvar resultados
        plot_filename = f"plot_{os.path.splitext(input_image_filename)[0]}_equalizacao.png"
        plot_output_path = os.path.join(output_dir_path, plot_filename)
        
        plot_images_and_histograms(
            original_pil_gray=pil_image_gray,
            equalized_pil=pil_image_equalized,
            hist_gray=hist_gray_original,
            hist_equalized=hist_equalized_new,
            main_title=f"Equalização de Histograma - {input_image_filename}",
            output_path=plot_output_path
        )
        print("Processamento de equalização concluído.")
    else:
        print(f"Não foi possível carregar a imagem '{input_image_path}'. O script será interrompido.")
