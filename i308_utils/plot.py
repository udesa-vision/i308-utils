import matplotlib.pyplot as plt
import cv2


def imshow(image, title=None):
    """

        Grafica una imagen usando matplotlib

    """
    if len(image.shape) == 2:  # Imagen en escala de grises
        plt.imshow(image, cmap='gray')
    else:  # Imagen en color (asumimos BGR)
        im = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        plt.imshow(im)

    if title is not None:
        plt.title(title, fontsize=10)
    plt.axis('off')
    plt.show()


def show_images(
        images,
        titles=None,
        grid=None,
        figsize=None,
        # title=None,
        # subtitle=None,
        show=True,
):
    """

        Grafica una lista de imágenes usando subplot de matplotlib.

        Args:
            images (list):
                lista de imágenes. para cada imagen:
                    - si es de 1 canal, se grafica en escala de grises.
                    - si es de 3 canales, se asume que está en formato BGR.
            titles (list, optional):
                títulos individuales para cada imagen. si no se proporciona, no se mostrarán títulos.
            grid (tuple, optional):
                tupla que indica el número de filas y columnas a utilizar en el subplot.
                si no se especifica, se asume una única fila.
            figsize (tuple, optional):
                tamaño del plot. si no se proporciona, se usará el tamaño por defecto de matplotlib.
            # title (str, optional):
            #     título general del plot.
            # subtitle (str, optional):
            #     subtítulo general del plot.

        Raises:
            ValueError: si la longitud de `titles` no coincide con la longitud de `images`.

    """

    if grid is None:
        grid = (1, len(images))

    if titles is None:
        titles = [None for _ in images]
    elif len(titles) != len(images):
        raise ValueError("la longitud de `titles` debe coincidir con la longitud de `images`.")

    n_rows, n_cols = grid
    if figsize is None:
        base_size = 3.5  # define el tamaño base por celda
        min_width = 12  # establece un ancho mínimo de la figura
        min_height = 3.5 * n_rows  # ajusta la altura según el número de filas

        figsize = (
            max(n_cols * base_size, min_width),
            max(min_height, 5)  # establece un mínimo de altura para evitar que sea muy chico
        )

    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)

    # convierte axes en una lista si solo hay una imagen
    if n_rows == 1 and n_cols == 1:
        axes = [axes]
    else:
        axes = axes.flat

    for i, ax in enumerate(axes):
        if i >= len(images):
            ax.axis('off')
            continue
        if len(images[i].shape) == 2:  # imagen en escala de grises
            ax.imshow(images[i], cmap='gray', vmin=0, vmax=255)
        else:  # imagen en color (asume BGR)
            im = cv2.cvtColor(images[i], cv2.COLOR_BGR2RGB)
            ax.imshow(im)

        if titles[i] is not None:
            ax.set_title(titles[i])
        ax.axis('off')

    # ajusta dinámicamente el espaciado según la cantidad de filas
    # top_margin = 0.92 - (0.04 * (n_rows - 1))  # reduce espacio si hay más filas
    # bottom_margin = 0.08 + (0.02 * (n_rows - 1)) + (0.03 * (n_rows > 1))  # más margen si hay más filas

    # if title is not None:
    #     fig.suptitle(title, fontsize=14, y=top_margin)
    #
    # if subtitle is not None:
    #     fig.text(0.5, bottom_margin, subtitle, ha='center', va='bottom', fontsize=12)
    #
    # # ajusta márgenes dinámicamente solo si hay pocas filas
    # fig.subplots_adjust(
    #     top=top_margin - 0.02 if n_rows == 1 else top_margin - 0.05,
    #     bottom=bottom_margin + 0.03 if n_rows > 1 else bottom_margin + 0.02,
    #     hspace=0.3 if n_rows > 1 else 0.1  # reduce el espacio vertical si hay una fila
    # )

    if show:
        plt.show()
